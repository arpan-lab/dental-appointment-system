from types import SimpleNamespace

import app.agents.supervisor as supervisor_module
import app.agents.information as information_module
import app.agents.booking as booking_module
import app.agents.cancellation as cancellation_module
import app.agents.rescheduling as rescheduling_module


# ============================================================
# MOCK SUPERVISOR
# ============================================================

class MockSupervisorLLM:

    def __init__(self, next_agent):
        self.next_agent = next_agent

    def invoke(self, messages):

        return SimpleNamespace(
            content=(
                '{"next_agent": "'
                + self.next_agent
                + '"}'
            )
        )


# ============================================================
# MOCK SPECIALIST LLM
# ============================================================

class MockAgentLLM:

    def __init__(self, response):
        self.response = response

    def invoke(self, messages):

        return SimpleNamespace(
            content=self.response,
            tool_calls=[]
        )


# ============================================================
# HELPER
# ============================================================

def setup_agent_mocks(
    monkeypatch,
    agent_name,
    response
):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM(agent_name)
    )

    if agent_name == "information":

        monkeypatch.setattr(
            information_module,
            "information_llm",
            MockAgentLLM(response)
        )

    elif agent_name == "booking":

        monkeypatch.setattr(
            booking_module,
            "booking_llm",
            MockAgentLLM(response)
        )

    elif agent_name == "cancellation":

        monkeypatch.setattr(
            cancellation_module,
            "cancellation_llm",
            MockAgentLLM(response)
        )

    elif agent_name == "rescheduling":

        monkeypatch.setattr(
            rescheduling_module,
            "rescheduling_llm",
            MockAgentLLM(response)
        )


# ============================================================
# TEST 1: INFORMATION FLOW
# ============================================================

def test_information_integration(monkeypatch):

    setup_agent_mocks(
        monkeypatch,
        "information",
        "Dr. Michael Smith is an Orthodontist."
    )

    supervisor_result = (
        supervisor_module.supervisor_agent({
            "messages": [
                SimpleNamespace(
                    content="Tell me about orthodontists."
                )
            ]
        })
    )

    assert supervisor_result["intent"] == "information"

    result = information_module.information_agent({
        "messages": [
            SimpleNamespace(
                content="Tell me about orthodontists."
            )
        ]
    })

    assert result["response"] == (
        "Dr. Michael Smith is an Orthodontist."
    )


# ============================================================
# TEST 2: BOOKING FLOW
# ============================================================

def test_booking_integration(monkeypatch):

    setup_agent_mocks(
        monkeypatch,
        "booking",
        "Appointment booked successfully."
    )

    supervisor_result = (
        supervisor_module.supervisor_agent({
            "messages": [
                SimpleNamespace(
                    content="Book an appointment with D002."
                )
            ]
        })
    )

    assert supervisor_result["intent"] == "booking"

    result = booking_module.booking_agent({
        "messages": [
            SimpleNamespace(
                content="Book an appointment with D002."
            )
        ]
    })

    assert result["response"] == (
        "Appointment booked successfully."
    )


# ============================================================
# TEST 3: CANCELLATION FLOW
# ============================================================

def test_cancellation_integration(monkeypatch):

    setup_agent_mocks(
        monkeypatch,
        "cancellation",
        "Appointment A001 cancelled successfully."
    )

    supervisor_result = (
        supervisor_module.supervisor_agent({
            "messages": [
                SimpleNamespace(
                    content="Cancel appointment A001."
                )
            ]
        })
    )

    assert supervisor_result["intent"] == "cancellation"

    result = cancellation_module.cancellation_agent({
        "messages": [
            SimpleNamespace(
                content="Cancel appointment A001."
            )
        ]
    })

    assert result["response"] == (
        "Appointment A001 cancelled successfully."
    )


# ============================================================
# TEST 4: RESCHEDULING FLOW
# ============================================================

def test_rescheduling_integration(monkeypatch):

    setup_agent_mocks(
        monkeypatch,
        "rescheduling",
        "Appointment A001 rescheduled successfully."
    )

    supervisor_result = (
        supervisor_module.supervisor_agent({
            "messages": [
                SimpleNamespace(
                    content="Move appointment A001 to tomorrow."
                )
            ]
        })
    )

    assert supervisor_result["intent"] == "rescheduling"

    result = rescheduling_module.rescheduling_agent({
        "messages": [
            SimpleNamespace(
                content="Move appointment A001 to tomorrow."
            )
        ]
    })

    assert result["response"] == (
        "Appointment A001 rescheduled successfully."
    )


# ============================================================
# TEST 5: FINISH ROUTING
# ============================================================

def test_supervisor_finish(monkeypatch):

    monkeypatch.setattr(
        supervisor_module,
        "supervisor_llm",
        MockSupervisorLLM("FINISH")
    )

    result = supervisor_module.supervisor_agent({
        "messages": [
            SimpleNamespace(
                content="Thank you."
            )
        ]
    })

    assert result["intent"] == "FINISH"