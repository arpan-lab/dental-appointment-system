import pandas as pd
from datetime import datetime

from app.database.connection import SessionLocal
from app.models.db_patient import PatientDB
from app.models.db_doctor import DoctorDB
from app.models.db_appointment import AppointmentDB


def migrate_patients(session):
    df = pd.read_csv("app/data/patients.csv")

    for _, row in df.iterrows():
        patient = PatientDB(
            patient_id=row["patient_id"],
            name=row["name"],
            phone=str(row["phone"]),
            email=row["email"],
        )

        session.add(patient)

    print(f"Patients loaded: {len(df)}")


def migrate_doctors(session):
    df = pd.read_csv("app/data/doctors.csv")

    for _, row in df.iterrows():
        doctor = DoctorDB(
            doctor_id=row["doctor_id"],
            name=row["name"],
            specialization=row["specialization"],
            available_days=row["available_days"],
        )

        session.add(doctor)

    print(f"Doctors loaded: {len(df)}")


def migrate_appointments(session):
    df = pd.read_csv("app/data/appointments.csv")

    for _, row in df.iterrows():

        appointment_date = pd.to_datetime(
            row["date"],
            dayfirst=True
        ).date()

        appointment_time = pd.to_datetime(
            row["time"]
        ).time()

        appointment = AppointmentDB(
            appointment_id=row["appointment_id"],
            patient_id=row["patient_id"],
            doctor_id=row["doctor_id"],
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status=row["status"],
        )

        session.add(appointment)

    print(f"Appointments loaded: {len(df)}")


def migrate():
    session = SessionLocal()

    try:
        # Step 1: Insert patients
        migrate_patients(session)
        session.commit()

        # Step 2: Insert doctors
        migrate_doctors(session)
        session.commit()

        # Step 3: Insert appointments
        migrate_appointments(session)
        session.commit()

        print("\nMigration completed successfully! 🎉")

    except Exception as e:
        session.rollback()
        print("\nMigration failed!")
        print("Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    migrate()