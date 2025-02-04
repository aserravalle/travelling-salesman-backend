from fastapi import APIRouter
from typing import List, Dict
from app.models.schemas import Job, Salesman
from app.services.scheduler_logic import assign_jobs

router = APIRouter()


@router.post("/assign_jobs")
def assign_jobs_endpoint(
    jobs: List[Job], salesmen: List[Salesman]
) -> Dict[int, List[int]]:
    return assign_jobs(jobs, salesmen)
