import sqlite3
import numpy as np
import os
import speech_recognition as sr
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator
from playsound import playsound
import subprocess
import uuid
import time
import wave
import pyaudio
from gtts import gTTS
import threading
import random

# ✅ Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
fwhisper_model = WhisperModel("tiny", compute_type="int8", cpu_threads=4)

# 🧠 Load model and database
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
conn = sqlite3.connect(os.path.join(base_dir, "voice_dataset.db"))
cursor = conn.cursor()
cursor.execute('SELECT id, question, answer, answer_audio_path FROM qa_pairs')
rows = cursor.fetchall()
conn.close()

# 📦 ID → (question, answer, audio_path)
id_map = {
    i: (row[1], row[2], os.path.join(base_dir, row[3]) if not os.path.isabs(row[3]) else row[3])
    for i, row in enumerate(rows)
}

# 🔠 Embedding all questions
questions = [id_map[i][0] for i in id_map]
question_vecs = model.encode(questions)

# 🗣️ Natural filler phrases (to play during transcription)
FILLER_PHRASES = [
    "ہممم... اچھا سوال ہے۔",
    "جی بالکل، ایک لمحہ۔",
    "یہ میں نے سنا، دیکھتی ہوں۔",
    "ٹھیک ہے، تھوڑا سا انتظار کیجیے۔",
    "سمجھ گئی، ابھی بتاتی ہوں۔",
    "یہ ذرا غور سے سن رہی ہوں۔",
    "ایک سیکنڈ، میں دیکھتی ہوں۔",
    "ہاں جی، یہ دھیان سے سن رہی ہوں۔",
    "جی ضرور، جواب تلاش کر رہی ہوں۔",
    "تھوڑا سا وقت دیں، میں دیکھ رہی ہوں۔"
]

FILLER_AUDIO_FILES = []
filler_dir = os.path.join(base_dir, "filler_audios")
os.makedirs(filler_dir, exist_ok=True)

for i, phrase in enumerate(FILLER_PHRASES):
    audio_path = os.path.join(filler_dir, f"filler_{i}.mp3")
    if not os.path.exists(audio_path):
        tts = gTTS(text=phrase, lang="ur")
        tts.save(audio_path)
    FILLER_AUDIO_FILES.append(audio_path)

# 🔊 Background thread: speaks filler while transcription runs
def speak_filler_while(flag):
    path = random.choice(FILLER_AUDIO_FILES)
    try:
        playsound(path)
    except Exception as e:
        print(f"⚠️ Filler playback error: {e}")
    finally:
        flag["running"] = False

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening (Google STT)...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            transcription = recognizer.recognize_google(audio, language="ur-PK")
            print(f"🗣️ You said (Google STT): {transcription}")
            return transcription
        except sr.WaitTimeoutError:
            print("⏱️ Timeout, no speech")
        except sr.UnknownValueError:
            print("❌ Google couldn't understand")
        except Exception as e:
            print(f"❌ Google STT failed: {e}")
        return ""
    
def speak(text):
    tts = gTTS(text=text, lang="ur")
    path = os.path.join(base_dir, "temp_reply.mp3")
    tts.save(path)
    playsound(path)
    os.remove(path)

def contains_exit_word(text):
    words = ["اللہ حافظ", "خاتم", "ختم", "بند", "بس", "چلیں", "خدا حافظ"]
    return next((w for w in words if w in text), None)

def wait_for_wake_word():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("👂 Say 'ہیلو' or 'السلام علیکم' to begin...")
            try:
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=5)
                wake_phrase = recognizer.recognize_google(audio, language="ur-PK")
                print(f"🗣️ Heard: {wake_phrase}")
                if "السلام علیکم" in wake_phrase:
                    speak("السلام علیکم، میں آپ کی کیسے مدد کر سکتی ہوں؟")
                    return
                if "ہیلو" in wake_phrase:
                    speak("ہیلو، میں آپ کی کیسے مدد کر سکتی ہوں؟")
                    return
            except sr.WaitTimeoutError:
                print("⏱️ No input, trying again...")
            except:
                print("❌ Could not understand wake word.")

def search(query, top_k=3, min_score=0.3):
    if not query.strip():
        return

    translated = Translator().translate(query, dest="ur").text
    print(f"🌐 Translated: {translated}")

    query_vec = model.encode([translated])
    scores = cosine_similarity(query_vec, question_vecs)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    print("\n🔍 Top Matches:")
    for idx in top_indices:
        score = scores[idx]
        print(f"🔹 Score: {score:.2f}")
        if score < min_score:
            print("⚠️ Match skipped: below threshold")
            continue
        question, answer, audio_path = id_map[idx]
        print(f"❓ {question}")
        print(f"💬 {answer}")
        if os.path.exists(audio_path):
            try:
                playsound(audio_path)
            except Exception as e:
                print(f"⚠️ Couldn't play audio: {e}")
        else:
            print(f"❌ Missing audio: {audio_path}")

if __name__ == "__main__":
    wait_for_wake_word()
    while True:
        query = recognize_speech()
        if not query:
            continue
        exit_word = contains_exit_word(query)
        if exit_word:
            speak(exit_word)
            break
        search(query)
