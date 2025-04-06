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

    def test_get_coordinates_from_address(self):
        self.set_test_cache({})
        assert LocationHelpers.locationCache == {}, "Pre assertion - empty cache"

        expected_result = {
            "Piazza del Colosseo, 1": {
                "latitude": 41.8916,
                "longitude": 12.4928,
                "address": "1, Piazza del Colosseo, Monti, Municipio Roma I, Roma, Roma Capitale, Lazio, 00184, Italia"
            }
        }

        result = LocationHelpers.get_coordinates_from_address("Piazza del Colosseo, 1")
        assert result == expected_result["Piazza del Colosseo, 1"]
        assert LocationHelpers.locationCache == expected_result, "New result should be added to cache"

        cacheResult = LocationHelpers.get_coordinates_from_cache("Piazza del Colosseo, 1")
        assert cacheResult == expected_result["Piazza del Colosseo, 1"]

        with open(self.test_file_path, 'r') as file:
            fileResult = json.load(file)
        assert fileResult == expected_result, "Cache file should be updated"

    def set_test_cache(self, test_data):
        # Create a valid JSON file
        with open(self.test_file_path, "w") as file:
            json.dump(test_data, file)

        # Call the method
        LocationHelpers.load_coordinates(self.test_file_path)