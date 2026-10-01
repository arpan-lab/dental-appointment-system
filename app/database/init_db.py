from app.database.connection import engine
from app.database.base import Base

# Import models so SQLAlchemy registers the tables
from app.models.db_patient import PatientDB
from app.models.db_doctor import DoctorDB
from app.models.db_appointment import AppointmentDB


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()