# services/google_maps_service.py
import requests
import os
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_nearest_restaurants(location, N=10, keyword=None):
    """
    Retrieve the nearest N restaurants with error handling.

    Parameters:
    - location: (latitude, longitude) tuple representing the search center.
    - N: Number of restaurants to retrieve.
    - keyword: Search keyword (e.g., "korean", "japanese"). If None, retrieves all restaurants.

    Returns:
    - A list of restaurant details, or an empty list if the request fails.
    """

    NEARBYSEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    latitude, longitude = location
    restaurants = []
    next_page_token = None

    while len(restaurants) < N:
        try:
            params = {
                "location": f"{latitude},{longitude}",
                "type": "restaurant",
                "rankby": "distance",
                "key": GOOGLE_API_KEY
            }
            if keyword:
                params["keyword"] = keyword
            if next_page_token:
                params["pagetoken"] = next_page_token

            response = requests.get(NEARBYSEARCH_URL, params=params)
            data = response.json()

            if "results" in data:
                restaurants.extend(data["results"])
            if "next_page_token" in data:
                next_page_token = data["next_page_token"]
                time.sleep(2)
            else:
                break
        except requests.exceptions.Timeout:
            print("Error: API request timed out.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error: API request failed - {e}")
            break
        except KeyError as e:
            print(f"Error: Missing key in API response - {e}")
            break
    
    return restaurants[:N]

def get_restaurant_details(place_id):
    """
    Retrieve detailed restaurant information using Google Places Details API.

    Parameters:
    - place_id: Unique Place ID from Google Places API.

    Returns:
    - A dictionary containing restaurant details, or None if the request fails.
    """
    DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    try:
        params = {
            "place_id": place_id,
            "fields": "name,rating,formatted_address,formatted_phone_number,opening_hours,reviews",
            "key": GOOGLE_API_KEY
        }

        response = requests.get(DETAILS_URL, params=params)
        data = response.json()

        if "result" in data:
            return data["result"]
        else:
            print(f"Warning: No 'result' field for place_id {place_id}.")
            return None

    except requests.exceptions.Timeout:
        print(f"Error: Timeout while fetching details for place_id {place_id}.")
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed for place_id {place_id} - {e}")
    except KeyError as e:
        print(f"Error: Missing key in API response - {e}")
    return None
