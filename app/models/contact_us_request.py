from pydantic import BaseModel


class ContactUsRequest(BaseModel):
    name: str
    email: str
    phoneNumber: str
    message: str