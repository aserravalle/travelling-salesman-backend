from pydantic import BaseModel
from datetime import datetime, timedelta
from pydantic import Field

from app.models.location import Location
from app.models.job import Job


class Salesman(BaseModel):
    """
    Represents a salesman who can be assigned jobs.

    Attributes:
        salesman_id: Unique identifier for the salesman
        home_location: Starting location of the salesman
        start_time: Earliest available start time
        end_time: Latest available end time
        current_location: Current location during job assignment
        current_time: Current time during job assignment
        time_worked_mins: Minutes worked so far
        max_workday_mins: Maximum allowed work minutes per day
    """

    salesman_id: str
    home_location: Location
    start_time: datetime
    end_time: datetime
    current_location: Location = None
    current_time: datetime = None
    time_worked_mins: int = Field(default=0, ge=0)
    max_workday_mins: int = Field(default=8 * 60, ge=0)  # 8 hours

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

    def assign_to_salesman(self, job: Job) -> None:
        """
        Update salesman's state after job assignment.

        Args:
            job: The job being assigned
        """
        buffer_time = (job.start_time - self.current_time).total_seconds() / 60 # time waiting and travelling between jobs
        if self.is_first_job():
            self.start_time = job.start_time
            buffer_time = 0 # Travel time to first job is not paid
        self.current_location = job.location
        self.current_time = job.start_time + timedelta(minutes=job.duration_mins)
        self.time_worked_mins += job.duration_mins + buffer_time

    def is_first_job(self) -> bool:
        """Check if this would be the first job assigned to the salesman."""
        return self.current_time == self.start_time

    def get_arrival_time(self, job: Job) -> datetime:
        """
        Calculate the earliest possible arrival time at a job location.

        Args:
            job: The job to travel to

        Returns:
            datetime: Earliest possible arrival time
        """
        if self.is_first_job():
            salesman_arrival_time = self.start_time
        else:
            travel_time = self.current_location.travel_time_to(job.location)
            salesman_arrival_time = self.current_time + travel_time
        
        return max(salesman_arrival_time, job.entry_time)


    def __lt__(self, other: "Salesman") -> bool:
        """
        Compare salesmen for sorting by:
        1. Date
        2. Entry time
        3. Time window duration
        """
        return self.earliest_availability() < other.earliest_availability()

    def earliest_availability(self):
        if self.current_time:
            return self.current_time
        else:
            return self.start_time