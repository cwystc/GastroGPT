# data/data_loader.py
import pandas as pd

def load_restaurants_from_csv(filename="data/restaurants.csv"):
    """
    Loads restaurant data from a CSV file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the restaurant data.
    """
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return None

def combine_text(df):
    """
    Combines the text information for each restaurant into a single string.

    Args:
        df (pd.DataFrame): DataFrame containing restaurant data.

    Returns:
        list: A list of combined text strings for each restaurant.
    """
    restaurant_texts = []
    for index, row in df.iterrows():
        reviews = " ".join(str(row[f"Review {i}"]) for i in range(1, 4) if pd.notnull(row[f"Review {i}"]))
        text = f"{row['Name']}. Rating: {row['Rating']}. Address: {row['Address']}. Phone: {row['Phone']}. Reviews: {reviews}"
        restaurant_texts.append(text)
    return restaurant_texts

# Example usage (moved to main.py)

