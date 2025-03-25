# api/rag.py
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from models import embedding_model
from models import vector_store
from data import data_loader

def create_index_and_add_vectors(df):
    """
    Creates the FAISS index and adds restaurant vectors.

    Args:
        df (pd.DataFrame): DataFrame containing restaurant data.

    Returns:
        faiss.Index: The FAISS index.
    """

    restaurant_texts = data_loader.combine_text(df)  # Use data_loader function

    #pre-process the restaurant information:
    # 3. Load embedding model
    model = embedding_model.load_model()

    # 4. Generate restaurant vectors
    restaurant_vectors = model.encode(restaurant_texts, normalize_embeddings=True)

    # 5. Build FAISS index
    dimension = restaurant_vectors.shape[1]
    index = vector_store.create_index(dimension)
    vector_store.add_vectors_to_index(index, restaurant_vectors)
    return index

def search_restaurants(index, query, k=5):
    """
    Searches for the top K restaurants based on the query.

    Args:
        index (faiss.Index): The FAISS index.
        query (str): The user query.
        k (int): Number of restaurants to retrieve.

    Returns:
        list: A list of tuples containing (distance, restaurant row).
    """
    model = embedding_model.load_model()
    # query = clean_text(query)
    query_vector = model.encode([query], normalize_embeddings=True)
    distances, indices = index.search(np.array(query_vector), k)

    return distances, indices
    # results = []
    # for i, idx in enumerate(indices[0]):
    #     row = df.iloc[idx]
    #     results.append((distances[0][i], row))
    # return results

def get_restaurant_info(df, indices):
    """
    Return restaurant information
    """
    results = []
    for i, idx in enumerate(indices[0]):
        row = df.iloc[idx]
        results.append(row)
    return results

# Example usage (moved to main.py)

