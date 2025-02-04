from fastapi import APIRouter
from app.models.schemas import RosterRequest
from app.services.scheduler_logic import generate_roster

router = APIRouter(prefix="/schedule", tags=["Scheduling"])


@router.post("/")
def schedule_jobs(roster_request: RosterRequest):
    roster = generate_roster(roster_request)
    return {"roster": roster}
