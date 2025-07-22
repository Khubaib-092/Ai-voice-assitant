import speech_recognition as sr
from langdetect import detect
from .vector_index import get_semantic_response_english, get_semantic_response_urdu


recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source, timeout=5)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)

def process_transcribed_text(user_query):
    try:
        lang = detect(user_query)
        print(f"Detected language: {lang}")

        if lang == 'ur':
            response = get_semantic_response_urdu(user_query)
        else:
            response = get_semantic_response_english(user_query)

        return response

    except Exception as e:
        print("Language detection failed:", e)
        return "Sorry, I couldn't understand that."