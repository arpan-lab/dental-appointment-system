import pytest

from app.database.connection import SessionLocal
from app.models.db_appointment import AppointmentDB
from app.models.db_patient import PatientDB
from app.models.db_doctor import DoctorDB

from app.tools.appointment_tools import (
    list_appointments,
    find_patient_appointments,
    find_appointment,
    check_slot_availability,
    create_appointment,
    cancel_existing_appointment,
    reschedule_existing_appointment,
)


@pytest.fixture
def test_data():

    session = SessionLocal()

    patient_id = "TEST_P002"
    doctor_id = "TEST_D002"

    # --------------------------------------------------------
    # Clean old test data
    # --------------------------------------------------------

    session.query(AppointmentDB).filter(
        AppointmentDB.patient_id == patient_id
    ).delete(synchronize_session=False)

    session.query(PatientDB).filter(
        PatientDB.patient_id == patient_id
    ).delete(synchronize_session=False)

    session.query(DoctorDB).filter(
        DoctorDB.doctor_id == doctor_id
    ).delete(synchronize_session=False)

    session.commit()

    # --------------------------------------------------------
    # Create test patient
    # --------------------------------------------------------

    patient = PatientDB(
        patient_id=patient_id,
        name="Tool Test Patient",
        phone="8888888888",
        email="tool_test_patient@example.com",
    )

    # --------------------------------------------------------
    # Create test doctor
    # --------------------------------------------------------
    # Available every day because these tests focus on
    # appointment tools, not doctor schedule validation.

    doctor = DoctorDB(
        doctor_id=doctor_id,
        name="Tool Test Doctor",
        specialization="General Dentist",
        available_days=(
            "Monday|Tuesday|Wednesday|Thursday|"
            "Friday|Saturday|Sunday"
        ),
    )

    session.add(patient)
    session.add(doctor)
    session.commit()

    # --------------------------------------------------------
    # Create two test appointments
    # --------------------------------------------------------

    appointment_service_import = __import__(
        "app.services.appointment_service",
        fromlist=["book_appointment"],
    )

    first = appointment_service_import.book_appointment(
        patient_id,
        doctor_id,
        "2026-10-20",
        "10:00",
    )

    second = appointment_service_import.book_appointment(
        patient_id,
        doctor_id,
        "2026-10-21",
        "11:00",
    )

    yield {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "first_appointment_id": first["appointment_id"],
        "second_appointment_id": second["appointment_id"],
    }

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    session = SessionLocal()

    session.query(AppointmentDB).filter(
        AppointmentDB.patient_id == patient_id
    ).delete(synchronize_session=False)

    session.query(PatientDB).filter(
        PatientDB.patient_id == patient_id
    ).delete(synchronize_session=False)

    session.query(DoctorDB).filter(
        DoctorDB.doctor_id == doctor_id
    ).delete(synchronize_session=False)

    session.commit()
    session.close()


# ============================================================
# LIST APPOINTMENTS
# ============================================================

def test_list_appointments(test_data):

    result = list_appointments.invoke({})

    appointment_ids = [
        appointment["appointment_id"]
        for appointment in result
    ]

    assert test_data["first_appointment_id"] in appointment_ids
    assert test_data["second_appointment_id"] in appointment_ids


# ============================================================
# FIND PATIENT APPOINTMENTS
# ============================================================

def test_find_patient_appointments(test_data):

    result = find_patient_appointments.invoke({
        "patient_id": test_data["patient_id"]
    })

    assert len(result) == 2

    for appointment in result:
        assert appointment["patient_id"] == test_data["patient_id"]


# ============================================================
# FIND APPOINTMENT
# ============================================================

def test_find_appointment(test_data):

    result = find_appointment.invoke({
        "appointment_id": test_data["first_appointment_id"]
    })

    assert result is not None

    assert result["appointment_id"] == (
        test_data["first_appointment_id"]
    )

    assert result["doctor_id"] == test_data["doctor_id"]


def test_find_appointment_not_found(test_data):

    result = find_appointment.invoke({
        "appointment_id": "BAD"
    })

    assert result is None


# ============================================================
# SLOT AVAILABILITY
# ============================================================

def test_check_slot_available(test_data):

    result = check_slot_availability.invoke({
        "doctor_id": test_data["doctor_id"],
        "date": "2026-10-22",
        "time": "10:00",
    })

    assert result is True


def test_check_slot_unavailable(test_data):

    result = check_slot_availability.invoke({
        "doctor_id": test_data["doctor_id"],
        "date": "2026-10-21",
        "time": "11:00",
    })

    assert result is False


# ============================================================
# CREATE APPOINTMENT
# ============================================================

def test_create_appointment(test_data):

    result = create_appointment.invoke({
        "patient_id": test_data["patient_id"],
        "doctor_id": test_data["doctor_id"],
        "date": "2026-10-23",
        "time": "10:00",
    })

    assert result["appointment_id"].startswith("A")
    assert result["patient_id"] == test_data["patient_id"]
    assert result["doctor_id"] == test_data["doctor_id"]
    assert result["date"] == "2026-10-23"
    assert result["time"] == "10:00"
    assert result["status"] == "booked"


def test_create_duplicate_appointment(test_data):

    with pytest.raises(
        ValueError,
        match="already booked",
    ):
        create_appointment.invoke({
            "patient_id": test_data["patient_id"],
            "doctor_id": test_data["doctor_id"],
            "date": "2026-10-21",
            "time": "11:00",
        })


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

def test_cancel_existing_appointment(test_data):

    result = cancel_existing_appointment.invoke({
        "appointment_id": test_data["first_appointment_id"]
    })

    assert result["appointment_id"] == (
        test_data["first_appointment_id"]
    )

    assert result["status"] == "cancelled"


def test_cancel_nonexistent_appointment(test_data):

    with pytest.raises(
        ValueError,
        match="was not found",
    ):
        cancel_existing_appointment.invoke({
            "appointment_id": "BAD"
        })


# ============================================================
# RESCHEDULE APPOINTMENT
# ============================================================

def test_reschedule_existing_appointment(test_data):

    result = reschedule_existing_appointment.invoke({
        "appointment_id": test_data["first_appointment_id"],
        "new_date": "2026-10-24",
        "new_time": "12:00",
    })

    assert result["appointment_id"] == (
        test_data["first_appointment_id"]
    )

    assert result["date"] == "2026-10-24"
    assert result["time"] == "12:00"
    assert result["status"] == "booked"


def test_reschedule_to_occupied_slot(test_data):

    with pytest.raises(
        ValueError,
        match="already booked",
    ):
        reschedule_existing_appointment.invoke({
            "appointment_id": test_data["first_appointment_id"],
            "new_date": "2026-10-21",
            "new_time": "11:00",
        })

