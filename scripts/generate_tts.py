# scripts/generate_tts.py

from gtts import gTTS
from pydub import AudioSegment
import os

def text_to_speech(text, mp3_file="reply.mp3", wav_file="reply.wav", lang="en"):
    # Convert text to mp3
    tts = gTTS(text=text, lang=lang)
    tts.save(mp3_file)
    print(f"✅ MP3 saved: {mp3_file}")

    # Convert mp3 to wav for Asterisk (if needed)
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")
    print(f"✅ WAV saved: {wav_file}")

# Example usage
if __name__ == "__main__":
    sample_text = "Hello, this is your AI assistant. How can I help you today?"
    text_to_speech(sample_text)
