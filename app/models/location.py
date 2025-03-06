from datetime import timedelta
from typing import NamedTuple, Tuple
from math import radians, sin, cos, sqrt, atan2

class Location(NamedTuple):
    """Represents a geographical location using latitude and longitude coordinates."""
    latitude: float
    longitude: float

    def to_tuple(self) -> Tuple[float, float]:
        """Convert location to a tuple of (latitude, longitude)."""
        return (self.latitude, self.longitude)

    def travel_time_to(self, other: "Location") -> timedelta:
        """
        Calculate travel time between two locations using Haversine formula.
        Returns a rough estimate based on straight-line distance.
        
        Args:
            other: Destination location
            
        Returns:
            Estimated travel time as timedelta
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        kmph = 10 # Assume walking speed of 10kmph
        hours = distance / kmph
        minutes = int(hours * 60)
        
        return timedelta(minutes=minutes)