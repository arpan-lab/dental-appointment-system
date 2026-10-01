from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PatientDB(Base):
    __tablename__ = "patients"

    patient_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )