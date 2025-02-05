from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Tuple, List


class Job(BaseModel):
    job_id: int
    date: datetime  # date the job needs to be completed
    location: Tuple[float, float]  # GPS location of the job
    duration: int  # estimated duration of service
    entry_time: datetime  # earliest entry time for starting the job
    exit_time: datetime  # latest exit time for completing the job
    salesman_id: Optional[int] = None  # designated salesman's ID
    start_time: Optional[datetime] = None  # designated start time


class Salesman(BaseModel):
    salesman_id: int
    home_location: Tuple[float, float]  # starting location of the salesman
    start_time: datetime  # earliest available start time of the salesman
    end_time: datetime  # latest available end time of the salesman


class Roster(BaseModel):
    salesman_id: int
    jobs: List[Job]


class Rosters(BaseModel):
    roster_id: int
    date: datetime  # effective date of the roster
    roster: List[Roster]  # list of each salesman's roster
