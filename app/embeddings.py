from sentence_transformers import SentenceTransformer
import numpy as np

# Recommended multilingual model (lightweight & compatible)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def embed_text(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)
