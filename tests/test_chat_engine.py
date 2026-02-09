"""Tests for the chat engine."""

import pytest
from unittest.mock import MagicMock, patch

from growcli.config import Settings
from growcli.chat_engine import ChatEngine, Message


@pytest.fixture
def mock_settings():
    """Create test settings."""
    return Settings(
        groq_api_key="gsk_test_key_for_testing",
        groq_model="llama-3.1-8b-instant",
        chatbot_name="TestBot",
        temperature=0.5,
        max_tokens=512,
        max_history=10,
    )


class TestChatEngine:
    """Test the ChatEngine class."""

    @patch("growcli.chat_engine.Groq")
    def test_initialization(self, mock_groq_class, mock_settings):
        """Engine should initialize with correct settings."""
        engine = ChatEngine(mock_settings)
        assert engine.model == "llama-3.1-8b-instant"
        assert engine.temperature == 0.5
        assert engine.max_tokens == 512
        assert len(engine.history) == 0

    @patch("growcli.chat_engine.Groq")
    def test_clear_history(self, mock_groq_class, mock_settings):
        """Clearing history should empty the list."""
        engine = ChatEngine(mock_settings)
        engine.history.append(Message(role="user", content="Hello"))
        engine.history.append(Message(role="assistant", content="Hi!"))
        assert len(engine.history) == 2

        engine.clear_history()
        assert len(engine.history) == 0

    @patch("growcli.chat_engine.Groq")
    def test_build_messages_includes_system(self, mock_groq_class, mock_settings):
        """Built messages should always start with system prompt."""
        engine = ChatEngine(mock_settings)
        messages = engine._build_messages()
        assert messages[0]["role"] == "system"
        assert "TestBot" in messages[0]["content"]

    @patch("growcli.chat_engine.Groq")
    def test_history_trimming(self, mock_groq_class, mock_settings):
        """History should be trimmed to max_history."""
        mock_settings.max_history = 4
        engine = ChatEngine(mock_settings)

        # Add 6 messages (3 pairs)
        for i in range(6):
            role = "user" if i % 2 == 0 else "assistant"
            engine.history.append(Message(role=role, content=f"msg {i}"))

        messages = engine._build_messages()
        # Should have: 1 system + 4 history (max_history) = 5
        assert len(messages) == 5

    @patch("growcli.chat_engine.Groq")
    def test_send_message_success(self, mock_groq_class, mock_settings):
        """Successful API call should return response and metrics."""
        # Mock the Groq client
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello! How can I help?"
        mock_response.usage.prompt_tokens = 50
        mock_response.usage.completion_tokens = 10
        mock_response.usage.total_tokens = 60
        mock_client.chat.completions.create.return_value = mock_response

        engine = ChatEngine(mock_settings)
        response, metrics = engine.send_message("Hi there!")

        assert response == "Hello! How can I help?"
        assert metrics.total_tokens == 60
        assert metrics.latency_seconds > 0
        assert len(engine.history) == 2  # user + assistant