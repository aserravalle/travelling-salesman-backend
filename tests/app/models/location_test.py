from datetime import timedelta
from app.models.location import Location
import pytest


def test_travel_time_to():
    loc_a = Location(34.0522, -118.2437)
    loc_b = Location(34.0000, -118.2500)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=35), "Locations are close to each other"

    loc_a = Location(34.0522, -118.2437)
    loc_b = Location(35.0522, -119.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=864), "Locations are progressively more distant 1"

    loc_b = Location(36.0522, -120.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(
        days=1, seconds=17040
    ), "Locations are progressively more distant 2"

    loc_b = Location(37.0522, -121.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(
        days=1, seconds=68340
    ), "Locations are progressively more distant 3"


def test_travel_time_to_same():
    loc_a = Location(34.0522, -118.2437)
    loc_b = Location(34.0522, -118.2437)
    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=0), "Locations are the same"


def test_travel_time_to_invalid():
    # Test case: Invalid locations (latitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(91.0000, -118.2437)
        loc_b = Location(34.0522, -118.2437)
        loc_a.travel_time_to(loc_b)

    # Test case: Invalid locations (longitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(34.0522, -181.0000)
        loc_b = Location(34.0522, -118.2437)
        loc_a.travel_time_to(loc_b)

    # Test case: Invalid locations (both latitude and longitude out of range)
    with pytest.raises(ValueError):
        loc_a = Location(91.0000, -181.0000)
        loc_b = Location(34.0522, -118.2437)
        loc_a.travel_time_to(loc_b)
