# main.py
from api import api
from data import data_loader
from api import rag
from services import recommendation_service

def main():
    # 1. Fetch and store restaurant data (if needed)
    gt_location = (33.7756, -84.3963)  # Example: Georgia Tech location
    api.fetch_and_store_restaurants(gt_location, N=30, keyword='korean')  # Fetch data and store to csv

    # 2. Load restaurant data
    df = data_loader.load_restaurants_from_csv()
    if df is None:
        print("Error: Could not load restaurant data.")
        return

    # 3. Create FAISS index and add vectors
    index = rag.create_index_and_add_vectors(df)

    # 4. User query
    query = "best korean bbq with good service and fresh meat"

    # 5. Search for restaurants
    distances, indices = rag.search_restaurants(index, query, k=10)

    # 6. Get the restaurant information
    results = rag.get_restaurant_info(df, indices)

    # 7. Reorder the results based on user preferences (example)
    user_preferences = {"cuisine": "Korean", "price_range": "moderate", "rating": 4.0}  # Example preferences
    reordered_results = recommendation_service.reorder_results(results, user_preferences)

    # 8. Output the results
    print(f"Top 10 restaurants for query: \"{query}\"\n")
    for i, row in enumerate(reordered_results):
        print(f"{i+1}. {row['Name']} (Rating: {row['Rating']}, Address: {row['Address']})")
        print(f"   Sample Review: {row['Review 1'][:150]}...\n")

if __name__ == "__main__":
    main()