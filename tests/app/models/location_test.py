from datetime import timedelta
from app.models.location import Location
import pytest


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
    assert loc.latitude == 41.8916  # Placeholder value
    assert loc.longitude == 12.4928  # Placeholder value
    assert loc.address == "1, Piazza del Colosseo, Monti, Municipio Roma I, Roma, Roma Capitale, Lazio, 00184, Italia"


def test_get_coordinates_from_address():
    coords = Location.get_coordinates_from_address(address="Piazza del Colosseo, 1, 00184 Roma RM, Italy")
    assert coords["latitude"] == 41.8916
    assert coords["longitude"] == 12.4928
    assert coords["address"] == "1, Piazza del Colosseo, Monti, Municipio Roma I, Roma, Roma Capitale, Lazio, 00184, Italia"


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


def test_travel_time_to():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=34.0000, longitude=-118.2500)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=20), "Locations are close to each other"

    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=35.0522, longitude=-119.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=20), "Locations are progressively more distant 1"

    loc_b = Location(latitude=36.0522, longitude=-120.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=20), "Locations are progressively more distant 2"

    loc_b = Location(latitude=37.0522, longitude=-121.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=20), "Locations are progressively more distant 3"


def test_travel_time_to_same():
    loc_a = Location(latitude=34.0522, longitude=-118.2437)
    loc_b = Location(latitude=34.0522, longitude=-118.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=20), "Locations are the same"


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
