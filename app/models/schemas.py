from pydantic import BaseModel, Field
from typing import List


class Job(BaseModel):
    property_id: int
    duration: int  # Minutes
    time_window: str  # "ENTRADA"/"SALIDA"


class Cleaner(BaseModel):
    cleaner_id: int
    name: str
    hours_available: int
    home_address: str  # Could store coordinates


class ScheduleRequest(BaseModel):
    jobs: List[Job] = Field(min_length=1)  # At least one job required
    cleaners: List[Cleaner] = Field(min_length=1)  # At least one cleaner required
