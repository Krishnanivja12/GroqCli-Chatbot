"""Tests for the configuration module."""

import os
import pytest
from unittest.mock import patch

from growcli.config import Settings, load_settings


class TestSettings:
    """Test the Settings dataclass validation."""

    def test_valid_settings(self):
        """Settings with all required fields should pass validation."""
        settings = Settings(
            groq_api_key="gsk_test_key_12345",
            groq_model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        errors = settings.validate()
        assert errors == [], f"Expected no errors, got: {errors}"

    def test_missing_api_key(self):
        """Missing API key should produce an error."""
        settings = Settings(groq_api_key="")
        errors = settings.validate()
        assert len(errors) >= 1
        assert "GROQ_API_KEY" in errors[0]

    def test_invalid_api_key_prefix(self):
        """API key not starting with 'gsk_' should warn."""
        settings = Settings(groq_api_key="invalid_key_format")
        errors = settings.validate()
        assert any("gsk_" in err for err in errors)

    def test_invalid_temperature(self):
        """Temperature outside 0-2 range should error."""
        settings = Settings(
            groq_api_key="gsk_valid_key",
            temperature=5.0,
        )
        errors = settings.validate()
        assert any("TEMPERATURE" in err.upper() for err in errors)

    def test_invalid_max_tokens(self):
        """Non-positive max_tokens should error."""
        settings = Settings(
            groq_api_key="gsk_valid_key",
            max_tokens=-1,
        )
        errors = settings.validate()
        assert any("MAX_TOKENS" in err.upper() for err in errors)


class TestLoadSettings:
    """Test loading settings from environment."""

    @patch.dict(os.environ, {
        "GROQ_API_KEY": "gsk_test_key_abc123",
        "GROQ_MODEL": "llama-3.1-8b-instant",
        "CHATBOT_NAME": "TestBot",
        "CHATBOT_TEMPERATURE": "0.5",
    })
    def test_load_from_environment(self):
        """Settings should load from environment variables."""
        settings = load_settings()
        assert settings.groq_api_key == "gsk_test_key_abc123"
        assert settings.groq_model == "llama-3.1-8b-instant"
        assert settings.chatbot_name == "TestBot"
        assert settings.temperature == 0.5