from api import rag
from data import data_loader

# Load your specific restaurants data
df = data_loader.load_restaurants_from_csv()
if df is None:
    print("Error: Could not load restaurant data.")
    exit(1)

# Create FAISS index and add vectors
index = rag.create_index_and_add_vectors(df)

while True:
    # Define your query
    query = input("Enter your query (or 'exit' to quit): ")
    if query.lower() == 'exit':
        break

    # Search for restaurants
    distances, indices = rag.search_restaurants(index, query, k=10)

    # Get the restaurant information
    results = rag.get_restaurant_info(df, indices)

    # Output the results without reordering
    print(f"Top 10 restaurants for query: \"{query}\"\n")
    for i, row in enumerate(results):
        print(f"{i+1}. {row['Name']} (Rating: {row['Rating']}, Address: {row['Address']})")
        print(f"   Sample Review: {row['Review 1'][:150]}...\n")

