import sounddevice as sd
import wave

# Settings
filename = "your_urdu_audio.wav"  # Output file
duration = 5  # seconds
samplerate = 16000  # Required by Vosk

print("🎙️ Recording... Speak now")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()
print("✅ Recording finished")

# Save as WAV
with wave.open(filename, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(samplerate)
    wf.writeframes(recording.tobytes())

print(f"🔉 Saved: {filename}")