from datetime import timedelta
from app.models.location import Location
import pytest
import random


def test_location_creation_with_coordinates():
    # Test valid coordinates
    loc = Location(latitude=34.0522, longitude=-118.2437)
    assert loc.latitude == 34.0522
    assert loc.longitude == -118.2437
    assert loc.address is None

    # Test with address alongside coordinates
    loc = Location(latitude=34.0522, longitude=-118.2437, address="123 Main St")
    assert loc.latitude == 34.0522
    assert loc.longitude == -118.2437
    assert loc.address == "123 Main St"


def test_location_creation_with_address():
    loc = Location(address="Piazza del Colosseo, 1, 00184 Roma RM, Italy")
    assert loc.latitude == 41.8916
    assert loc.longitude == 12.4928
    assert loc.address == "1, Piazza del Colosseo, Monti, Municipio Roma I, Roma, Roma Capitale, Lazio, 00184, Italia"


def test_location_validation():
    # Test missing both coordinates and address
    with pytest.raises(ValueError, match="Either coordinates or address must be provided"):
        Location()

    # Test missing one coordinate
    with pytest.raises(ValueError, match="Either coordinates or address must be provided"):
        Location(latitude=34.0522)

    with pytest.raises(ValueError, match="Either coordinates or address must be provided"):
        Location(latitude=34.0522)

    # Test invalid latitude range
    with pytest.raises(ValueError):
        Location(latitude=91.0, longitude=-118.2437)

    # Test invalid longitude range
    with pytest.raises(ValueError):
        Location(latitude=34.0522, longitude=-181.0)


def test_should_never_have_microseconds():
    lat_a, lon_a = random.uniform(-90, 90), random.uniform(-180, 180)
    lat_b, lon_b = random.uniform(-90, 90), random.uniform(-180, 180)
    loc_a = Location(latitude=lat_a, longitude=lon_a)
    loc_b = Location(latitude=lat_b, longitude=lon_b)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time.microseconds == 0, f"Travel time should not have microseconds but did for values: [{loc_a}, {loc_a}]"


def test_travel_time_to():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=34.0000, longitude=-118.2500)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(seconds=4200), "Locations are close to each other"

def test_travel_time_to_1():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=35.0522, longitude=-119.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(days=1, seconds=17340), "Locations are progressively more distant 1"

def test_travel_time_to_2():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=36.0522, longitude=-120.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(days=2, seconds=34140), "Locations are progressively more distant 2"

def test_travel_time_to_3():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=37.0522, longitude=-121.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(days=3, seconds=50400), "Locations are progressively more distant 3"


def test_travel_time_to_same():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=34.0522, longitude=-118.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=5), "Locations are the same"


def test_travel_time_to_invalid():
    # Test case: Invalid locations (latitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(latitude=91.0000, longitude=-118.2437)
        loc_b = Location(latitude=34.0522, longitude=-118.2437)
        loc_a.travel_time_to(loc_b)

    # Test case: Invalid locations (longitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(latitude=34.0522, longitude=-181.0000)
        loc_b = Location(latitude=34.0522, longitude=-118.2437)
        loc_a.travel_time_to(loc_b)

    # Test case: Invalid locations (both latitude and longitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(latitude=91.0000, longitude=-181.0000)
        loc_b = Location(latitude=34.0522, longitude=-118.2437)
        loc_a.travel_time_to(loc_b)
