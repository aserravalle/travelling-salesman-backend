from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from pydantic import Field

from app.models.location import Location
from app.models.job import Job


class Salesman(BaseModel):
    """
    Represents a salesman who can be assigned jobs.

    Attributes:
        salesman_id: Unique identifier for the salesman
        salesman_name: Optional name of the salesman
        location: Home location of the salesman (coordinates and/or address)
        start_time: Earliest available start time
        end_time: Latest available end time
        current_location: Current location during job assignment
        current_time: Current time during job assignment
        time_worked_mins: Minutes worked so far
        max_workday_mins: Maximum allowed work minutes per day
    """

    salesman_id: str
    salesman_name: Optional[str] = None
    location: Location
    start_time: datetime
    end_time: datetime
    current_location: Optional[Location] = None
    current_time: Optional[datetime] = None
    time_worked_mins: int = Field(default=0, ge=0)
    max_workday_mins: int = Field(default=9 * 60, ge=0)  # 9 hours

    def can_complete_job_in_time(
        self, job_exit_time: datetime, completion_time: datetime
    ) -> bool:
        """
        Check if the salesman can complete a job within the given constraints.

        Args:
            job_exit_time: Latest allowed completion time for the job
            completion_time: Estimated completion time

        Returns:
            bool: True if job can be completed within constraints
        """
        job_finished_in_time = completion_time <= min(self.end_time, job_exit_time)
        salesman_exceeds_max_hours = (completion_time - self.start_time) > timedelta(
            minutes=self.max_workday_mins
        )
        return job_finished_in_time and not salesman_exceeds_max_hours

    def is_at_capacity(self) -> bool:
        """If the salesman is close to reaching the maximum workday limit."""
        return self.time_worked_mins >= self.max_workday_mins - 80

    def wait(self, minutes) -> None:
        """Make the salesman wait on or off the clock depending on whether theyve started work already or not"""
        if self.is_first_job():
            self.start_time += timedelta(minutes=minutes)
            self.current_time = self.start_time
        else:
            self.current_time += timedelta(minutes=minutes)
            self.time_worked_mins += minutes

    def assign_job(self, job: Job) -> None:
        """
        Update salesman's state after job assignment.

        Args:
            job: The job being assigned
        """
        buffer_time = (
            job.start_time - self.current_time
        ).total_seconds() / 60  # accounts for travel time + waiting for the job to become available
        if self.is_first_job():
            self.start_time = job.start_time
            buffer_time = 0  # Travel time to first job is not paid
        self.current_location = job.location
        self.current_time = job.start_time + timedelta(minutes=job.duration_mins)
        self.time_worked_mins += job.duration_mins + buffer_time

    def is_first_job(self) -> bool:
        """Check if this would be the first job assigned to the salesman."""
        return self.current_time == self.start_time

    def get_arrival_time(self, job: Job, travel_time: timedelta) -> datetime:
        """
        Calculate the earliest possible arrival time at a job location.

        Args:
            job: The job to travel to
            travel_time: The time it takes to travel to the job location

        Returns:
            datetime: Earliest possible arrival time
        """
        if self.is_first_job():
            return max(self.start_time, job.entry_time)
        else:
            return max(self.current_time + travel_time, job.entry_time)

    def __lt__(self, other: "Salesman") -> bool:
        """
        Compare salesmen by earliest availability
        current_time where possible or start_time otherwise.
        """
        return self.earliest_availability() < other.earliest_availability()

    def earliest_availability(self):
        if self.current_time:
            return self.current_time
        else:
            return self.start_time