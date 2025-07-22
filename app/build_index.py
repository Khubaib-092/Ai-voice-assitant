# run once to prepare the index (save as build_index.py)
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Example org documents
documents = [
    "ہماری کمپنی صارفین کو 24 گھنٹے کسٹمر سپورٹ فراہم کرتی ہے۔",
    "اگر آپ کو کوئی شکایت ہو تو ہمارے ہیلپ لائن نمبر پر رابطہ کریں۔",
    "ہم ہر جمعہ کو آفس بند رکھتے ہیں۔"
]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(documents).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "app/index/faiss_index.index")
with open("app/index/documents.pkl", "wb") as f:
    pickle.dump(documents, f)
