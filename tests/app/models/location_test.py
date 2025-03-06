from datetime import timedelta
from app.models.location import Location


def test_travel_time_to():
    loc_a = Location(34.0522, -118.2437)
    loc_b = Location(34.0000, -118.2500)

    travel_time = loc_a.travel_time_to(loc_b)
    assert travel_time == timedelta(minutes=35)
