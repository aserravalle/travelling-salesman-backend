import os
import json
from app.services.location_helpers import LocationHelpers


class TestLocationHelpers:
    def setup_method(self):
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'locationCache.json')
        LocationHelpers.cache_file_path = self.test_file_path
        LocationHelpers.locationCache = {}

        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)


    def teardown_method(self):
        # Teardown: Remove the file after tests
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_load_coordinates_valid_file(self):
        test_data = {"address1": {"latitude": 40.7128, "longitude": -74.0060, "address": "New York"}}
        self.set_test_cache(test_data)

        # Assert the cache is loaded correctly
        assert LocationHelpers.locationCache == test_data, "Cache should match the file content"

    def test_load_coordinates_file_not_found(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        LocationHelpers.load_coordinates(self.test_file_path)

        assert LocationHelpers.locationCache == {}, "Cache should be empty if file is not found"

    def test_load_coordinates_invalid_json(self):
        test_data = "{invalid_json: true}"
        self.set_test_cache(test_data)

        # Assert the cache is empty and a message is printed
        assert LocationHelpers.locationCache == {}, "Cache should be empty if JSON is invalid"

    def test_get_coordinates_from_cache(self):
        test_data = {"address1": {"latitude": 40.7128, "longitude": -74.0060, "address": "New York"}}
        self.set_test_cache(test_data)

        assert LocationHelpers.locationCache == test_data, "Cache should match the file content"
        result = LocationHelpers.get_coordinates_from_cache("address1")
        assert result == test_data["address1"], "Should return the cached coordinates for address1"

    def test_get_coordinates_from_cache_not_found(self):
        test_data = {"address1": {"latitude": 40.7128, "longitude": -74.0060, "address": "New York"}}
        self.set_test_cache(test_data)

        result = LocationHelpers.get_coordinates_from_cache("Piazza del Colosseo, 1")
        assert result is None, "Should return None for non-existent address in cache"

    def test_get_coordinates_from_address_italian(self):
        self.set_test_cache({})
        assert LocationHelpers.locationCache == {}, "Pre assertion - empty cache"

        expected_result = {
            "Piazza del Colosseo, 1": {
                "latitude": 41.8900,
                "longitude": 12.4943,
                "address": "Piazza del Colosseo, 1, 00184 Roma RM, Italy"
            }
        }
        rawAddress = next(iter(expected_result.keys()))

        self.assert_get_new_address_and_add_to_cache(expected_result, rawAddress)


    def test_get_coordinates_from_address_spanish(self):
        self.set_test_cache({})
        assert LocationHelpers.locationCache == {}, "Pre assertion - empty cache"

        expected_result = {
            "C/ MIGUEL SERVET, 18-8ª, VALENCIA, VALENCIA, ESPAÑA": {
                "latitude": 39.4874,
                "longitude": -0.3932,
                "address": "C/ de Miguel Servet, 18, Benicalap, 46015 València, Valencia, Spain"
            }
        }
        rawAddress = next(iter(expected_result.keys()))

        self.assert_get_new_address_and_add_to_cache(expected_result, rawAddress)

    def assert_get_new_address_and_add_to_cache(self, expected_result, rawAddress):
        result = LocationHelpers.get_coordinates_from_address(rawAddress)
        assert result == expected_result[rawAddress]
        assert LocationHelpers.locationCache.get(rawAddress, {}) == expected_result[rawAddress], "New result should be added to cache"

        cacheResult = LocationHelpers.get_coordinates_from_cache(rawAddress)
        assert cacheResult == expected_result[rawAddress]

        with open(self.test_file_path, 'r') as file:
            fileResult = json.load(file)
        assert fileResult[rawAddress] == expected_result[rawAddress], "Cache file should be updated"

    def set_test_cache(self, test_data):
        with open(self.test_file_path, "w") as file:
            json.dump(test_data, file)

        LocationHelpers.load_coordinates(self.test_file_path)
