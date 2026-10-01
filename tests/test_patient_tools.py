
from app.tools.patient_tools import (
    list_patients,
    find_patient_by_id,
    find_patient_by_email,
)


# ============================================================
# LIST PATIENTS
# ============================================================

def test_list_patients():

    result = list_patients.invoke({})

    assert len(result) >= 4

    patient_ids = [
        patient["patient_id"]
        for patient in result
    ]

    assert "P001" in patient_ids


# ============================================================
# FIND PATIENT BY ID
# ============================================================

def test_find_patient_by_id():

    result = find_patient_by_id.invoke({
        "patient_id": "P001"
    })

    assert result is not None
    assert result["patient_id"] == "P001"
    assert result["name"] == "Arpan Chakraborty"
    assert result["email"] == "arpan@example.com"


def test_find_patient_by_id_not_found():

    result = find_patient_by_id.invoke({
        "patient_id": "BAD"
    })

    assert result is None


# ============================================================
# FIND PATIENT BY EMAIL
# ============================================================

def test_find_patient_by_email():

    result = find_patient_by_email.invoke({
        "email": "arpan@example.com"
    })

    assert result is not None
    assert result["patient_id"] == "P001"
    assert result["name"] == "Arpan Chakraborty"


def test_find_patient_by_email_case_insensitive():

    result = find_patient_by_email.invoke({
        "email": "ARPAN@EXAMPLE.COM"
    })

    assert result is not None
    assert result["patient_id"] == "P001"


def test_find_patient_by_email_not_found():

    result = find_patient_by_email.invoke({
        "email": "unknown@example.com"
    })

    assert result is None