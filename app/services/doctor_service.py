from app.database.connection import SessionLocal
from app.models.db_doctor import DoctorDB


def doctor_to_dict(doctor: DoctorDB) -> dict:
    """
    Convert SQLAlchemy DoctorDB object to dictionary.
    """
    return {
        "doctor_id": doctor.doctor_id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "available_days": doctor.available_days,
    }


def get_all_doctors() -> list[dict]:
    """
    Return all doctors from MySQL.
    """
    session = SessionLocal()

    try:
        doctors = session.query(DoctorDB).all()

        return [
            doctor_to_dict(doctor)
            for doctor in doctors
        ]

    finally:
        session.close()


def get_doctor_by_id(doctor_id: str) -> dict | None:
    """
    Find a doctor by doctor_id from MySQL.
    """
    session = SessionLocal()

    try:
        doctor = (
            session.query(DoctorDB)
            .filter(
                DoctorDB.doctor_id == doctor_id
            )
            .first()
        )

        if doctor is None:
            return None

        return doctor_to_dict(doctor)

    finally:
        session.close()


def get_doctor_by_name(name: str) -> dict | None:
    """
    Find a doctor by name from MySQL.
    """

    session = SessionLocal()

    try:
        # Remove common title if provided by the user
        cleaned_name = name.strip()

        if cleaned_name.lower().startswith("dr. "):
            cleaned_name = cleaned_name[4:].strip()

        doctor = (
            session.query(DoctorDB)
            .filter(
                DoctorDB.name.ilike(
                    cleaned_name
                )
            )
            .first()
        )

        if doctor is None:
            return None

        return doctor_to_dict(doctor)

    finally:
        session.close()


def get_doctors_by_specialization(
    specialization: str
) -> list[dict]:
    """
    Find doctors by specialization from MySQL.
    """
    session = SessionLocal()

    try:
        doctors = (
            session.query(DoctorDB)
            .filter(
                DoctorDB.specialization.ilike(
                    specialization
                )
            )
            .all()
        )

        return [
            doctor_to_dict(doctor)
            for doctor in doctors
        ]

    finally:
        session.close()

