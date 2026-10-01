from langchain_core.tools import tool

from app.services.appointment_service import (
    get_all_appointments,
    get_appointments_by_patient,
    get_appointment_by_id,
    is_slot_available,
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
)


@tool
def list_appointments() -> list[dict]:
    """
    Get all appointments in the system.
    """

    return get_all_appointments()


@tool
def find_patient_appointments(
    patient_id: str,
) -> list[dict]:
    """
    Find all appointments belonging to a patient.
    """

    return get_appointments_by_patient(patient_id)


@tool
def find_appointment(
    appointment_id: str,
) -> dict | None:
    """
    Find an appointment using its appointment ID.
    """

    return get_appointment_by_id(
        appointment_id
    )


@tool
def check_slot_availability(
    doctor_id: str,
    date: str,
    time: str,
) -> bool:
    """
    Check whether a doctor's appointment slot is available.
    """

    return is_slot_available(
        doctor_id,
        date,
        time,
    )


@tool
def create_appointment(
    patient_id: str,
    doctor_id: str,
    date: str,
    time: str,
) -> dict:
    """
    Create a new dental appointment.

    The appointment ID is generated automatically
    by the application.
    """

    return book_appointment(
        patient_id,
        doctor_id,
        date,
        time,
    )


@tool
def cancel_existing_appointment(
    appointment_id: str,
) -> dict:
    """
    Cancel an existing appointment.
    """

    return cancel_appointment(
        appointment_id,
    )


@tool
def reschedule_existing_appointment(
    appointment_id: str,
    new_date: str,
    new_time: str,
) -> dict:
    """
    Reschedule an existing appointment.
    """

    return reschedule_appointment(
        appointment_id,
        new_date,
        new_time,
    )