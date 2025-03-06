from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field

from app.models.location import Location


class Job(BaseModel):
    """
    Represents a job that needs to be completed by a salesman.

    Attributes:
        job_id: Unique identifier for the job
        date: Date the job needs to be completed
        location: GPS location of the job
        duration_mins: Estimated duration of service in minutes
        entry_time: Earliest time the job can be started
        exit_time: Latest time the job must be completed
        salesman_id: ID of the assigned salesman (optional)
        start_time: Scheduled start time (optional)
    """

    job_id: str
    date: datetime
    location: Location
    duration_mins: int = Field(gt=0)
    entry_time: datetime
    exit_time: datetime
    salesman_id: Optional[str] = None
    start_time: Optional[datetime] = None
    _travel_time_mins: Optional[int] = 0

    def assign_salesman_and_start_time(
        self, salesman_id: str, job_start_time: datetime
    ) -> None:
        """
        Assign a salesman and start time to this job.

        Args:
            salesman_id: ID of the salesman to assign
            job_start_time: Scheduled start time for the job
        """
        self.salesman_id = salesman_id
        self.start_time = job_start_time

    def __lt__(self, other: "Job") -> bool:
        """
        Compare jobs for sorting. Jobs are sorted by:
        1. Date
        2. Entry time
        3. Time window duration
        """
        return (
            self.date,
            self.entry_time,
            self.duration_mins,
            self.exit_time - self.entry_time,
        ) < (
            other.date,
            other.entry_time,
            other.duration_mins,
            other.exit_time - other.entry_time,
        )
