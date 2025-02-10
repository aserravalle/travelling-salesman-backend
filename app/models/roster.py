from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional

from app.models.job import Job
from app.models.salesman import Salesman


class Roster(BaseModel):
    roster_id: str
    date: datetime  # effective date of the roster
    jobs: Optional[Dict[str, List[Job]]] = Field(
        default_factory=dict
    )  # key: salesman_id, value: list of jobs they will complete

    def add_salesmen(self, salesmen: List[Salesman] = []):
        for sman in salesmen:
            self.add_salesman(sman)

    def add_salesman(self, sman: Salesman):
        sman.current_location = sman.home_location
        sman.current_time = sman.start_time
        self.jobs[sman.salesman_id] = []

    def assign_job_to_salesman(
        self, job: Job, salesman: Salesman, job_start_time: datetime
    ) -> None:
        job.update_status(salesman.salesman_id, job_start_time)
        salesman.update_status(job)

        self.jobs[salesman.salesman_id].append(job)
