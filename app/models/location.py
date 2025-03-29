from datetime import timedelta
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from math import radians, sin, cos, sqrt, atan2


def get_coordinates_from_address(address: str) -> tuple[float, float]:
    """
    Placeholder function to get coordinates from address.
    To be implemented with geocoding service.
    """
    return (39.473800, -0.375600) # Valencia, Spain


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

        # If either coordinate is missing ensure both are missing
        if self.latitude is None or self.longitude is None:
            self.latitude = None
            self.longitude = None

            # If no coordinates but address is present, generate coordinates
            if self.address is not None:
                self.latitude, self.longitude = get_coordinates_from_address(self.address)
            else:
                raise ValueError("Either coordinates or address must be provided")
        

        return self
    
    def is_same_location_as(self, other: 'Location') -> bool:
        return (self.address is not None and self.address == other.address) or (
            self.latitude == other.latitude and self.longitude == other.longitude
            )


    def travel_time_to(self, other: 'Location') -> timedelta:
        """
        Calculate travel time between two locations
        Args:
            other: Destination location

        Returns:
            Estimated travel time as timedelta
        """
        if self.is_same_location_as(other):
            return timedelta(minutes=0)

        return timedelta(minutes=20)