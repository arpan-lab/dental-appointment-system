
from langchain_core.messages import SystemMessage

from app.llm.model import get_llm

from app.tools.doctor_tools import (
    find_doctor_by_id,
    find_doctor_by_name,
    find_doctors_by_specialization,
)

from app.tools.appointment_tools import (
    check_slot_availability,
    create_appointment,
)


llm = get_llm()


booking_tools = [
    find_doctor_by_id,
    find_doctor_by_name,
    find_doctors_by_specialization,
    check_slot_availability,
    create_appointment,
]


booking_llm = llm.bind_tools(booking_tools)


SYSTEM_PROMPT = """
You are the Booking Agent for a dental appointment system.

Your responsibility is to help patients book dental appointments.

Follow this process:

1. Understand the patient's booking request.

2. Identify the doctor using the information provided:
   - If the patient provides a doctor name, use find_doctor_by_name.
   - If the patient provides a doctor ID, use find_doctor_by_id.
   - If the patient provides a specialization, use
     find_doctors_by_specialization.

3. Identify the patient ID.

4. Identify the requested date and time.

5. Check whether the requested slot is available.

6. Only create an appointment after confirming that the slot is available.

7. The application automatically generates the appointment ID.

8. Never ask the patient to provide an appointment ID.

9. Never invent doctor information or appointment availability.

10. Never claim that an appointment was booked unless the booking tool
    successfully creates it.

11. If required booking information is missing, ask the patient for it.

12. If the requested doctor cannot be found, clearly tell the patient
    that the doctor could not be found.



Required information:

- Patient ID
- Doctor ID or specialization
- Doctor name (if provided)
- Date
- Time

Keep responses concise and helpful.
"""


def booking_agent(state):

    messages = state["messages"]

    response = booking_llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {
        "messages": [response],
        "response": response.content,
    }

