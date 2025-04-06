import os
import requests
import json

class LocationHelpers:
    cache_file_path = os.path.join(os.path.dirname(__file__), 'locationCache.json')
    locationCache = {}

    @staticmethod
    def load_coordinates(file_path=None):
        if file_path:
            LocationHelpers.cache_file_path = file_path
        try:
            with open(LocationHelpers.cache_file_path, 'r') as file:
                result = json.load(file)
                for key, value in result.items():
                    if LocationHelpers.is_valid_location(value):
                        LocationHelpers.locationCache[key] = value
                    else:
                        print(f"Invalid location data for {key}: {value}")
        except FileNotFoundError:
            print(f"Cache file not found: {LocationHelpers.cache_file_path}")
            LocationHelpers.locationCache = {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from cache file: {e}")
            LocationHelpers.locationCache = {}
        except Exception as e:
            print(f"Unexpected error while loading cache: {e}")
            LocationHelpers.locationCache = {}


    @staticmethod
    def get_coordinates_from_address(address: str) -> dict:
        """
        Get latitude, longitude (rounded to 4 decimals), and formatted address.
        Try getting it from cache first. If not valid, use OpenStreetMap's Nominatim API.
        """
        result = LocationHelpers.get_coordinates_from_cache(address)
        if not LocationHelpers.is_valid_location(result):
            result = LocationHelpers.get_coordinates_via_api(address)
            assert LocationHelpers.is_valid_location(result)
            LocationHelpers.add_result_to_cache(address, result)
        return result
    
    @staticmethod
    def add_result_to_cache(address: str, location: dict):
        """
        Add the result to the cache and save it to a JSON file.
        """
        LocationHelpers.locationCache[address] = location
        with open(LocationHelpers.cache_file_path, 'w') as file:
            json.dump(LocationHelpers.locationCache, file)

    
    @staticmethod
    def is_valid_location(location: dict) -> bool:
        """
        Check if the location dictionary contains valid data
        """
        return (
            isinstance(location, dict) and \
           all(key in location for key in ['address', 'latitude', 'longitude']) and \
           isinstance(location['address'], str) and \
           isinstance(location['latitude'], (int, float)) and \
           isinstance(location['longitude'], (int, float))
        )
        

    @staticmethod
    def get_coordinates_from_cache(rawAddress: str) -> dict:
        """
        Get coordinates from a JSON file cache.
        """
        try:
            result = LocationHelpers.locationCache[rawAddress]
            return result
        except KeyError:
            print(f"Coordinates for {rawAddress} not found in cache.")
            return None
        

    @staticmethod
    def get_coordinates_via_api(address: str) -> dict:
        """
        Get latitude, longitude (rounded to 4 decimals), and formatted address 
        from a partial address using OpenStreetMap's Nominatim API.
        Returns a dictionary with keys: 'latitude', 'longitude', 'address'.
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'addressdetails': 1,  # ask for extra details
            'limit': 1            # only top result
        }
        headers = {
            'User-Agent': 'TravellingSalesman/1.0 (magicchili1998@gmail.com)'  # Required
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data:
                result = data[0]
                return {
                    'latitude': round(float(result['lat']), 4),
                    'longitude': round(float(result['lon']), 4),
                    'address': result.get('display_name', '')
                }
            else:
                return {}
            
        except Exception as e:
            print(f"Error getting coordinates from API for {address}: {e}")
            raise e


# Load coordinates when the class is imported
LocationHelpers.load_coordinates()