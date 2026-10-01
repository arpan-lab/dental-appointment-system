from langchain_core.messages import HumanMessage, AIMessage

import app.agents.supervisor as supervisor_module
import app.agents.information as information_module
import app.agents.booking as booking_module
import app.agents.cancellation as cancellation_module
import app.agents.rescheduling as rescheduling_module

from app.graph.workflow import build_workflow


# ============================================================
# MOCK SUPERVISOR LLM
# ============================================================

class MockSupervisorLLM:

    def __init__(self, next_agent):
        self.next_agent = next_agent

    def invoke(self, messages):

        class Decision:

            def __init__(self, next_agent):
                self.content = (
                    '{"next_agent": "' + next_agent + '"}'
                )

        return Decision(self.next_agent)


# ============================================================
# MOCK SPECIALIST LLM
# ============================================================

class MockAgentLLM:

    def __init__(self, response):
        self.response = response

    def invoke(self, messages):
        return AIMessage(content=self.response)


# ============================================================
# HELPERS
# ============================================================

def create_state(message):

    return {
        "messages": [
            HumanMessage(content=message)
        ],
        "patient_id": None,
        "intent": None,
        "doctor_id": None,
        "appointment_id": None,
        "date": None,
        "time": None,
        "response": None,
    }


def create_config(thread_id):

    return {
        "configurable": {
            "thread_id": thread_id
        }
    }


# ============================================================
# INFORMATION
# ============================================================

def test_information_graph_execution(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("information"),
    )

    monkeypatch.setattr(
        information_module,
        "information_llm",
        MockAgentLLM(
            "Dr. Michael Smith is an Orthodontist."
        ),
    )

    workflow = build_workflow()

    result = workflow.invoke(
        create_state(
            "Tell me about orthodontists."
        ),
        config=create_config(
            "information-test"
        ),
    )

    assert result["intent"] == "information"
    assert result["response"] == (
        "Dr. Michael Smith is an Orthodontist."
    )


# ============================================================
# BOOKING
# ============================================================

def test_booking_graph_execution(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("booking"),
    )

    monkeypatch.setattr(
        booking_module,
        "booking_llm",
        MockAgentLLM(
            "Please provide your patient ID."
        ),
    )

    workflow = build_workflow()

    result = workflow.invoke(
        create_state(
            "I want to book a dental appointment."
        ),
        config=create_config(
            "booking-test"
        ),
    )

    assert result["intent"] == "booking"
    assert result["response"] == (
        "Please provide your patient ID."
    )


# ============================================================
# CANCELLATION
# ============================================================

def test_cancellation_graph_execution(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("cancellation"),
    )

    monkeypatch.setattr(
        cancellation_module,
        "cancellation_llm",
        MockAgentLLM(
            "Please provide the appointment ID."
        ),
    )

    workflow = build_workflow()

    result = workflow.invoke(
        create_state(
            "I want to cancel my appointment."
        ),
        config=create_config(
            "cancellation-test"
        ),
    )

    assert result["intent"] == "cancellation"
    assert result["response"] == (
        "Please provide the appointment ID."
    )


# ============================================================
# RESCHEDULING
# ============================================================

def test_rescheduling_graph_execution(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("rescheduling"),
    )

    monkeypatch.setattr(
        rescheduling_module,
        "rescheduling_llm",
        MockAgentLLM(
            "Please provide the new date and time."
        ),
    )

    workflow = build_workflow()

    result = workflow.invoke(
        create_state(
            "I want to reschedule my appointment."
        ),
        config=create_config(
            "rescheduling-test"
        ),
    )

    assert result["intent"] == "rescheduling"
    assert result["response"] == (
        "Please provide the new date and time."
    )


# ============================================================
# FINISH
# ============================================================

def test_finish_graph_execution(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("FINISH"),
    )

    workflow = build_workflow()

    result = workflow.invoke(
        create_state(
            "Thank you."
        ),
        config=create_config(
            "finish-test"
        ),
    )

    assert result["intent"] == "FINISH"