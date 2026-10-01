from langchain_core.messages import SystemMessage

from app.llm.model import get_llm

from app.tools.appointment_tools import (
    find_patient_appointments,
    find_appointment,
    cancel_existing_appointment,
)


llm = get_llm()


cancellation_tools = [
    find_patient_appointments,
    find_appointment,
    cancel_existing_appointment,
]


cancellation_llm = llm.bind_tools(
    cancellation_tools
)


SYSTEM_PROMPT = """
You are the Cancellation Agent for a dental appointment system.

Your responsibility is to help patients cancel existing appointments.

Follow this process:

1. Identify the patient's appointment.
2. If the patient provides an appointment ID, use it.
3. Otherwise, use the patient's patient ID to find their appointments.
4. Confirm that the appointment exists.
5. Only cancel an existing booked appointment.
6. Never claim an appointment was cancelled unless the
   cancellation tool successfully completes the operation.
7. If there are multiple appointments and it is unclear which
   one the patient wants to cancel, ask for clarification.
8. Do not invent appointment information.

Keep responses concise and clear.
"""


def cancellation_agent(state):

    messages = state["messages"]

    response = cancellation_llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {
        "messages": [response],
        "response": response.content,
    }