from langchain_core.messages import SystemMessage

from app.llm.model import get_llm

from app.tools.appointment_tools import (
    find_patient_appointments,
    find_appointment,
    check_slot_availability,
    reschedule_existing_appointment,
)


llm = get_llm()


rescheduling_tools = [
    find_patient_appointments,
    find_appointment,
    check_slot_availability,
    reschedule_existing_appointment,
]


rescheduling_llm = llm.bind_tools(
    rescheduling_tools
)


SYSTEM_PROMPT = """
You are the Rescheduling Agent for a dental appointment system.

Your responsibility is to help patients change the date or time
of an existing appointment.

Follow this process:

1. Identify the patient's appointment.
2. If the patient provides an appointment ID, use it.
3. Otherwise, use the patient's patient ID to find their appointments.
4. Confirm that the appointment exists.
5. Identify the new requested date and time.
6. Check whether the new slot is available.
7. Only reschedule if the new slot is available.
8. Never claim an appointment was rescheduled unless the
   rescheduling tool successfully completes the operation.
9. If the requested slot is unavailable, tell the patient and
   ask for another date or time.
10. If multiple appointments exist and it is unclear which one
    should be changed, ask the patient for clarification.
11. Never invent appointment information.

Keep responses concise and clear.
"""


def rescheduling_agent(state):

    messages = state["messages"]

    response = rescheduling_llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {
        "messages": [response],
        "response": response.content,
    }