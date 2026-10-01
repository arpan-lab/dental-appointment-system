from pydantic import BaseModel


class Patient(BaseModel):
    patient_id: str
    name: str
    phone: str
    email: str