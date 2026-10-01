# 🦷 Dental Appointment Assistant

An **Agentic AI dental appointment management system** built with **LangGraph, LangChain, SQLAlchemy, MySQL, and Streamlit**.

The application uses a **multi-agent architecture** where specialized AI agents work together to understand user requests and perform appointment operations such as booking, cancellation, rescheduling, and doctor information lookup.

---

## ✨ Features

* 🤖 Multi-agent AI workflow using LangGraph
* 📅 Book dental appointments
* ❌ Cancel appointments
* 🔄 Reschedule appointments
* 👨‍⚕️ Find doctors by ID, name, or specialization
* 🗓️ Validate doctor availability by working day
* 🚫 Prevent duplicate appointment slots
* 👤 Manage patient information
* 🗄️ MySQL database integration
* 🔧 Tool-based agent execution
* 💬 Natural-language interaction
* 🖥️ Streamlit frontend
* 🧪 96 automated tests
* ✅ Service, tool, agent, workflow, and integration testing

---

## 🧠 Agentic AI Architecture

The system uses **LangGraph** to coordinate multiple specialized agents.

```text
                    User
                      │
                      ▼
              ┌───────────────┐
              │   Supervisor  │
              │     Agent     │
              └───────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Information   Booking    Cancellation
        Agent        Agent        Agent
          │           │           │
          │           ▼           │
          │      Appointment      │
          │         Tools         │
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
              Rescheduling Agent
                      │
                      ▼
                Service Layer
                      │
                      ▼
              SQLAlchemy / MySQL
```

The supervisor determines the user's intent and routes the request to the appropriate specialized agent.

---

## 🤖 Agents

### Supervisor Agent

Responsible for understanding the user's request and routing it to the appropriate agent.

Example:

```text
"Book me with Dr. Michael Smith tomorrow."
                │
                ▼
        Supervisor Agent
                │
                ▼
          Booking Agent
```

### Booking Agent

Handles:

* Doctor identification
* Patient identification
* Date and time extraction
* Slot availability
* Appointment creation

### Cancellation Agent

Handles:

* Finding appointments
* Validating appointment status
* Cancelling booked appointments

### Rescheduling Agent

Handles:

* Identifying the appointment
* Validating appointment status
* Checking the new slot
* Validating doctor availability
* Updating the appointment

### Information Agent

Handles informational requests such as:

```text
"What orthodontists are available?"
```

and retrieves doctor information from the database.

---

## 🔧 Agent Tools

Agents interact with the application through LangChain tools.

### Doctor Tools

```text
list_doctors
find_doctor_by_id
find_doctor_by_name
find_doctors_by_specialization
```

### Appointment Tools

```text
list_appointments
find_patient_appointments
find_appointment
check_slot_availability
create_appointment
cancel_existing_appointment
reschedule_existing_appointment
```

### Patient Tools

Patient information is retrieved through the patient service layer and database.

---

## 🗄️ Database

The application uses **MySQL** as the persistent database.

SQLAlchemy is used as the ORM/database abstraction layer.

Main entities:

```text
Patient
   │
   └── patient_id

Doctor
   │
   ├── doctor_id
   ├── name
   ├── specialization
   └── available_days

Appointment
   │
   ├── appointment_id
   ├── patient_id
   ├── doctor_id
   ├── date
   ├── time
   └── status
```

Appointment statuses include:

```text
booked
cancelled
```

---

## 🛡️ Business Validations

The service layer performs important validations before modifying the database.

### Patient validation

The system verifies that the patient exists.

### Doctor validation

The system verifies that the requested doctor exists.

### Doctor availability

Doctors can only receive appointments on their configured working days.

Example:

```text
Michael Smith
Specialization: Orthodontist
Available:
Tuesday | Thursday | Saturday
```

Therefore:

```text
2026-10-17 → Saturday → Available ✅

2026-10-19 → Monday → Not Available ❌
```

### Duplicate appointment protection

The system prevents two appointments from occupying the same doctor/date/time slot.

### Cancellation validation

Only booked appointments can be cancelled.

### Rescheduling validation

Only booked appointments can be rescheduled.

The new date/time is also validated against doctor availability and existing appointments.

---

## 🖥️ Frontend

The application provides a Streamlit-based chat interface.

The frontend provides:

* Patient selection
* Chat interface
* System status
* Appointment interaction
* Example prompts
* Assistant responses

Example requests:

```text
What orthodontists are available?

Book me with Dr. Michael Smith on 2026-10-17 at 10:00 AM.

Show my appointments.

Cancel my appointment A12356.

Reschedule my appointment A12355 to 2026-10-20 at 11:00 AM.
```

---

## 🏗️ Project Structure

```text
dental-appointment-system/
│
├── app/
│   │
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── booking.py
│   │   ├── cancellation.py
│   │   ├── rescheduling.py
│   │   └── information.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── llm/
│   │   └── model.py
│   │
│   ├── models/
│   │   ├── state.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── db_patient.py
│   │   ├── db_doctor.py
│   │   └── db_appointment.py
│   │
│   ├── services/
│   │   ├── patient_service.py
│   │   ├── doctor_service.py
│   │   └── appointment_service.py
│   │
│   └── tools/
│       ├── patient_tools.py
│       ├── doctor_tools.py
│       └── appointment_tools.py
│
├── frontend/
│   ├── app.py
│   ├── components.py
│   └── styles.py
│
├── tests/
│   ├── test_agents/
│   ├── test_tools/
│   ├── test_services/
│   ├── test_workflow/
│   └── test_integration/
│
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | Application development            |
| LangGraph     | Multi-agent workflow orchestration |
| LangChain     | LLM and tool integration           |
| SQLAlchemy    | ORM/database interaction           |
| MySQL         | Persistent data storage            |
| Streamlit     | Frontend interface                 |
| Pytest        | Automated testing                  |
| Pydantic      | Data validation                    |
| Python-dotenv | Environment configuration          |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd dental-appointment-system
```

### 2. Create a virtual environment

Using Python:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/dental_appointment
```

Add the required LLM configuration used by your project.

Do not commit `.env` to GitHub.

---

## 🗄️ Database Setup

Create the MySQL database:

```sql
CREATE DATABASE dental_appointment;
```

Configure the database connection in `.env`.

Then make sure the required tables are available before running the application.

---

## ▶️ Run the Application

From the project root:

```powershell
streamlit run frontend/app.py
```

The Streamlit interface will open in your browser.

---

## 🧪 Testing

The project contains automated tests covering services, tools, agents, workflow behavior, and integration scenarios.

Run:

```bash
pytest -v
```

Current test result:

```text
96 passed
```

Example:

```text
==============================

96 passed in 2.85s

==============================
```

---

## 💬 Example Workflow

### User

```text
Book P001 with Dr. Michael Smith
on 2026-10-17 at 10:00 AM.
```

### System

```text
Supervisor Agent
        ↓
Booking Agent
        ↓
Find Doctor
        ↓
Check Availability
        ↓
Create Appointment
        ↓
MySQL
```

### Result

```text
Appointment confirmed.

Appointment ID: A12356
Patient: P001
Doctor: Michael Smith (D002)
Date: 2026-10-17
Time: 10:00 AM
```

---

## 🔒 Error Handling

The application handles common appointment errors including:

```text
Patient not found
Doctor not found
Doctor unavailable on requested day
Appointment slot already booked
Appointment not found
Cancelled appointment cannot be cancelled again
Cancelled appointment cannot be rescheduled
Invalid appointment date/time
```

Application validation errors are converted into user-friendly responses in the frontend.

---

## 🎯 Project Goals

This project demonstrates how an **Agentic AI application** can combine:

```text
LLM
 ↓
LangGraph
 ↓
Specialized Agents
 ↓
Tools
 ↓
Service Layer
 ↓
SQLAlchemy
 ↓
MySQL
```

instead of relying on a single LLM response.

The agents use application tools to retrieve information and perform real database operations.

---

## 🔮 Future Improvements

Potential future enhancements include:

* Authentication and authorization
* Multiple patient accounts
* Doctor schedule management
* Appointment reminders
* Email/SMS notifications
* Calendar integration
* Production deployment
* Human-in-the-loop approval
* Improved observability and tracing
* More comprehensive conversational memory

---

## 👨‍💻 Project

**Dental Appointment Assistant**

Built as an **Agentic AI application** using LangGraph, LangChain, SQLAlchemy, MySQL, and Streamlit.

The project demonstrates multi-agent orchestration, tool calling, database-backed business logic, validation, and conversational appointment management.
