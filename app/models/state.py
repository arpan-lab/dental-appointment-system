from typing import Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class DentalState(TypedDict):

    messages: Annotated[list[AnyMessage], add_messages]

    patient_id: Optional[str]

    intent: Optional[str]

    doctor_id: Optional[str]

    appointment_id: Optional[str]

    date: Optional[str]

    time: Optional[str]

    response: Optional[str]