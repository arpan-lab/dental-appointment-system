from app.database.connection import SessionLocal
from app.models.db_patient import PatientDB


def patient_to_dict(patient: PatientDB) -> dict:
    """
    Convert SQLAlchemy PatientDB object to dictionary.
    """

    return {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "phone": patient.phone,
        "email": patient.email,
    }


def get_all_patients() -> list[dict]:
    """
    Return all patients from MySQL.
    """

    session = SessionLocal()

    try:
        patients = session.query(PatientDB).all()

        return [
            patient_to_dict(patient)
            for patient in patients
        ]

    finally:
        session.close()


def get_patient_by_id(patient_id: str) -> dict | None:
    """
    Find a patient by patient_id from MySQL.
    """

    session = SessionLocal()

    try:
        patient = (
            session.query(PatientDB)
            .filter(PatientDB.patient_id == patient_id)
            .first()
        )

        if patient is None:
            return None

        return patient_to_dict(patient)

    finally:
        session.close()


def get_patient_by_email(email: str) -> dict | None:
    """
    Find a patient by email from MySQL.
    """

    session = SessionLocal()

    try:
        patient = (
            session.query(PatientDB)
            .filter(PatientDB.email.ilike(email))
            .first()
        )

        if patient is None:
            return None

        return patient_to_dict(patient)

    finally:
        session.close()