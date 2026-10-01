
from langchain_core.tools import tool

from app.services.doctor_service import (
    get_all_doctors,
    get_doctor_by_id,
    get_doctor_by_name,
    get_doctors_by_specialization,
)


@tool
def list_doctors() -> list[dict]:
    """
    Get a list of all available doctors.
    """

    return get_all_doctors()


@tool
def find_doctor_by_id(doctor_id: str) -> dict | None:
    """
    Find a doctor using their doctor ID.
    """

    return get_doctor_by_id(doctor_id)


@tool
def find_doctor_by_name(name: str) -> dict | None:
    """
    Find a doctor using their name.
    """

    return get_doctor_by_name(name)


@tool
def find_doctors_by_specialization(
    specialization: str
) -> list[dict]:
    """
    Find doctors based on their specialization.
    """

    return get_doctors_by_specialization(
        specialization
    )

