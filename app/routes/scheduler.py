import os
from fastapi import APIRouter, HTTPException

from app.models.roster_response import RosterResponse
from app.models.roster_request import RosterRequest
from app.services.job_assignment import assign_jobs

from app.models.contact_us_request import ContactUsRequest
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

router = APIRouter()

@router.post("/assign_jobs")
def assign_jobs_endpoint_post(request: RosterRequest) -> dict:
    try:
        roster = assign_jobs(request.jobs, request.salesmen)
        return roster.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assign_jobs")
def assign_jobs_endpoint_get() -> str:
    return "assign_jobs works"

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_EMAIL_ADDRESS = os.getenv("SENDGRID_EMAIL_ADDRESS", "")

@router.post("/contact_us")
def contact_us_endpoint_post(request: ContactUsRequest) -> dict:
    if not SENDGRID_API_KEY or not SENDGRID_EMAIL_ADDRESS:
        raise HTTPException(status_code=500, detail="SendGrid API key or email address not configured")

    message = Mail(
        from_email=SENDGRID_EMAIL_ADDRESS,
        to_emails=SENDGRID_EMAIL_ADDRESS,
        subject=f"Caminora Contact Us: {request.name}",
        plain_text_content=f"Name: {request.name}\nEmail: {request.email}\nPhone: {request.phoneNumber}\nMessage:\n\n{request.message}",
        html_content=f"""
            <p><strong>Name:</strong> {request.name}</p>
            <p><strong>Email:</strong> {request.email}</p>
            <p><strong>Phone:</strong> {request.phoneNumber}</p>
            <p><strong>Message:</strong></p>
            <p>{request.message.replace('\n', '<br/>')}</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        print(f"SendGrid error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")

@router.get("/contact_us")
def contact_us_endpoint() -> str:
    if not SENDGRID_API_KEY:
        raise HTTPException(status_code=500, detail="SendGrid API key not configured")
    if not SENDGRID_EMAIL_ADDRESS:
        raise HTTPException(status_code=500, detail="SendGrid email address not configured")
    return "contact_us works"
