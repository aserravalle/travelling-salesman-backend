from pydantic import BaseModel, Field
from datetime import datetime
from typing import Tuple, List


class Job(BaseModel):
    id: int
    location: Tuple[float, float]
    duration: int
    entry_time: datetime
    exit_time: datetime


class Salesman(BaseModel):
    id: int
    home_location: Tuple[float, float]
    start_time: datetime
    end_time: datetime


class RosterRequest(BaseModel):
    jobs: List[Job] = Field(min_length=1)  # At least one job required
    salesman: List[Salesman] = Field(min_length=1)  # At least one cleaner required
