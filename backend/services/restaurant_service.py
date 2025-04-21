# services/restaurant_service.py

import pandas as pd
# from models.vector_store import VectorStore
# from services.google_maps_service import GoogleMapsService
import nltk

from utils.text_processing import clean_text, punkt_tokenizer


class RestaurantService:
    def __init__(self, row):
        self.row = row
        reviews = " ".join(str(row[f"Review {i}"]) for i in range(1, 4) if pd.notnull(row[f"Review {i}"]))
        self.info = f"{row['Name']}. Rating: {row['Rating']}. Address: {row['Address']}. Phone: {row['Phone']}. Reviews: {reviews}. Google Maps URL: {row['Google Maps URL']}"
        self.url = row['Google Maps URL']
        # self.embedding_model = EmbeddingModel()
        # self.vector_store = None

    def combine_text_chunks(self, min_words=3, max_char_length=2000):
        """
        split and clean the reviews to multiple chunks, and get it combined to become metadata
        拼接所有 reviews → 清洗 → 句子切割 → chunking,不拼接 meta data
        Args:
            row: one row of DataFrame 
            min_words: smallest number of word in one chunk 最少包含的词数
            max_char_length: one chunk maximum length(prevent the chunk is too large to embedded)

        Returns:
            List[str]: a list of chunk. 拼接好的 chunk 列表，每个 chunk 是独立的一段文字。
        """
        # 1. combined all the reviews
        review_number = 3
        all_reviews = " ".join(
            str(self.row[f"Review {i}"]) for i in range(1, review_number+1) if pd.notnull(self.row.get(f"Review {i}"))
        )

        # 2. clean
        cleaned = clean_text(all_reviews)

        # 3. tokenize
        sentences = punkt_tokenizer.tokenize(cleaned)

        # 4. Chunking
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_char_length:
                current_chunk += " " + sentence
            else:
                if len(current_chunk.split()) >= min_words:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        # last one
        if len(current_chunk.split()) >= min_words:
            chunks.append(current_chunk.strip())

        return chunks # lists of chunks that belongs to one restaurant



    # def prepare_vector_store(self):
    #     texts = self.df.apply(self.combine_text, axis=1).tolist()
    #     vectors = self.embedding_model.encode(texts)
    #     self.vector_store = VectorStore(vectors.shape[1])
    #     self.vector_store.add_vectors(vectors)

    # def search_restaurants(self, query: str, k: int = 5):
    #     query_vector = self.embedding_model.encode([query])[0]
    #     distances, indices = self.vector_store.search(query_vector, k)
    #     return [self.df.iloc[idx] for idx in indices[0]]

    # def fetch_and_update_restaurants(self, location: str, radius: int = 1000):
    #     new_restaurants = self.google_maps_service.fetch_restaurant_data(location, radius)
    #     # Here you would update self.df with the new data
    #     # For simplicity, let's assume we're just replacing the data
    #     self.df = pd.DataFrame(new_restaurants)
    #     self.prepare_vector_store()
