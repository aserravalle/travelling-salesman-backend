from datetime import timedelta
from app.models.location import Location


def test_travel_time_to():
    loc_a = Location(1, 2)
    loc_b = Location(3, 4)

    assert loc_a.travel_time_to(loc_b) == timedelta(minutes=30)
