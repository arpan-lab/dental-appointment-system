import pytest

from app.database.connection import SessionLocal
from app.models.db_appointment import AppointmentDB
from app.models.db_patient import PatientDB
from app.models.db_doctor import DoctorDB
import app.services.appointment_service as appointment_service


@pytest.fixture
def test_data():

    session = SessionLocal()

    patient_id = "TEST_P001"
    doctor_id = "TEST_D001"

    # Clean up old test data if it exists
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

    # Create test patient
    patient = PatientDB(
        patient_id=patient_id,
        name="Test Patient",
        phone="9999999999",
        email="test_patient@example.com",
    )

    # Create test doctor
    # Available every day because these tests focus
    # on appointment functionality, not doctor schedules.
    doctor = DoctorDB(
        doctor_id=doctor_id,
        name="Test Doctor",
        specialization="General Dentist",
        available_days=(
            "Monday|Tuesday|Wednesday|Thursday|"
            "Friday|Saturday|Sunday"
        ),
    )

    session.add(patient)
    session.add(doctor)
    session.commit()

    yield {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
    }

    # Clean up after test
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
# GENERATE APPOINTMENT ID
# ============================================================

def test_generate_appointment_id(test_data):

    appointment_id = (
        appointment_service.generate_appointment_id()
    )

    assert appointment_id.startswith("A")
    assert appointment_id[1:].isdigit()


# ============================================================
# SUCCESSFUL BOOKING
# ============================================================

def test_successful_booking(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-05",
        "10:00",
    )

    assert appointment["appointment_id"].startswith("A")
    assert appointment["patient_id"] == test_data["patient_id"]
    assert appointment["doctor_id"] == test_data["doctor_id"]
    assert appointment["status"] == "booked"


# ============================================================
# INVALID PATIENT
# ============================================================

def test_invalid_patient(test_data):

    with pytest.raises(
        ValueError,
        match="Patient.*not found",
    ):
        appointment_service.book_appointment(
            "BAD",
            test_data["doctor_id"],
            "2026-10-05",
            "10:00",
        )


# ============================================================
# INVALID DOCTOR
# ============================================================

def test_invalid_doctor(test_data):

    with pytest.raises(
        ValueError,
        match="Doctor.*not found",
    ):
        appointment_service.book_appointment(
            test_data["patient_id"],
            "BAD",
            "2026-10-05",
            "10:00",
        )


# ============================================================
# DUPLICATE BOOKING
# ============================================================

def test_duplicate_booking(test_data):

    appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-06",
        "11:00",
    )

    with pytest.raises(
        ValueError,
        match="already booked",
    ):
        appointment_service.book_appointment(
            test_data["patient_id"],
            test_data["doctor_id"],
            "2026-10-06",
            "11:00",
        )


# ============================================================
# SUCCESSFUL CANCELLATION
# ============================================================

def test_successful_cancellation(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-07",
        "10:00",
    )

    result = appointment_service.cancel_appointment(
        appointment["appointment_id"]
    )

    assert result["appointment_id"] == appointment["appointment_id"]
    assert result["status"] == "cancelled"


# ============================================================
# CANCEL NONEXISTENT APPOINTMENT
# ============================================================

def test_cancel_nonexistent_appointment(test_data):

    with pytest.raises(
        ValueError,
        match="was not found",
    ):
        appointment_service.cancel_appointment(
            "BAD"
        )


# ============================================================
# CANCEL ALREADY CANCELLED
# ============================================================

def test_cancel_already_cancelled(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-08",
        "10:00",
    )

    appointment_service.cancel_appointment(
        appointment["appointment_id"]
    )

    with pytest.raises(
        ValueError,
        match="Only booked appointments",
    ):
        appointment_service.cancel_appointment(
            appointment["appointment_id"]
        )


# ============================================================
# SUCCESSFUL RESCHEDULING
# ============================================================

def test_successful_rescheduling(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-09",
        "10:00",
    )

    result = appointment_service.reschedule_appointment(
        appointment["appointment_id"],
        "2026-10-10",
        "12:00",
    )

    assert result["appointment_id"] == appointment["appointment_id"]
    assert result["date"] == "2026-10-10"
    assert result["time"] == "12:00"
    assert result["status"] == "booked"


# ============================================================
# RESCHEDULE TO OCCUPIED SLOT
# ============================================================

def test_reschedule_to_occupied_slot(test_data):

    first = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-11",
        "11:00",
    )

    second = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-12",
        "11:00",
    )

    with pytest.raises(
        ValueError,
        match="already booked",
    ):
        appointment_service.reschedule_appointment(
            second["appointment_id"],
            "2026-10-11",
            "11:00",
        )


# ============================================================
# RESCHEDULE CANCELLED APPOINTMENT
# ============================================================

def test_reschedule_cancelled_appointment(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-13",
        "12:00",
    )

    appointment_service.cancel_appointment(
        appointment["appointment_id"]
    )

    with pytest.raises(
        ValueError,
        match="Only booked appointments",
    ):
        appointment_service.reschedule_appointment(
            appointment["appointment_id"],
            "2026-10-14",
            "12:00",
        )


# ============================================================
# DOCTOR AVAILABILITY
# ============================================================

def test_booking_on_doctor_available_day(test_data):

    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-06",  # Tuesday
        "10:00",
    )

    assert appointment["status"] == "booked"


def test_booking_on_doctor_unavailable_day(test_data):

    # TEST_D001 is available every day in the generic fixture,
    # so temporarily change the doctor's schedule for this test.

    session = SessionLocal()

    doctor = session.query(DoctorDB).filter(
        DoctorDB.doctor_id == test_data["doctor_id"]
    ).first()

    doctor.available_days = "Tuesday|Thursday|Saturday"

    session.commit()
    session.close()

    with pytest.raises(
        ValueError,
        match="not available",
    ):
        appointment_service.book_appointment(
            test_data["patient_id"],
            test_data["doctor_id"],
            "2026-10-05",  # Monday
            "10:00",
        )


def test_reschedule_to_doctors_available_day(test_data):

    # Initial appointment: Tuesday
    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-06",
        "10:00",
    )

    # Reschedule to Thursday
    result = appointment_service.reschedule_appointment(
        appointment["appointment_id"],
        "2026-10-08",
        "12:00",
    )

    assert result["date"] == "2026-10-08"
    assert result["time"] == "12:00"
    assert result["status"] == "booked"


def test_reschedule_to_doctors_unavailable_day(test_data):

    # Change test doctor's schedule
    session = SessionLocal()

    doctor = session.query(DoctorDB).filter(
        DoctorDB.doctor_id == test_data["doctor_id"]
    ).first()

    doctor.available_days = "Tuesday|Thursday|Saturday"

    session.commit()
    session.close()

    # Create appointment on Tuesday
    appointment = appointment_service.book_appointment(
        test_data["patient_id"],
        test_data["doctor_id"],
        "2026-10-06",
        "10:00",
    )

    # Try to move it to Monday
    with pytest.raises(
        ValueError,
        match="not available",
    ):
        appointment_service.reschedule_appointment(
            appointment["appointment_id"],
            "2026-10-05",
            "12:00",
        )

