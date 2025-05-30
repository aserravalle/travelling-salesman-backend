from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional
from pydantic import Field

from app.models.location import Location


class Job(BaseModel):
    """
    Represents a job that needs to be completed by a salesman.

    Attributes:
        job_id: Unique identifier for the job
        client_name: Optional name of the client
        date: Date the job needs to be completed
        location: Location of the job (coordinates and/or address)
        duration_mins: Estimated duration of service in minutes
        entry_time: Earliest time the job can be started
        exit_time: Latest time the job must be completed
        salesman_id: ID of the assigned salesman (optional)
        start_time: Scheduled start time (optional)
    """

    job_id: str
    client_name: Optional[str] = None
    date: datetime
    location: Location
    duration_mins: int = Field(gt=0)
    entry_time: datetime
    exit_time: datetime
    salesman_id: Optional[str] = None
    salesman_name: Optional[str] = None
    start_time: Optional[datetime] = None
    cluster: Optional[int] = None
    _travel_time_mins: Optional[int] = 0

    @field_validator('exit_time')
    @classmethod
    def validate_exit_time(cls, v, values):
        if 'entry_time' in values.data and v < values.data['entry_time']:
            raise ValueError('exit_time must be after entry_time')
        return v

    @model_validator(mode="after")
    def adjust_exit_time_if_needed(self) -> 'Job':
        availability = (self.exit_time - self.entry_time).total_seconds() / 60
        if availability < self.duration_mins:
            self.exit_time = self.entry_time + timedelta(minutes=self.duration_mins)
        return self

    def assign_salesman(
        self, salesman_id: str, job_start_time: datetime, salesman_name: str = ""
    ) -> None:
        self.salesman_id = salesman_id
        self.salesman_name = salesman_name
        self.start_time = job_start_time

    @property
    def urgency(self) -> float:
        """
        Calculate the urgency of the job based on the time window and duration.

        Returns:
            float: Urgency score
        """
        return self.get_urgency()

    def get_urgency(self) -> float:
        time_diff = self.exit_time - self.entry_time
        time_diff_mins = time_diff.total_seconds() / 60
        urgency = (self.duration_mins ** 2) / time_diff_mins
        return urgency

    def __lt__(self, other: "Job") -> bool:
        """
        Compare jobs for sorting. Jobs are sorted by:
        1. Date
        2. Entry time
        3. Job duration
        4. Time window duration
        """
        return self.urgency < other.urgency