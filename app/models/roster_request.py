from pydantic import BaseModel
from typing import List

from app.models.job import Job
from app.models.salesman import Salesman


class RosterRequest(BaseModel):
    jobs: List[Job]
    salesmen: List[Salesman]
