from langchain_core.messages import SystemMessage

from app.llm.model import get_llm

from app.tools.doctor_tools import (
    list_doctors,
    find_doctor_by_id,
    find_doctors_by_specialization,
)


llm = get_llm()


information_tools = [
    list_doctors,
    find_doctor_by_id,
    find_doctors_by_specialization,
]


information_llm = llm.bind_tools(
    information_tools
)


SYSTEM_PROMPT = """
You are the Information Agent for a dental appointment system.

Your responsibilities are:

1. Answer questions about dentists.
2. Find doctors by specialization.
3. Find doctors using doctor ID.
4. Provide doctor availability information.

Use the available tools whenever actual doctor information
is required.

Do not invent doctors, specializations, or availability.

If the requested doctor or specialization does not exist,
clearly tell the patient.

Keep responses concise and helpful.
"""


def information_agent(state):

    messages = state["messages"]

    response = information_llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {
        "messages": [response],
        "response": response.content,
    }