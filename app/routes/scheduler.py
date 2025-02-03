from fastapi import APIRouter
from app.models.schemas import ScheduleRequest
from app.services.scheduler_logic import generate_schedule

router = APIRouter(prefix="/schedule", tags=["Scheduling"])


@router.post("/")
def schedule_jobs(schedule_data: ScheduleRequest):
    result = generate_schedule(schedule_data)
    return {"schedule": result}
