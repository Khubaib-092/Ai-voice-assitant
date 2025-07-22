import os
import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from django.conf import settings
from fuzzywuzzy import fuzz  

# Load multilingual sentence transformer
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Globals
faiss_index = None
questions = []
audio_paths = []

def load_faiss_from_db():
    global faiss_index, questions, audio_paths

    db_path = os.path.join(settings.BASE_DIR, "voice_dataset.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer_audio_path FROM qa_pairs")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise ValueError("❌ No data in qa_pairs table.")

    questions = [row[0] for row in rows]
    audio_paths = [row[1] for row in rows]

    # Embed all questions
    embeddings = model.encode(questions)
    embeddings = np.array(embeddings).astype("float32")

    # Build FAISS index
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)

# Load once at module import
load_faiss_from_db()

def search_faiss(query):

    conn = sqlite3.connect("voice_dataset.db")
    c = conn.cursor()
    c.execute("SELECT question, answer_audio_path FROM qa_pairs")
    data = c.fetchall()
    conn.close()

    best_match = None
    best_score = 0
    best_audio_path = None

    for question, audio_path in data:
        score = fuzz.ratio(query, question)
        print(f"🧪 Comparing to: {question} | Fuzzy Score: {score}")
        if score > best_score:
            best_score = score
            best_match = question
            best_audio_path = audio_path

    print(f"✅ Best matched question: {best_match}")
    print(f"📁 Matched audio path: {best_audio_path}")
    
    return best_match, best_audio_path   # 🔥 FIXED: returns 2 values
    global faiss_index, audio_paths, questions

    # Embed the incoming query
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search top 3 matches in FAISS
    distances, indices = faiss_index.search(query_embedding, k=3)

    # Fuzzy match on top 3 results
    best_score = 0
    best_idx = indices[0][0]  # fallback

    for i in range(3):
        idx = indices[0][i]
        candidate_question = questions[idx]
        score = fuzz.partial_ratio(query, candidate_question)
        print(f"🧪 Comparing to: {candidate_question} | Fuzzy Score: {score}")
        if score > best_score:
            best_score = score
            best_idx = idx

    matched_audio_path = audio_paths[best_idx]
    matched_question = questions[best_idx]

    # Logs for debugging
    print(f"🔍 Input query: {query}")
    print(f"✅ Best matched question: {matched_question}")
    print(f"📁 Matched audio path: {matched_audio_path}")

    return best_question, matched_audio_path

