
from types import SimpleNamespace

import pytest

import app.agents.information as information_agent_module


# ============================================================
# MOCK LLM
# ============================================================


class MockInformationLLM:

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

    mock = MockInformationLLM(
        response_content="Dr. Michael Smith is an Orthodontist."
    )

    monkeypatch.setattr(
        information_agent_module,
        "information_llm",
        mock
    )

    return mock


# ============================================================
# TEST 1: INFORMATION AGENT RETURNS RESPONSE
# ============================================================


def test_information_agent_returns_response(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="Tell me about orthodontists."
            )
        ]
    }

    result = information_agent_module.information_agent(state)

    assert "messages" in result
    assert "response" in result

    assert result["response"] == (
        "Dr. Michael Smith is an Orthodontist."
    )

    assert len(result["messages"]) == 1


# ============================================================
# TEST 2: INFORMATION AGENT SENDS USER MESSAGE TO LLM
# ============================================================


def test_information_agent_passes_user_message(mock_llm):

    user_question = "Find doctors who are orthodontists."

    state = {
        "messages": [
            SimpleNamespace(
                content=user_question
            )
        ]
    }

    information_agent_module.information_agent(state)

    assert mock_llm.received_messages is not None

    message_contents = [
        message.content
        for message in mock_llm.received_messages
    ]

    assert user_question in message_contents


# ============================================================
# TEST 3: INFORMATION AGENT INCLUDES SYSTEM PROMPT
# ============================================================


def test_information_agent_includes_system_prompt(mock_llm):

    state = {
        "messages": [
            SimpleNamespace(
                content="List all available doctors."
            )
        ]
    }

    information_agent_module.information_agent(state)

    assert mock_llm.received_messages is not None

    system_message = mock_llm.received_messages[0]

    assert isinstance(
        system_message.content,
        str
    )

    assert "Information Agent" in system_message.content
    assert "Do not invent doctors" in system_message.content


# ============================================================
# TEST 4: INFORMATION AGENT PRESERVES RESPONSE CONTENT
# ============================================================


def test_information_agent_preserves_llm_response(monkeypatch):

    expected_response = (
        "No doctor with the requested specialization exists."
    )

    mock = MockInformationLLM(
        response_content=expected_response
    )

    monkeypatch.setattr(
        information_agent_module,
        "information_llm",
        mock
    )

    state = {
        "messages": [
            SimpleNamespace(
                content="Find a surgeon."
            )
        ]
    }

    result = information_agent_module.information_agent(state)

    assert result["response"] == expected_response
    assert result["messages"][0].content == expected_response