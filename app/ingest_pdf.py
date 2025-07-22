
import os
import sys

import faiss
import numpy as np
from PyPDF2 import PdfReader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.embeddings import embed_text

PDF_DIR = os.path.join(os.path.dirname(__file__), "documents")
INDEX_PATH = "document_index.faiss"
CHUNKS_PATH = "text_chunks.txt"
CHUNK_SIZE = 500  # Adjust based on your documents

def clean_text(text):
    return ' '.join(text.replace('\n', ' ').split())

def load_pdfs(pdf_dir):
    all_text = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            reader = PdfReader(path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
            all_text.append(clean_text(full_text))
    return all_text

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def build_faiss_index(chunks):
    embeddings = np.array([embed_text(c) for c in chunks])
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_chunks(chunks, path=CHUNKS_PATH):
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.strip() + "\n")

def main():
    print("🔍 Loading PDFs...")
    pdf_texts = load_pdfs(PDF_DIR)
    
    print("📦 Chunking text...")
    all_chunks = []
    for text in pdf_texts:
        all_chunks.extend(chunk_text(text))

    print(f"🧠 Generating embeddings for {len(all_chunks)} chunks...")
    index = build_faiss_index(all_chunks)

    print("💾 Saving FAISS index and text chunks...")
    faiss.write_index(index, INDEX_PATH)
    save_chunks(all_chunks)

    print("✅ PDF ingestion completed successfully.")

if __name__ == "__main__":
    main()
