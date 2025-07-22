from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Load FAISS index
index_path = "app/index/faiss_index.index"
assert os.path.exists(index_path), f"FAISS index not found at {index_path}"
index = faiss.read_index(index_path)

# Load answer list
with open("app/index/documents.pkl", "rb") as f:
    documents = pickle.load(f)  # List of answers

# Embedding helper
def embed(text: str):
    return model.encode([text])[0].astype("float32")

# Search function
def search_documents(query: str, top_k=1):
    query_vector = embed(query).reshape(1, -1)
    D, I = index.search(query_vector, top_k)

    # Filter invalid results
    results = []
    for i in I[0]:
        if i != -1 and i < len(documents):
            results.append(documents[i])
    return results
