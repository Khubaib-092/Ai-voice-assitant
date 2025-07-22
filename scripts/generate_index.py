import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Get base dir as the parent of 'scripts', i.e., the 'assist' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHUNKS_FILE = os.path.join(BASE_DIR, "text_chunks.txt")  # <== correct location
INDEX_FILE = os.path.join(BASE_DIR, "document_index.faiss")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Read the text chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    texts = [chunk.strip() for chunk in content.split('---') if chunk.strip()]

# Embed the text chunks
embeddings = model.encode(texts, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index
faiss.write_index(index, INDEX_FILE)

print("✅ FAISS index created and saved to:", INDEX_FILE)
print("🧾 Loaded Chunks:")
for i, chunk in enumerate(texts):
    print(f"{i+1}: {chunk}")
