from datetime import datetime

from app.database.connection import SessionLocal
from app.models.db_appointment import AppointmentDB
from app.models.db_patient import PatientDB
from app.models.db_doctor import DoctorDB


def appointment_to_dict(
    appointment: AppointmentDB
) -> dict:
    """
    Convert SQLAlchemy AppointmentDB object
    to the dictionary format used by the application.
    """
    return {
        "appointment_id": appointment.appointment_id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "date": appointment.appointment_date.isoformat(),
        "time": appointment.appointment_time.strftime("%H:%M"),
        "status": appointment.status,
    }


def parse_date(date: str):
    """
    Convert date string into Python date object.
    """
    try:
        return datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        try:
            return datetime.strptime(
                date,
                "%d/%m/%Y"
            ).date()
        except ValueError:
            raise ValueError(
                "Invalid appointment date format. "
                "Use YYYY-MM-DD."
            )


def parse_time(time: str):
    """
    Convert time string into Python time object.
    """
    for fmt in ("%H:%M", "%I:%M %p"):
        try:
            return datetime.strptime(
                time.strip(),
                fmt
            ).time()
        except ValueError:
            continue

    raise ValueError(
        "Invalid appointment time format. "
        "Use HH:MM or HH:MM AM/PM."
    )


def is_doctor_available_on_date(
    doctor_id: str,
    appointment_date
) -> bool:
    """
    Check whether the doctor is available
    on the requested date.
    """
    from app.services.doctor_service import (
        get_doctor_by_id
    )

    doctor = get_doctor_by_id(doctor_id)

    if doctor is None:
        return False

    available_days = [
        day.strip().lower()
        for day in doctor["available_days"].split("|")
    ]

    requested_day = (
        appointment_date.strftime("%A").lower()
    )

    return requested_day in available_days


def get_all_appointments() -> list[dict]:
    """
    Return all appointments from MySQL.
    """
    session = SessionLocal()

    try:
        appointments = (
            session.query(AppointmentDB)
            .all()
        )

        return [
            appointment_to_dict(appointment)
            for appointment in appointments
        ]

    finally:
        session.close()


def get_appointments_by_patient(
    patient_id: str
) -> list[dict]:
    """
    Find all appointments for a patient.
    """
    session = SessionLocal()

    try:
        appointments = (
            session.query(AppointmentDB)
            .filter(
                AppointmentDB.patient_id == patient_id
            )
            .all()
        )

        return [
            appointment_to_dict(appointment)
            for appointment in appointments
        ]

    finally:
        session.close()


def get_appointment_by_id(
    appointment_id: str
) -> dict | None:
    """
    Find an appointment using appointment ID.
    """
    session = SessionLocal()

    try:
        appointment = (
            session.query(AppointmentDB)
            .filter(
                AppointmentDB.appointment_id
                == appointment_id
            )
            .first()
        )

        if appointment is None:
            return None

        return appointment_to_dict(appointment)

    finally:
        session.close()


def is_slot_available(
    doctor_id: str,
    date: str,
    time: str
) -> bool:
    """
    Check whether a doctor's slot is available.
    """
    appointment_date = parse_date(date)
    appointment_time = parse_time(time)

    session = SessionLocal()

    try:
        existing = (
            session.query(AppointmentDB)
            .filter(
                AppointmentDB.doctor_id == doctor_id,
                AppointmentDB.appointment_date
                == appointment_date,
                AppointmentDB.appointment_time
                == appointment_time,
                AppointmentDB.status.ilike("booked"),
            )
            .first()
        )

        return existing is None

    finally:
        session.close()


def generate_appointment_id() -> str:
    """
    Generate the next appointment ID.

    Example:
    A001 → A002 → A003
    """
    session = SessionLocal()

    try:
        appointments = (
            session.query(AppointmentDB)
            .all()
        )

        if not appointments:
            return "A001"

        numbers = []

        for appointment in appointments:

            appointment_id = str(
                appointment.appointment_id
            )

            if appointment_id.startswith("A"):
                try:
                    numbers.append(
                        int(appointment_id[1:])
                    )
                except ValueError:
                    continue

        if not numbers:
            next_number = 1
        else:
            next_number = max(numbers) + 1

        return f"A{next_number:03d}"

    finally:
        session.close()


def book_appointment(
    patient_id: str,
    doctor_id: str,
    date: str,
    time: str
) -> dict:
    """
    Create a new appointment.
    """

    # Validate patient ID
    from app.services.patient_service import (
        get_patient_by_id
    )

    patient = get_patient_by_id(patient_id)

    if patient is None:
        raise ValueError(
            f"Patient '{patient_id}' was not found."
        )

    # Validate doctor ID
    from app.services.doctor_service import (
        get_doctor_by_id
    )

    doctor = get_doctor_by_id(doctor_id)

    if doctor is None:
        raise ValueError(
            f"Doctor '{doctor_id}' was not found."
        )

    # Validate date
    if not date:
        raise ValueError(
            "Appointment date is required."
        )

    # Validate time
    if not time:
        raise ValueError(
            "Appointment time is required."
        )

    appointment_date = parse_date(date)
    appointment_time = parse_time(time)

    # Validate doctor's available day
    if not is_doctor_available_on_date(
        doctor_id,
        appointment_date
    ):
        raise ValueError(
            f"Doctor '{doctor_id}' is not available "
            f"on {appointment_date.strftime('%A')}."
        )

    # Check slot availability
    if not is_slot_available(
        doctor_id,
        date,
        time
    ):
        raise ValueError(
            "The selected appointment slot "
            "is already booked."
        )

    # Generate ID inside application
    appointment_id = generate_appointment_id()

    session = SessionLocal()

    try:
        new_appointment = AppointmentDB(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="booked",
        )

        session.add(new_appointment)
        session.commit()
        session.refresh(new_appointment)

        return appointment_to_dict(
            new_appointment
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def cancel_appointment(
    appointment_id: str
) -> dict:
    """
    Cancel an existing booked appointment.
    """
    session = SessionLocal()

    try:
        appointment = (
            session.query(AppointmentDB)
            .filter(
                AppointmentDB.appointment_id
                == appointment_id
            )
            .first()
        )

        if appointment is None:
            raise ValueError(
                f"Appointment '{appointment_id}' "
                "was not found."
            )

        if appointment.status.lower() != "booked":
            raise ValueError(
                "Only booked appointments "
                "can be cancelled."
            )

        appointment.status = "cancelled"

        session.commit()
        session.refresh(appointment)

        return appointment_to_dict(
            appointment
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def reschedule_appointment(
    appointment_id: str,
    new_date: str,
    new_time: str
) -> dict:
    """
    Reschedule an existing appointment.
    """
    session = SessionLocal()

    try:
        appointment = (
            session.query(AppointmentDB)
            .filter(
                AppointmentDB.appointment_id
                == appointment_id
            )
            .first()
        )

        if appointment is None:
            raise ValueError(
                f"Appointment '{appointment_id}' "
                "was not found."
            )

        if appointment.status.lower() != "booked":
            raise ValueError(
                "Only booked appointments "
                "can be rescheduled."
            )

        if not new_date:
            raise ValueError(
                "New appointment date is required."
            )

        if not new_time:
            raise ValueError(
                "New appointment time is required."
            )

        new_appointment_date = parse_date(
            new_date
        )

        new_appointment_time = parse_time(
            new_time
        )

        doctor_id = appointment.doctor_id

        # Validate doctor's available day
        if not is_doctor_available_on_date(
            doctor_id,
            new_appointment_date
        ):
            raise ValueError(
                f"Doctor '{doctor_id}' is not available "
                f"on {new_appointment_date.strftime('%A')}."
            )

        # Check new slot availability
        if not is_slot_available(
            doctor_id,
            new_date,
            new_time
        ):
            raise ValueError(
                "The new appointment slot "
                "is already booked."
            )

        appointment.appointment_date = (
            new_appointment_date
        )

        appointment.appointment_time = (
            new_appointment_time
        )

        session.commit()
        session.refresh(appointment)

        return appointment_to_dict(
            appointment
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()