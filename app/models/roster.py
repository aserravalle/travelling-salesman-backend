from datetime import datetime
from typing import Dict, List, Optional
from pydantic import Field

from app.models.base_model import BaseModel
from app.models.job import Job
from app.models.salesman import Salesman

class RosterResponse(BaseModel):
    """
    Represents a daily roster of job assignments to salesmen.
    
    Attributes:
        jobs: Dictionary mapping salesman IDs to their assigned jobs
        unassigned_jobs: List of jobs that couldn't be assigned
        message: Status message about the roster creation
    """
    jobs: Dict[str, List[Job]] = Field(default_factory=dict)
    unassigned_jobs: List[Job] = Field(default_factory=list)
    message: Optional[str] = None

    def add_salesmen(self, salesmen: List[Salesman]) -> None:
        """Initialize roster with a list of salesmen."""
        for salesman in salesmen:
            self.add_salesman(salesman)

    def add_salesman(self, salesman: Salesman) -> None:
        """
        Initialize a salesman in the roster.
        
        Args:
            salesman: Salesman to add to the roster
        """
        salesman.current_location = salesman.home_location
        salesman.current_time = salesman.start_time
        self.jobs[salesman.salesman_id] = []

    def assign_job_to_salesman(self, job: Job, salesman: Salesman, job_start_time: datetime) -> None:
        """
        Assign a job to a salesman and update relevant states.
        
        Args:
            job: Job to assign
            salesman: Salesman to assign the job to
            job_start_time: When the job should start
        """
        job.assign_salesman_and_start_time(salesman.salesman_id, job_start_time)
        salesman.assign_to_salesman(job)
        self.jobs[salesman.salesman_id].append(job)