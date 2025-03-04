# models/vector_store.py
import faiss

def create_index(dimension):
    """Creates a FAISS index."""
    index = faiss.IndexFlatIP(dimension)  # Inner product index
    return index

def add_vectors_to_index(index, vectors):
    """Adds vectors to the FAISS index."""
    index.add(vectors)
