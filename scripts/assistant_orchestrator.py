# scripts/assistant_orchestrator.py
from test_transcribe import transcribe_audio
from document_search import search_faiss
from generate_tts import text_to_speech

AUDIO_FILE = "your_urdu_audio.wav"

print("🎙️ Step 1: Transcribing...")
query = transcribe_audio(AUDIO_FILE)
print("📜 You said:", query)

if not query.strip():
    print("⚠️ Transcription is empty. Skipping search and TTS.")
    exit()

answer = search_faiss(query)
print("📚 Assistant reply:", answer)

if not answer.strip():
    print("⚠️ No valid reply. Skipping TTS.")
    exit()

text_to_speech(answer)
print("✅ Reply ready in reply.wav")