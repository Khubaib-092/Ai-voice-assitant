from faster_whisper import WhisperModel
import openai
from gtts import gTTS
import playsound

# 1. Load model (you can use "tiny", "base", "small", "medium")
model = WhisperModel("small", compute_type="int8")

# 2. Transcribe Urdu audio
def transcribe_audio(audio_path):
    try:
        # Important: use language="ur" for Urdu transcription
        segments, info = model.transcribe(audio_path, language="ur")
        print(f"🎛 Duration: {info.duration:.2f}s, Detected language: {info.language}")

        full_text = ""
        for segment in segments:
            full_text += segment.text.strip() + " "

        print("📜 Transcription:", full_text.strip())
        return full_text.strip()
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return ""

# 3. Generate reply from OpenRouter (text → text)
def generate_reply(user_text):  
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = "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"  # Replace with your OpenRouter API key

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who replies in Urdu."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        print("💬 Assistant:", reply)
        return reply
    except Exception as e:
        print(f"❌ Error generating reply: {e}")
        return "معاف کیجیے، میں اس وقت جواب نہیں دے سکا۔"

# 4. Convert reply to speech
def speak_reply(reply_text):
    try:
        tts = gTTS(text=reply_text, lang="ur")
        tts.save("reply.wav")
        playsound.playsound("reply.wav")
    except Exception as e:
        print(f"❌ Error in TTS: {e}")

# 5. Full pipeline
if __name__ == "__main__":
    audio_path = "your_urdu_audio.wav"  # Make sure this file exists
    user_text = transcribe_audio(audio_path)
    if user_text:
        reply = generate_reply(user_text)
        speak_reply(reply)
