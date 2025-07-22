# batch_generate_tts.py
import os, hashlib
from gtts import gTTS
from vector_index import chunk_list

tts_dir = "tts_audio"
os.makedirs(tts_dir, exist_ok=True)

for text in chunk_list:
    filename = hashlib.md5(text.encode('utf-8')).hexdigest() + ".mp3"
    path = os.path.join(tts_dir, filename)
    if not os.path.exists(path):
        tts = gTTS(text, lang="ur")
        tts.save(path)
        print(f"✅ Saved: {path}")
    else:
        print(f"🔁 Skipped (exists): {path}")
