
import pytest

import app.services.patient_service as patient_service


def test_get_all_patients():

    patients = patient_service.get_all_patients()

    assert len(patients) >= 4

    patient_ids = [
        patient["patient_id"]
        for patient in patients
    ]

    assert "P001" in patient_ids


def test_get_patient_by_id():

    patient = patient_service.get_patient_by_id(
        "P001"
    )

    assert patient is not None
    assert patient["patient_id"] == "P001"
    assert patient["name"] == "Arpan Chakraborty"
    assert patient["email"] == "arpan@example.com"


def test_get_patient_by_id_not_found():

    patient = patient_service.get_patient_by_id(
        "BAD"
    )

    assert patient is None


def test_get_patient_by_email():

    patient = patient_service.get_patient_by_email(
        "arpan@example.com"
    )

    assert patient is not None
    assert patient["patient_id"] == "P001"
    assert patient["name"] == "Arpan Chakraborty"


def test_get_patient_by_email_case_insensitive():

    patient = patient_service.get_patient_by_email(
        "ARPAN@EXAMPLE.COM"
    )

    assert patient is not None
    assert patient["patient_id"] == "P001"


def test_get_patient_by_email_not_found():

    patient = patient_service.get_patient_by_email(
        "unknown@example.com"
    )

    assert patient is None