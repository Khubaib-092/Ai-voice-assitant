from faster_whisper import WhisperModel
from gtts import gTTS
import playsound
import os 
import sys

# Add app directory to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
from app.nlp_pipeline import process_user_query  # your own document-based query processor

# Load Whisper model (already optimized)
model = WhisperModel("small", compute_type="int8")

def transcribe_audio(audio_path):
    try:
        segments, info = model.transcribe(audio_path, language="ur")
        print(f"Duration: {info.duration:.2f}s, Detected language: {info.language}")
        full_text = " ".join([segment.text.strip() for segment in segments])
        print("Transcription:", full_text)
        return full_text.strip()
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

def speak_reply(reply_text):
    try:
        tts = gTTS(text=reply_text, lang="ur")
        tts.save("reply.mp3")
        print("reply.mp3 exists?", os.path.exists("reply.mp3"), "Size:", os.path.getsize("reply.mp3"))
        playsound.playsound("reply.mp3")
    except Exception as e:
        print(f"Error in TTS: {e}")

if __name__ == "__main__":
    audio_path = "your_urdu_audio.wav"  # replace with real path or input
    user_text = transcribe_audio(audio_path)
    if user_text:
        reply = process_user_query(user_text)
        print("Assistant:", reply)
        speak_reply(reply)
