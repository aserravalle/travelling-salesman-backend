from pydantic import BaseModel, Field
from datetime import datetime
from typing import Tuple, List


class Job(BaseModel):
    id: int
    date: datetime
    location: Tuple[float, float]
    duration: int
    entry_time: datetime
    exit_time: datetime


class Salesman(BaseModel):
    id: int
    home_location: Tuple[float, float]
    start_time: datetime
    end_time: datetime
