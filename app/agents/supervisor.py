import json
from typing import Literal

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from app.llm.model import get_llm


llm = get_llm()


class SupervisorDecision(BaseModel):

    next_agent: Literal[
        "information",
        "booking",
        "cancellation",
        "rescheduling",
        "FINISH",
    ] = Field(
        description="The specialist agent that should handle the user's request."
    )


supervisor_llm = llm.bind(
    response_format={
        "type": "json_object"
    }
)


SYSTEM_PROMPT = """
You are the Supervisor Agent for a dental appointment system.

Your ONLY job is to decide which specialist agent should handle
the user's request.

You MUST return ONLY valid JSON.

The JSON must have exactly this format:

{
    "next_agent": "booking"
}

Allowed values for next_agent are:

"information"
"booking"
"cancellation"
"rescheduling"
"FINISH"

Available agents:

information:
- Doctor information
- Dentist specializations
- Doctor availability
- Finding doctors

booking:
- Creating a new appointment
- Booking an appointment
- Continuing an incomplete booking conversation
- Providing missing information for an appointment

cancellation:
- Cancelling an existing appointment
- Continuing an incomplete cancellation conversation

rescheduling:
- Changing the date or time of an existing appointment
- Continuing an incomplete rescheduling conversation

FINISH:
- Goodbye
- Thank you
- Conversation is complete
- No specialist action is required

IMPORTANT:

Use the entire conversation history.

If the conversation is already about booking and the user
provides a continuation such as:

- "yes"
- "okay"
- "P001"
- "tomorrow"
- "at 3 PM"
- "that works"
- "1"
- "I want that doctor"

then route to:

"booking"

If the conversation is about cancellation and the user
provides additional information, route to:

"cancellation"

If the conversation is about rescheduling and the user
provides additional information, route to:

"rescheduling"

If the user asks about doctors, specializations, or availability,
route to:

"information"

If the user says goodbye or thanks the assistant and no
specialist action is required, route to:

"FINISH"

NEVER answer the user.

NEVER ask the user a question.

NEVER include explanations.

RETURN ONLY JSON.
"""


def supervisor_agent(state):

    messages = state["messages"]

    response = supervisor_llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]
    )

    try:
        data = json.loads(response.content)

        decision = SupervisorDecision(
            next_agent=data["next_agent"]
        )

    except (json.JSONDecodeError, KeyError, ValueError):

        decision = SupervisorDecision(
            next_agent="FINISH"
        )

    return {
        "intent": decision.next_agent,
    }

