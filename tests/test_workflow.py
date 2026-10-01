from langchain_core.messages import AIMessage

from app.graph.workflow import (
    build_workflow,
    route_from_supervisor,
    route_information,
    route_booking,
    route_cancellation,
    route_rescheduling,
)


# ============================================================
# SUPERVISOR ROUTING
# ============================================================

def test_route_from_supervisor_information():

    state = {
        "intent": "information"
    }

    assert route_from_supervisor(state) == "information"


def test_route_from_supervisor_booking():

    state = {
        "intent": "booking"
    }

    assert route_from_supervisor(state) == "booking"


def test_route_from_supervisor_cancellation():

    state = {
        "intent": "cancellation"
    }

    assert route_from_supervisor(state) == "cancellation"


def test_route_from_supervisor_rescheduling():

    state = {
        "intent": "rescheduling"
    }

    assert route_from_supervisor(state) == "rescheduling"


# ============================================================
# INFORMATION ROUTING
# ============================================================

def test_route_information_to_tools():

    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "list_doctors",
                "args": {},
                "id": "call_1",
            }
        ],
    )

    state = {
        "messages": [message]
    }

    assert route_information(state) == "tools"


def test_route_information_to_end():

    message = AIMessage(
        content="Here are the available doctors."
    )

    state = {
        "messages": [message]
    }

    assert route_information(state) == "end"


# ============================================================
# BOOKING ROUTING
# ============================================================

def test_route_booking_to_tools():

    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "check_slot_availability",
                "args": {},
                "id": "call_2",
            }
        ],
    )

    state = {
        "messages": [message]
    }

    assert route_booking(state) == "tools"


def test_route_booking_to_end():

    message = AIMessage(
        content="Please provide your patient ID."
    )

    state = {
        "messages": [message]
    }

    assert route_booking(state) == "end"


# ============================================================
# CANCELLATION ROUTING
# ============================================================

def test_route_cancellation_to_tools():

    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "find_appointment",
                "args": {},
                "id": "call_3",
            }
        ],
    )

    state = {
        "messages": [message]
    }

    assert route_cancellation(state) == "tools"


def test_route_cancellation_to_end():

    message = AIMessage(
        content="Please provide the appointment ID."
    )

    state = {
        "messages": [message]
    }

    assert route_cancellation(state) == "end"


# ============================================================
# RESCHEDULING ROUTING
# ============================================================

def test_route_rescheduling_to_tools():

    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "check_slot_availability",
                "args": {},
                "id": "call_4",
            }
        ],
    )

    state = {
        "messages": [message]
    }

    assert route_rescheduling(state) == "tools"


def test_route_rescheduling_to_end():

    message = AIMessage(
        content="Please provide the new date and time."
    )

    state = {
        "messages": [message]
    }

    assert route_rescheduling(state) == "end"


# ============================================================
# WORKFLOW BUILD
# ============================================================

def test_build_workflow():

    workflow = build_workflow()

    assert workflow is not None

    graph_nodes = workflow.get_graph().nodes

    expected_nodes = {
        "supervisor",
        "information",
        "booking",
        "cancellation",
        "rescheduling",
        "information_tools",
        "booking_tools",
        "cancellation_tools",
        "rescheduling_tools",
    }

    for node in expected_nodes:
        assert node in graph_nodes