# services/restaurant_service.py

import pandas as pd
from models.embedding_model import EmbeddingModel
from models.vector_store import VectorStore
from services.google_maps_service import GoogleMapsService

class RestaurantService:
    def __init__(self, file_path: str, google_maps_api_key: str):
        self.df = pd.read_csv(file_path)
        self.embedding_model = EmbeddingModel()
        self.vector_store = None
        self.google_maps_service = GoogleMapsService(google_maps_api_key)

    def combine_text(self, row):
        reviews = " ".join(str(row[f"Review {i}"]) for i in range(1, 4) if pd.notnull(row[f"Review {i}"]))
        text = f"{row['Name']}. Rating: {row['Rating']}. Address: {row['Address']}. Phone: {row['Phone']}. Reviews: {reviews}"
        return text

    def prepare_vector_store(self):
        texts = self.df.apply(self.combine_text, axis=1).tolist()
        vectors = self.embedding_model.encode(texts)
        self.vector_store = VectorStore(vectors.shape[1])
        self.vector_store.add_vectors(vectors)

    def search_restaurants(self, query: str, k: int = 5):
        query_vector = self.embedding_model.encode([query])[0]
        distances, indices = self.vector_store.search(query_vector, k)
        return [self.df.iloc[idx] for idx in indices[0]]

    def fetch_and_update_restaurants(self, location: str, radius: int = 1000):
        new_restaurants = self.google_maps_service.fetch_restaurant_data(location, radius)
        # Here you would update self.df with the new data
        # For simplicity, let's assume we're just replacing the data
        self.df = pd.DataFrame(new_restaurants)
        self.prepare_vector_store()
