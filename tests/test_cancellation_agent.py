from types import SimpleNamespace

import pytest

import app.agents.cancellation as cancellation_agent_module


# ============================================================
# MOCK LLM
# ============================================================

class MockCancellationLLM:

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

    mock = MockCancellationLLM(
        response_content="Appointment A001 cancelled successfully."
    )

    monkeypatch.setattr(
        cancellation_agent_module,
        "cancellation_llm",
        mock
    )

    return mock


# ============================================================
# TEST 1: CANCELLATION AGENT RETURNS RESPONSE
# ============================================================

def test_cancellation_agent_returns_response(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="Cancel my appointment A001."
            )
        ]
    }

    result = cancellation_agent_module.cancellation_agent(state)

    assert "messages" in result
    assert "response" in result

    assert result["response"] == (
        "Appointment A001 cancelled successfully."
    )

    assert len(result["messages"]) == 1


# ============================================================
# TEST 2: USER MESSAGE REACHES LLM
# ============================================================

def test_cancellation_agent_passes_user_message(mock_llm):

    user_question = (
        "Please cancel my appointment A002."
    )

    state = {
        "messages": [
            SimpleNamespace(
                content=user_question
            )
        ]
    }

    cancellation_agent_module.cancellation_agent(state)

    assert mock_llm.received_messages is not None

    message_contents = [
        message.content
        for message in mock_llm.received_messages
    ]

    assert user_question in message_contents


# ============================================================
# TEST 3: SYSTEM PROMPT IS INCLUDED
# ============================================================

def test_cancellation_agent_includes_system_prompt(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="I want to cancel an appointment."
            )
        ]
    }

    cancellation_agent_module.cancellation_agent(state)

    assert mock_llm.received_messages is not None

    system_message = mock_llm.received_messages[0]

    assert isinstance(
        system_message.content,
        str
    )

    assert "Cancellation Agent" in system_message.content
    assert "cancel existing appointments" in (
        system_message.content
    )


# ============================================================
# TEST 4: CANCELLATION RULES ARE PRESENT
# ============================================================

def test_cancellation_agent_has_required_rules(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="Cancel my appointment."
            )
        ]
    }

    cancellation_agent_module.cancellation_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "appointment ID" in system_prompt
    assert "patient ID" in system_prompt
    assert "find their appointments" in system_prompt
    assert "Only cancel an existing booked appointment" in (
        system_prompt
    )

    assert "Do not invent appointment information" in (
        system_prompt
    )


# ============================================================
# TEST 5: MULTIPLE APPOINTMENTS RULE
# ============================================================

def test_cancellation_agent_handles_multiple_appointments_rule(
    mock_llm
):

    state = {
        "messages": [
            SimpleNamespace(
                content="I have multiple appointments."
            )
        ]
    }

    cancellation_agent_module.cancellation_agent(state)

    system_prompt = (
        mock_llm.received_messages[0].content
    )

    assert "multiple appointments" in system_prompt
    assert "ask for clarification" in system_prompt


# ============================================================
# TEST 6: RESPONSE IS PRESERVED
# ============================================================

def test_cancellation_agent_preserves_llm_response(
    monkeypatch
):

    expected_response = (
        "The appointment does not exist."
    )

    mock = MockCancellationLLM(
        response_content=expected_response
    )

    monkeypatch.setattr(
        cancellation_agent_module,
        "cancellation_llm",
        mock
    )

    state = {
        "messages": [
            SimpleNamespace(
                content="Cancel appointment BAD123."
            )
        ]
    }

    result = cancellation_agent_module.cancellation_agent(state)

    assert result["response"] == expected_response
    assert result["messages"][0].content == expected_response