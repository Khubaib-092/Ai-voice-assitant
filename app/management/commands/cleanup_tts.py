from django.core.management.base import BaseCommand
import os
import sqlite3
from django.conf import settings

class Command(BaseCommand):
    help = 'Clean up unused TTS audio files.'

    def handle(self, *args, **kwargs):
        db_path = os.path.join(settings.BASE_DIR, "voice_dataset.db")
        audio_dir = os.path.join(settings.BASE_DIR, "tts_audio")

        # Get all audio paths from DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT answer_audio_path FROM qa_pairs")
        used_paths = set(row[0] for row in cursor.fetchall())
        conn.close()

        # Check all .mp3 in tts_audio/
        for filename in os.listdir(audio_dir):
            full_path = os.path.join(audio_dir, filename)
            relative_path = os.path.join("tts_audio", filename)

            if filename.endswith(".mp3") and relative_path not in used_paths:
                os.remove(full_path)
                print(f"🧹 Deleted unused: {relative_path}")
