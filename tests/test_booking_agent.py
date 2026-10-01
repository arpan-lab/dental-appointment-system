from types import SimpleNamespace

import pytest

import app.agents.booking as booking_agent_module


# ============================================================
# MOCK LLM
# ============================================================

class MockBookingLLM:

    def __init__(self, response_content):

        self.response_content = response_content
        self.received_messages = None

    def invoke(self, messages):

        self.received_messages = messages

        return SimpleNamespace(
            content=self.response_content
        )


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def mock_llm(monkeypatch):

    mock = MockBookingLLM(
        response_content="Appointment booked successfully."
    )

    monkeypatch.setattr(
        booking_agent_module,
        "booking_llm",
        mock
    )

    return mock


# ============================================================
# TEST 1: BOOKING AGENT RETURNS RESPONSE
# ============================================================

def test_booking_agent_returns_response(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="I want to book an appointment with an orthodontist."
            )
        ]
    }

    result = booking_agent_module.booking_agent(state)

    assert "messages" in result
    assert "response" in result

    assert result["response"] == (
        "Appointment booked successfully."
    )

    assert len(result["messages"]) == 1


# ============================================================
# TEST 2: USER MESSAGE REACHES LLM
# ============================================================

def test_booking_agent_passes_user_message(mock_llm):

    user_question = (
        "Book an appointment with doctor D002 "
        "on 2026-09-25 at 11:00."
    )

    state = {
        "messages": [
            SimpleNamespace(
                content=user_question
            )
        ]
    }

    booking_agent_module.booking_agent(state)

    assert mock_llm.received_messages is not None

    message_contents = [
        message.content
        for message in mock_llm.received_messages
    ]

    assert user_question in message_contents


# ============================================================
# TEST 3: SYSTEM PROMPT IS INCLUDED
# ============================================================

def test_booking_agent_includes_system_prompt(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="I want to book an appointment."
            )
        ]
    }

    booking_agent_module.booking_agent(state)

    assert mock_llm.received_messages is not None

    system_message = mock_llm.received_messages[0]

    assert isinstance(
        system_message.content,
        str
    )

    assert "Booking Agent" in system_message.content
    assert "Check whether the requested slot is available" in (
        system_message.content
    )


# ============================================================
# TEST 4: BOOKING RULES ARE PRESENT
# ============================================================

def test_booking_agent_has_required_booking_rules(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="I need a dental appointment."
            )
        ]
    }

    booking_agent_module.booking_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "Patient ID" in system_prompt
    assert "Doctor ID or specialization" in system_prompt
    assert "Date" in system_prompt
    assert "Time" in system_prompt

    assert "Never ask the patient to provide an appointment ID" in (
        system_prompt
    )

    assert "application automatically generates the appointment ID" in (
        system_prompt
    )


# ============================================================
# TEST 5: RESPONSE IS PRESERVED
# ============================================================

def test_booking_agent_preserves_llm_response(monkeypatch):

    expected_response = (
        "The requested slot is unavailable. "
        "Please choose another time."
    )

    mock = MockBookingLLM(
        response_content=expected_response
    )

    monkeypatch.setattr(
        booking_agent_module,
        "booking_llm",
        mock
    )

    state = {
        "messages": [
            SimpleNamespace(
                content="Book D002 tomorrow at 11 AM."
            )
        ]
    }

    result = booking_agent_module.booking_agent(state)

    assert result["response"] == expected_response
    assert result["messages"][0].content == expected_response