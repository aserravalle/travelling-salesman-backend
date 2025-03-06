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

    def can_complete_job_in_time(self, job_exit_time: datetime, completion_time: datetime) -> bool:
        """
        Check if the salesman can complete a job within the given constraints.
        
        Args:
            job_exit_time: Latest allowed completion time for the job
            completion_time: Estimated completion time
            
        Returns:
            bool: True if job can be completed within constraints
        """
        if completion_time > min(self.end_time, job_exit_time):
            return False
            
        total_work_mins = (completion_time - self.start_time).total_seconds() / 60
        return total_work_mins <= self.max_workday_mins

    def assign_to_salesman(self, job: Job) -> None:
        """
        Update salesman's state after job assignment.
        
        Args:
            job: The job being assigned
        """
        if self.is_first_job():
            self.start_time = job.start_time
        self.current_location = job.location
        self.current_time = job.start_time + timedelta(minutes=job.duration_mins)
        self.time_worked_mins += job.duration_mins

    def get_arrival_time(self, job: Job) -> datetime:
        """
        Calculate the earliest possible arrival time at a job location.
        
        Args:
            job: The job to travel to
            
        Returns:
            datetime: Earliest possible arrival time
        """
        travel_time = self.current_location.travel_time_to(job.location)
        return max(self.current_time + travel_time, job.entry_time)

    def is_first_job(self) -> bool:
        """Check if this would be the first job assigned to the salesman."""
        return self.current_time == self.start_time