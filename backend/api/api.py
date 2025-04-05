# api/api.py
from services import google_maps_service
from data import data_loader
import pandas as pd

def fetch_and_store_restaurants(location, N=10, keyword=None, filename="data/restaurants.csv"):
    """
    Fetches restaurant data from Google Maps API and stores it in a CSV file.

    Args:
        location (tuple): (latitude, longitude) tuple.
        N (int): Number of restaurants to fetch.
        keyword (str): Keyword to filter restaurants (e.g., "korean").
        filename (str): Path to the CSV file to store the data.
    """
    # location = (33.7756, -84.3963)
    nearest_restaurants = google_maps_service.get_nearest_restaurants(location, N, keyword)

    restaurants_data = []
    for restaurant in nearest_restaurants:
        place_id = restaurant["place_id"]
        details = google_maps_service.get_restaurant_details(place_id)

        if details:
            restaurants_data.append({
                "Name": details["name"],
                "Rating": details["rating"],
                "Address": details["formatted_address"],
                "Phone": details.get("formatted_phone_number", "N/A"),
                "Review 1": details.get("reviews", [{}])[0].get("text", "") if details.get("reviews") else "",
                "Review 2": details.get("reviews", [{}])[1].get("text", "") if len(details.get("reviews", [])) > 1 else "",
                "Review 3": details.get("reviews", [{}])[2].get("text", "") if len(details.get("reviews", [])) > 2 else ""
            })

    df = pd.DataFrame(restaurants_data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"Data saved to `{filename}` successfully")


if __name__ == '__main__':
    gt_location = (33.7756, -84.3963)  # Example: Georgia Tech location
    fetch_and_store_restaurants(gt_location, N=30, keyword='korean')
