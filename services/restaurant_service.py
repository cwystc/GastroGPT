# services/restaurant_service.py

import pandas as pd
from models.embedding_model import EmbeddingModel
from models.vector_store import VectorStore
from services.google_maps_service import GoogleMapsService
from utils.text_processing import clean_text


class RestaurantService:
    def __init__(self, file_path: str, google_maps_api_key: str):
        self.df = pd.read_csv(file_path)
        self.embedding_model = EmbeddingModel()
        self.vector_store = None
        self.google_maps_service = GoogleMapsService(google_maps_api_key)

    from utils.text_processing import clean_text

    def combine_text_chunks(row, min_words=3, max_char_length=300):
        """
        split and clean the reviews to multiple chunks, and get it combined to become metadata

        Args:
            row: one row of DataFrame 
            min_words: smallest number of word in one chunk 最少包含的词数
            max_char_length: 单个 chunk 最多字符数（防止过长）

        Returns:
            List[str]: 拼接好的 chunk 列表，每个 chunk 是独立的一段文字。
        """
        chunks_list = []

        for i in range(1, 4): #from review1 to review3
            
            review = row.get(f"Review {i}")
            if pd.notnull(review):
                cleaned = clean_text(str(review))

                # # 按句子拆也可以按逻辑拆分也可以跳过这里直接处理
                words = cleaned.split()
                if len(words) < min_words:
                    continue  # 跳过太短的

                # 按 max_char_length 拆 review 成多个 chunk
                
                for j in range(0, len(cleaned), max_char_length):
                    review_chunk = cleaned[j:j + max_char_length]
                    if len(review_chunk.split()) >= min_words:
                        
                        chunks_list.append(review_chunk)

        return chunks_list


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
