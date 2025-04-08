from fastapi import APIRouter
from pydantic import BaseModel
from app.models.roster_response import RosterResponse
from app.models.roster_request import RosterRequest
from app.services.job_assignment import assign_jobs

router = APIRouter()

@router.post("/assign_jobs")
def assign_jobs_endpoint_post(request: RosterRequest) -> RosterResponse:
    roster = assign_jobs(request.jobs, request.salesmen)
    return roster.model_dump()


@router.get("/assign_jobs")
def assign_jobs_endpoint_get() -> str:
    return "assign_jobs works"

class ContactUsRequest(BaseModel):
    name: str
    email: str
    phoneNumber: str
    message: str

@router.post("/contact_us")
def contact_us_endpoint(request: ContactUsRequest) -> dict:
    return {"response": f"Received message from {request.name} with email {request.email} and phone {request.phoneNumber}: {request.message}"}


@router.get("/contact_us")
def contact_us_endpoint() -> str:
    return "contact_us works"
