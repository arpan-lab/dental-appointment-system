from types import SimpleNamespace

import pytest

import app.agents.rescheduling as rescheduling_agent_module


# ============================================================
# MOCK LLM
# ============================================================

class MockReschedulingLLM:

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

    mock = MockReschedulingLLM(
        response_content="Appointment A001 rescheduled successfully."
    )

    monkeypatch.setattr(
        rescheduling_agent_module,
        "rescheduling_llm",
        mock
    )

    return mock


# ============================================================
# TEST 1: AGENT RETURNS RESPONSE
# ============================================================

def test_rescheduling_agent_returns_response(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="Reschedule appointment A001."
            )
        ]
    }

    result = rescheduling_agent_module.rescheduling_agent(state)

    assert "messages" in result
    assert "response" in result

    assert result["response"] == (
        "Appointment A001 rescheduled successfully."
    )

    assert len(result["messages"]) == 1


# ============================================================
# TEST 2: USER MESSAGE REACHES LLM
# ============================================================

def test_rescheduling_agent_passes_user_message(mock_llm):

    user_question = (
        "Reschedule appointment A001 "
        "to 2026-09-25 at 14:00."
    )

    state = {
        "messages": [
            SimpleNamespace(
                content=user_question
            )
        ]
    }

    rescheduling_agent_module.rescheduling_agent(state)

    assert mock_llm.received_messages is not None

    message_contents = [
        message.content
        for message in mock_llm.received_messages
    ]

    assert user_question in message_contents


# ============================================================
# TEST 3: SYSTEM PROMPT IS INCLUDED
# ============================================================

def test_rescheduling_agent_includes_system_prompt(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="I want to change my appointment."
            )
        ]
    }

    rescheduling_agent_module.rescheduling_agent(state)

    assert mock_llm.received_messages is not None

    system_message = mock_llm.received_messages[0]

    assert isinstance(
        system_message.content,
        str
    )

    assert "Rescheduling Agent" in system_message.content
    assert "change the date or time" in system_message.content


# ============================================================
# TEST 4: RESCHEDULING RULES ARE PRESENT
# ============================================================

def test_rescheduling_agent_has_required_rules(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="Change my appointment."
            )
        ]
    }

    rescheduling_agent_module.rescheduling_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "appointment ID" in system_prompt
    assert "patient ID" in system_prompt
    assert "new requested date and time" in system_prompt
    assert "Check whether the new slot is available" in (
        system_prompt
    )

    assert "Only reschedule if the new slot is available" in (
        system_prompt
    )


# ============================================================
# TEST 5: MULTIPLE APPOINTMENTS RULE
# ============================================================

def test_rescheduling_agent_handles_multiple_appointments_rule(
    mock_llm
):

    state = {
        "messages": [
            SimpleNamespace(
                content="I have multiple appointments."
            )
        ]
    }

    rescheduling_agent_module.rescheduling_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "multiple appointments" in system_prompt
    assert "ask the patient for clarification" in system_prompt


# ============================================================
# TEST 6: UNAVAILABLE SLOT RULE
# ============================================================

def test_rescheduling_agent_handles_unavailable_slot_rule(
    mock_llm
):

    state = {
        "messages": [
            SimpleNamespace(
                content="Move my appointment to another time."
            )
        ]
    }

    rescheduling_agent_module.rescheduling_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "requested slot is unavailable" in system_prompt
    assert "ask for another date or time" in system_prompt


# ============================================================
# TEST 7: RESPONSE IS PRESERVED
# ============================================================

def test_rescheduling_agent_preserves_llm_response(
    monkeypatch
):

    expected_response = (
        "The requested time slot is unavailable."
    )

    mock = MockReschedulingLLM(
        response_content=expected_response
    )

    monkeypatch.setattr(
        rescheduling_agent_module,
        "rescheduling_llm",
        mock
    )

    state = {
        "messages": [
            SimpleNamespace(
                content="Move appointment A001 to 10:00."
            )
        ]
    }

    result = rescheduling_agent_module.rescheduling_agent(state)

    assert result["response"] == expected_response
    assert result["messages"][0].content == expected_response