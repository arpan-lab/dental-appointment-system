
from app.tools.doctor_tools import (
    list_doctors,
    find_doctor_by_id,
    find_doctors_by_specialization,
)


# ============================================================
# LIST DOCTORS
# ============================================================

def test_list_doctors():

    result = list_doctors.invoke({})

    assert len(result) >= 4

    doctor_ids = [
        doctor["doctor_id"]
        for doctor in result
    ]

    assert "D001" in doctor_ids
    assert "D002" in doctor_ids
    assert "D003" in doctor_ids


# ============================================================
# FIND DOCTOR BY ID
# ============================================================

def test_find_doctor_by_id():

    result = find_doctor_by_id.invoke({
        "doctor_id": "D002"
    })

    assert result is not None
    assert result["doctor_id"] == "D002"
    assert result["name"] == "Michael Smith"
    assert result["specialization"] == "Orthodontist"


def test_find_doctor_by_id_not_found():

    result = find_doctor_by_id.invoke({
        "doctor_id": "BAD"
    })

    assert result is None


# ============================================================
# FIND DOCTORS BY SPECIALIZATION
# ============================================================

def test_find_doctors_by_specialization():

    result = find_doctors_by_specialization.invoke({
        "specialization": "Orthodontist"
    })

    assert len(result) == 1
    assert result[0]["doctor_id"] == "D002"
    assert result[0]["name"] == "Michael Smith"


def test_specialization_case_insensitive():

    result = find_doctors_by_specialization.invoke({
        "specialization": "ORTHODONTIST"
    })

    assert len(result) == 1
    assert result[0]["doctor_id"] == "D002"


def test_specialization_not_found():

    result = find_doctors_by_specialization.invoke({
        "specialization": "Surgeon"
    })

    assert result == []