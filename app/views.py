import tempfile
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .vector_index import search_faiss
import uuid
import subprocess
from io import BytesIO
import base64
import torch
import soundfile as sf
from langdetect import detect
from gtts import gTTS

# 🧠 Lazy-loaded models
qa_pipeline = None
processor = None
model = None
@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        filename = f"input_{uuid.uuid4().hex}.webm"
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(audio_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Convert .webm to .wav (16kHz mono)
        wav_filename = filename.replace(".webm", ".wav")
        wav_path = os.path.join(settings.MEDIA_ROOT, wav_filename)
        os.system(f'ffmpeg -y -i "{audio_path}" -ar 16000 -ac 1 "{wav_path}"')

        # Transcribe (adjust to your own transcriber)
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = r.record(source)
            try:
                query = r.recognize_google(audio_data, language='ur-PK')
            except:
                query = ""

        if query.strip():
            answer_text, answer_audio_path = search_faiss(query)

            rel_audio_path = os.path.relpath(answer_audio_path, settings.MEDIA_ROOT)
            return JsonResponse({'answer': answer_text, 'audio': rel_audio_path, 'query': query})
        else:
            return JsonResponse({'error': 'Could not recognize speech'}, status=400)

def load_models():
    global qa_pipeline, processor, model
    if qa_pipeline is None or processor is None or model is None:
        print("📦 Loading models...")
        from transformers import pipeline, Wav2Vec2ForCTC, Wav2Vec2Processor
        processor = Wav2Vec2Processor.from_pretrained("kingabzpro/wav2vec2-urdu")
        model = Wav2Vec2ForCTC.from_pretrained("kingabzpro/wav2vec2-urdu")
        qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")
        print("✅ Models loaded.")


def transcribe_urdu(path):
    audio, sr_val = sf.read(path)
    inputs = processor(audio, sampling_rate=sr_val, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    return processor.batch_decode(predicted_ids)[0]

def process_transcribed_text(user_query):
    try:
        lang = detect(user_query)
        print(f"Detected language: {lang}")

        if lang == "ur":
            from .vector_index import search_faiss
            audio_rel_path = search_faiss(user_query)
            return "🔊 Playing Urdu audio response...", audio_rel_path
        else:
            return "🔊 English audio not supported yet.", None

    except Exception as e:
        print("❌ Language detection failed:", e)
        return "معذرت، میں سمجھ نہیں سکی۔", None   

@csrf_exempt
def voice_query(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    audio_file = request.FILES.get("audio")
    if not audio_file:
        return JsonResponse({"error": "No audio file uploaded"}, status=400)

    try:
        load_models()

        # Save WebM audio temporarily
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_webm:
            for chunk in audio_file.chunks():
                tmp_webm.write(chunk)
            webm_path = tmp_webm.name

        # Convert to 16kHz WAV using ffmpeg
        wav_path = webm_path.replace(".webm", ".wav")
        subprocess.run(["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", wav_path], check=True)

        # Transcribe
        user_query = transcribe_urdu(wav_path)
        print(f"🎙️ User said: {user_query}")

        audio_rel_path = search_faiss(user_query)
        answer_text = "🔊 Playing audio response..."  # You can customize this text if needed


        print(f"🤖 FAISS Answer: {answer_text}")
        print(f"🔊 Audio path: {audio_rel_path}")

        # Load MP3 and convert to base64
        audio_full_path = os.path.join(settings.BASE_DIR, audio_rel_path)
        with open(audio_full_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        # Clean up
        os.unlink(webm_path)
        os.unlink(wav_path)

        return JsonResponse({
            "question": user_query,
            "answer": answer_text,
            "audio_base64": audio_base64
        })

    except Exception as e:
        print("❌ Error:", repr(e))
        return JsonResponse({"error": str(e)}, status=500)

def tts_audio(request):
    return JsonResponse({"error": "TTS route is unused in this setup"})

def speech_to_text(request):
    return JsonResponse({"error": "Not used in web version"})

def home(request):
    return render(request, "search_audio.html")

def index(request):
    return render(request, "app/index.html")

def query_audio(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    try:
        audio_path = search_faiss(query)
        relative_path = os.path.relpath(audio_path, settings.BASE_DIR)
        return JsonResponse({"audio": relative_path})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)