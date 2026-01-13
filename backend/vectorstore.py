import faiss
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    # Convert embeddings to float32 numpy array (FAISS requirement)
    embeddings = model.encode(texts)
    return np.array(embeddings).astype("float32")

def save_index(vectors, metadatas):
    if len(vectors) == 0:
        raise ValueError("No vectors to index")

    dimension = vectors.shape[1]  # ✅ Correct way
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    os.makedirs("data/vector_db", exist_ok=True)

    faiss.write_index(index, "data/vector_db/index.faiss")

    with open("data/vector_db/meta.pkl", "wb") as f:
        pickle.dump(metadatas, f)

def load_index():
    index = faiss.read_index("data/vector_db/index.faiss")

    with open("data/vector_db/meta.pkl", "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
