from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from app.models.state import DentalState

from app.agents.supervisor import supervisor_agent

from app.agents.information import (
    information_agent,
    information_tools,
)

from app.agents.booking import (
    booking_agent,
    booking_tools,
)

from app.agents.cancellation import (
    cancellation_agent,
    cancellation_tools,
)

from app.agents.rescheduling import (
    rescheduling_agent,
    rescheduling_tools,
)


def build_workflow():

    graph = StateGraph(DentalState)

    # -------------------------
    # Agents
    # -------------------------

    graph.add_node("supervisor", supervisor_agent)

    graph.add_node(
        "information",
        information_agent,
    )

    graph.add_node(
        "booking",
        booking_agent,
    )

    graph.add_node(
        "cancellation",
        cancellation_agent,
    )

    graph.add_node(
        "rescheduling",
        rescheduling_agent,
    )

    # -------------------------
    # Tool Nodes
    # -------------------------

    graph.add_node(
        "information_tools",
        ToolNode(information_tools),
    )

    graph.add_node(
        "booking_tools",
        ToolNode(booking_tools),
    )

    graph.add_node(
        "cancellation_tools",
        ToolNode(cancellation_tools),
    )

    graph.add_node(
        "rescheduling_tools",
        ToolNode(rescheduling_tools),
    )

    # -------------------------
    # Start
    # -------------------------

    graph.add_edge(
        START,
        "supervisor",
    )

    # -------------------------
    # Supervisor Routing
    # -------------------------

    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "information": "information",
            "booking": "booking",
            "cancellation": "cancellation",
            "rescheduling": "rescheduling",
            "FINISH": END,
        },
    )

    # -------------------------
    # Information
    # -------------------------

    graph.add_conditional_edges(
        "information",
        route_information,
        {
            "tools": "information_tools",
            "end": END,
        },
    )

    graph.add_edge(
        "information_tools",
        "information",
    )

    # -------------------------
    # Booking
    # -------------------------

    graph.add_conditional_edges(
        "booking",
        route_booking,
        {
            "tools": "booking_tools",
            "end": END,
        },
    )

    graph.add_edge(
        "booking_tools",
        "booking",
    )

    # -------------------------
    # Cancellation
    # -------------------------

    graph.add_conditional_edges(
        "cancellation",
        route_cancellation,
        {
            "tools": "cancellation_tools",
            "end": END,
        },
    )

    graph.add_edge(
        "cancellation_tools",
        "cancellation",
    )

    # -------------------------
    # Rescheduling
    # -------------------------

    graph.add_conditional_edges(
        "rescheduling",
        route_rescheduling,
        {
            "tools": "rescheduling_tools",
            "end": END,
        },
    )

    graph.add_edge(
        "rescheduling_tools",
        "rescheduling",
    )

    # -------------------------
    # Compile with Memory
    # -------------------------

    memory = MemorySaver()

    return graph.compile(
        checkpointer=memory,
    )


# ============================================================
# Routing Functions
# ============================================================

def route_from_supervisor(state: DentalState):

    return state["intent"]


def route_information(state: DentalState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


def route_booking(state: DentalState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


def route_cancellation(state: DentalState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


def route_rescheduling(state: DentalState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"