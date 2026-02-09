import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv


def _find_dotenv() -> Path | None:
    """Walk up directories to find .env file."""
    current = Path.cwd()
    while current != current.parent:
        env_path = current / ".env"
        if env_path.exists():
            return env_path
        current = current.parent
    return None


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    # GroqCloud
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Chatbot behavior
    chatbot_name: str = "Atlas"
    max_history: int = 20
    temperature: float = 0.7
    max_tokens: int = 1024

    def validate(self) -> list[str]:
        """Validate required settings. Returns list of error messages."""
        errors = []
        if not self.groq_api_key:
            errors.append("GROQ_API_KEY is required. Get one at https://console.groq.com/keys")
        if not self.groq_api_key.startswith("gsk_") and self.groq_api_key:
            errors.append("GROQ_API_KEY should start with 'gsk_'. Check your key.")
        if self.temperature < 0 or self.temperature > 2:
            errors.append(f"CHATBOT_TEMPERATURE must be 0-2, got {self.temperature}")
        if self.max_tokens < 1:
            errors.append(f"CHATBOT_MAX_TOKENS must be positive, got {self.max_tokens}")
        return errors


def load_settings() -> Settings:
    """
    Load settings from environment variables / .env file.

    Returns:
        Settings: Validated application settings.

    Raises:
        SystemExit: If required settings are missing.
    """
    # Load .env file
    dotenv_path = _find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)

    settings = Settings(
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        chatbot_name=os.getenv("CHATBOT_NAME", "Atlas"),
        max_history=int(os.getenv("CHATBOT_MAX_HISTORY", "20")),
        temperature=float(os.getenv("CHATBOT_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("CHATBOT_MAX_TOKENS", "1024")),
    )

    # Validate
    errors = settings.validate()
    if errors:
        print("\n❌ Configuration Error(s):")
        for err in errors:
            print(f"   • {err}")
        print("\n💡 Tip: Copy .env.example to .env and fill in your values:")
        print("   cp .env.example .env\n")
        sys.exit(1)

    return settings