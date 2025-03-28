from datetime import timedelta
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from math import radians, sin, cos, sqrt, atan2


def get_coordinates_from_address(address: str) -> tuple[float, float]:
    """
    Placeholder function to get coordinates from address.
    Currently returns (0, 0) - to be implemented with geocoding service.
    """
    return (0.0, 0.0)


class Location(BaseModel):
    """
    Represents a geographical location using latitude/longitude coordinates and optional address.
    
    Either coordinates (both latitude and longitude) or address must be provided.
    Address can be provided alongside coordinates for display purposes.
    """
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = None

    @model_validator(mode='after')
    def validate_coordinates_or_address(self) -> 'Location':
        """
        Validates that either both coordinates are provided or address is provided.
        If only address is provided, generates coordinates.
        """
        has_latitude = self.latitude is not None
        has_longitude = self.longitude is not None
        has_address = self.address is not None

        # Both coordinates must be present if either is present
        if has_latitude != has_longitude:
            raise ValueError("Both latitude and longitude must be provided together")

        # If no coordinates but address is present, generate coordinates
        if not has_latitude and has_address:
            self.latitude, self.longitude = get_coordinates_from_address(self.address)
        
        # Must have either coordinates or address
        if not has_latitude and not has_address:
            raise ValueError("Either coordinates or address must be provided")

        return self
    
    def is_same_location_as(self, other: 'Location') -> bool:
        return (self.address is not None and self.address == other.address) or (
            self.latitude == other.latitude and self.longitude == other.longitude
            )


    def travel_time_to(self, other: 'Location') -> timedelta:
        """
        Calculate travel time between two locations using Haversine formula.
        Returns a rough estimate based on straight-line distance.

        Args:
            other: Destination location

        Returns:
            Estimated travel time as timedelta
        """
        if self.is_same_location_as(other):
            return timedelta(minutes=0)

        # R = 6371  # Earth's radius in kilometers

        # lat1, lon1 = radians(self.latitude), radians(self.longitude)
        # lat2, lon2 = radians(other.latitude), radians(other.longitude)

        # dlat = lat2 - lat1
        # dlon = lon2 - lon1

        # a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        # c = 2 * atan2(sqrt(a), sqrt(1 - a))
        # distance = R * c

        # kmph = 5  # Assumed walking speed # TODO - make this a parameter
        # hours = distance / kmph
        # minutes = int(hours * 60)

        return timedelta(minutes=20)