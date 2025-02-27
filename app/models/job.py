from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models.location import Location


class Job(BaseModel):
    job_id: str
    date: datetime                              # date the job needs to be completed
    location: Location                          # GPS location of the job
    duration_mins: int                          # estimated duration of service
    entry_time: datetime                        # earliest entry time for starting the job
    exit_time: datetime                         # latest exit time for completing the job
    salesman_id: Optional[int] = None           # designated salesman's ID
    start_time: Optional[datetime] = None       # designated start time

    def assign_salesman_and_start_time(self, salesman_id, job_start_time):
        self.salesman_id = salesman_id
        self.start_time = job_start_time

    def __lt__(self, other: "Job") -> bool:
        """
        Job sort order is determined first by its entry time, then by the size of the job window
        """
        return (self.date, self.entry_time, self.exit_time - self.entry_time) < (other.date, other.entry_time, other.exit_time - other.entry_time)
