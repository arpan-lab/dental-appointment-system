from langchain_core.tools import tool

from app.services.patient_service import (
    get_all_patients,
    get_patient_by_id,
    get_patient_by_email,
)


@tool
def list_patients() -> list[dict]:
    """
    Get a list of all registered patients.
    """

    return get_all_patients()


@tool
def find_patient_by_id(
    patient_id: str,
) -> dict | None:
    """
    Find a patient using their patient ID.
    """

    return get_patient_by_id(patient_id)


@tool
def find_patient_by_email(
    email: str,
) -> dict | None:
    """
    Find a patient using their email address.
    """

    return get_patient_by_email(email)