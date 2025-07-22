import sqlite3
import os
from gtts import gTTS   
from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import uuid

# Initialize Whisper for Urdu STT
whisper_model = WhisperModel("small", compute_type="int8")

# Connect to SQLite
conn = sqlite3.connect("voice_dataset.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS qa_pairs (
    id TEXT PRIMARY KEY,
    question TEXT,
    answer TEXT,
    answer_audio_path TEXT
)
""")
conn.commit()

def record_audio(filename="temp.wav", duration=4):
    fs = 16000
    print(f"🎙️ Recording {filename} for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    print(f"✅ Saved {filename}")
    return filename

def transcribe(audio_path):
    segments, info = whisper_model.transcribe(audio_path, language="ur")
    return " ".join([seg.text.strip() for seg in segments])

def get_input_pair(mode):
    if mode == "v":
        question_audio = record_audio("question.wav")
        question_text = transcribe(question_audio)
        print("🧠 Question:", question_text)

        answer_audio = record_audio("answer.wav")
        answer_text = transcribe(answer_audio)
        print("🧠 Answer:", answer_text)
    else:
        question_text = input("❓ Enter Question (Urdu or Roman Urdu): ").strip()
        answer_text = input("💬 Enter Answer (Urdu or Roman Urdu): ").strip()

    return question_text, answer_text

def store_pair(question_text, answer_text):
    audio_dir = os.path.join(os.getcwd(), "tts_audio")
    os.makedirs(audio_dir, exist_ok=True)

    audio_filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
    audio_path = os.path.join(audio_dir, audio_filename)

    try:
        tts = gTTS(text=answer_text, lang="ur")
        tts.save(audio_path)
        print(f"🔊 TTS saved to: {audio_path}")
    except Exception as e:
        print("❌ TTS generation failed:", e)
        return

    entry_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO qa_pairs (id, question, answer, answer_audio_path) VALUES (?, ?, ?, ?)",
        (entry_id, question_text, answer_text, audio_path)
    )
    conn.commit()
    print("✅ Stored successfully!\n")

# --- MAIN LOOP ---
print("🎙️ Voice-based Q&A Dataset Builder")
mode = input("Choose mode - (v) Voice or (t) Text? [v]: ").strip().lower()
if mode not in ["v", "t"]:
    mode = "v"

while True:
    q, a = get_input_pair(mode)
    store_pair(q, a)

    again = input("➕ Add another? (y/n): ").strip().lower()
    if again != "y":
        break

conn.close()
