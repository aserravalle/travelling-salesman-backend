from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

from app.models.job import Job
from app.models.salesman import Salesman


class Roster(BaseModel):
    roster_id: str
    date: datetime                              # effective date of the roster
    jobs: Optional[Dict[str, List[Job]]] = {}   # key: salesman_id, value: list of jobs they will complete
    unassigned_jobs: List[Job] = []
    message: Optional[str] = None

    def add_salesmen(self, salesmen: List[Salesman] = []):
        for sman in salesmen:
            self.add_salesman(sman)

    def add_salesman(self, sman: Salesman):
        sman.current_location = sman.home_location
        sman.current_time = sman.start_time
        self.jobs[sman.salesman_id] = []

    def assign_job_to_salesman(self, job: Job, salesman: Salesman, job_start_time: datetime) -> None:
        job.assign_salesman_and_start_time(salesman.salesman_id, job_start_time)
        salesman.assign_to_salesman(job)

        self.jobs[salesman.salesman_id].append(job)
