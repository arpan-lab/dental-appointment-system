from pydantic import BaseModel


class Appointment(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_id: str
    date: str
    time: str
    status: str = "booked"