
import app.services.doctor_service as doctor_service


# ============================================================
# GET ALL DOCTORS
# ============================================================

def test_get_all_doctors():

    doctors = doctor_service.get_all_doctors()

    assert len(doctors) >= 4

    doctor_ids = [
        doctor["doctor_id"]
        for doctor in doctors
    ]

    assert "D001" in doctor_ids


# ============================================================
# GET DOCTOR BY ID
# ============================================================

def test_get_doctor_by_id():

    doctor = doctor_service.get_doctor_by_id(
        "D002"
    )

    assert doctor is not None
    assert doctor["doctor_id"] == "D002"
    assert doctor["name"] == "Michael Smith"
    assert doctor["specialization"] == "Orthodontist"


def test_get_doctor_by_id_not_found():

    doctor = doctor_service.get_doctor_by_id(
        "BAD"
    )

    assert doctor is None


# ============================================================
# GET DOCTORS BY SPECIALIZATION
# ============================================================

def test_get_doctors_by_specialization():

    doctors = (
        doctor_service.get_doctors_by_specialization(
            "Orthodontist"
        )
    )

    assert len(doctors) == 1
    assert doctors[0]["doctor_id"] == "D002"
    assert doctors[0]["name"] == "Michael Smith"


def test_specialization_case_insensitive():

    doctors = (
        doctor_service.get_doctors_by_specialization(
            "ORTHODONTIST"
        )
    )

    assert len(doctors) == 1
    assert doctors[0]["doctor_id"] == "D002"


def test_specialization_not_found():

    doctors = (
        doctor_service.get_doctors_by_specialization(
            "Surgeon"
        )
    )

    assert doctors == []