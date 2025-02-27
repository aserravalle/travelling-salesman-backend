from fastapi import APIRouter
from app.models.roster import Roster
from app.models.roster_request import RosterRequest
from app.services.job_assignment import assign_jobs

router = APIRouter()


@router.post("/assign_jobs")
def assign_jobs_endpoint(request: RosterRequest) -> Roster:
    roster = assign_jobs(request.jobs, request.salesmen)
    return roster.model_dump()
