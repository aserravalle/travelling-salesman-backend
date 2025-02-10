from datetime import timedelta
from typing import NamedTuple, Tuple


class Location(NamedTuple):
    latitude: float
    longitude: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

    def travel_time_to(self, other: "Location") -> timedelta:
        # TODO euclidian distance algorithm for determining rough distance between these points.
        return timedelta(minutes=30)
