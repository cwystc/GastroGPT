import requests
from requests.exceptions import RequestException
import time
import backoff  # For exponential backoff

class GoogleMapsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GastroGPT/1.0',
            'Accept': 'application/json'
        })

    @backoff.on_exception(backoff.expo, RequestException, max_tries=3)
    def _make_request(self, endpoint, params):
        """Generic method to make API requests with error handling"""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            if response.status_code == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                return self._make_request(endpoint, params)
                
            return response.json()
            
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise ValueError("Invalid API key")
            elif response.status_code == 404:
                raise ValueError(f"Resource not found: {endpoint}")
            raise http_err
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to Google Maps API")
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get_nearest_restaurants(self, location, N=10, keyword=None):
        """Enhanced version with proper error handling"""
        latitude, longitude = location
        restaurants = []
        next_page_token = None
        
        while len(restaurants) < N:
            params = {
                "location": f"{latitude},{longitude}",
                "type": "restaurant",
                "rankby": "distance",
                "key": self.api_key
            }
            if keyword:
                params["keyword"] = keyword
            if next_page_token:
                params["pagetoken"] = next_page_token

            try:
                data = self._make_request("place/nearbysearch/json", params)
                if "error_message" in data:
                    raise ValueError(f"API Error: {data['error_message']}")
                    
                if "results" in data:
                    restaurants.extend(data["results"])
                next_page_token = data.get("next_page_token")
                if not next_page_token:
                    break
                    
                time.sleep(2)  # Respect API rate limits
                
            except Exception as e:
                logger.error(f"Failed to fetch restaurants: {str(e)}")
                break

        return restaurants[:N]