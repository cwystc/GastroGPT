from services import google_maps_service
from api import rag
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from models import embedding_model
from models import vector_store
from data import data_loader
from services import restaurant_service

def fetch_and_create_index(location, N=10, keyword=None):
    if location is None:
        raise ValueError("The location cannot be empty when fetching!")
    nearest_restaurants = google_maps_service.get_nearest_restaurants(location, N, keyword)


    restaurants_data = []
    for restaurant in nearest_restaurants:
        place_id = restaurant["place_id"]
        details = google_maps_service.get_restaurant_details(place_id)

        if details:
            restaurants_data.append({
                "Name": details.get("name", "N/A"),
                "Rating": details.get("rating", "N/A"),
                "Address": details.get("formatted_address", "N/A"),
                "Phone": details.get("formatted_phone_number", "N/A"),
                "Review 1": details.get("reviews", [{}])[0].get("text", "") if details.get("reviews") else "",
                "Review 2": details.get("reviews", [{}])[1].get("text", "") if len(details.get("reviews", [])) > 1 else "",
                "Review 3": details.get("reviews", [{}])[2].get("text", "") if len(details.get("reviews", [])) > 2 else ""
            })


    df = pd.DataFrame(restaurants_data)


    print(f"Data fetched successfully")


    # 这里做preprocess和chunk

    chunks = []
    indexid_to_restaurant = []
    for index, row in df.iterrows():
        restaurant = restaurant_service.RestaurantService(row)
        list_of_chunks = restaurant.combine_text_chunks()

        # print(index, list_of_chunks)
        
        chunks.extend(list_of_chunks)

        for i in range(len(list_of_chunks)):
            indexid_to_restaurant.append(restaurant)
        # restaurants.append(restaurant)





    # 3. Load embedding model
    model = embedding_model.load_model()

    # 4. Generate restaurant vectors
    restaurant_vectors = model.encode(chunks, normalize_embeddings=True)

    # 5. Build FAISS index
    dimension = restaurant_vectors.shape[1]
    index = vector_store.create_index(dimension)

    # print(restaurant_vectors)

    vector_store.add_vectors_to_index(index, restaurant_vectors)

    return index, indexid_to_restaurant

