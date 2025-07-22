import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ✅ Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# 📦 Load Urdu+English Q&A from database
db_path = os.path.join(base_dir, "voice_dataset.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT question FROM qa_pairs")
questions = [row[0] for row in cursor.fetchall()]
conn.close()

# 🤖 Encode questions
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(questions).astype("float32")

# 🧠 Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 💾 Save index to disk
index_dir = os.path.join(base_dir, "app", "index")
os.makedirs(index_dir, exist_ok=True)
index_path = os.path.join(index_dir, "faiss_index.index")
faiss.write_index(index, index_path)

print(f"✅ Rebuilt FAISS index with {len(questions)} entries.")
