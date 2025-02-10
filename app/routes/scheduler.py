import json
from fastapi import APIRouter
from typing import List
from app.models.job import Job
from app.models.salesman import Salesman
from app.services.scheduler_logic import assign_jobs

router = APIRouter()


@router.post("/assign_jobs")
def assign_jobs_endpoint(jobs: List[Job], salesmen: List[Salesman]) -> json:
    roster = assign_jobs(jobs, salesmen)
    return roster.model_dump()
