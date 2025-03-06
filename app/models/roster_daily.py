from pydantic import BaseModel
from datetime import datetime, date
from typing import List
from pydantic import Field

from app.models.job import Job
from app.models.salesman import Salesman


class RosterDaily(BaseModel):
    """
    Represents a daily roster of job assignments to salesmen.

    Attributes:
        date: Effective date of roster
        salesman_id: ID of salesman to which this roster applies
        jobs: List of assigned jobs
    """

    date: date
    salesman_id: str
    jobs: List[Job] = Field(default_factory=list)
    
    def assign_job_to_salesman(
        self, job: Job, salesman: Salesman, job_start_time: datetime
    ) -> None:
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
