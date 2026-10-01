from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AppointmentDB(Base):
    __tablename__ = "appointments"

    appointment_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    patient_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    doctor_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    appointment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    appointment_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="booked"
    )