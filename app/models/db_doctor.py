from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DoctorDB(Base):
    __tablename__ = "doctors"

    doctor_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    available_days: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )