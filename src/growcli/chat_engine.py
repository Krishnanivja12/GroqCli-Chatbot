"""
Chat Engine — Core logic for communicating with GroqCloud API.

Manages conversation history, sends messages, and returns responses
along with performance metrics. Optimized for fast loading.
"""

import time
from dataclasses import dataclass, field
from typing import Optional

from groq import Groq, APIError, APIConnectionError, RateLimitError

from growcli.config import Settings
from growcli.prompts import get_system_prompt


@dataclass
class InteractionMetrics:
    """Metrics for a single chat interaction."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_seconds: float = 0.0
    model: str = ""


@dataclass
class Message:
    """A single message in the conversation."""
    role: str  # "system", "user", or "assistant"
    content: str


class ChatEngine:
    """
    Manages conversations with the GroqCloud API.

    Handles:
    - Conversation history management
    - API communication with error handling
    - Token and latency tracking
    - Lazy loading for faster startup
    """

    def __init__(self, settings: Settings):
        """
        Initialize the chat engine with lazy loading.

        Args:
            settings: Application settings with API key, model, etc.
        """
        self.settings = settings
        self._client: Optional[Groq] = None  # Lazy loaded
        self.model = settings.groq_model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens
        self.max_history = settings.max_history

        # Initialize conversation with system prompt
        self.system_message = Message(
            role="system",
            content=get_system_prompt(settings.chatbot_name),
        )
        self.history: list[Message] = []

    @property
    def client(self) -> Groq:
        """
        Lazy load the Groq client on first use.
        This speeds up initial startup time.
        """
        if self._client is None:
            from rich.console import Console
            console = Console()
            console.print("  [cyan]🤖 Loading AI model (first time)...[/cyan]", end="")
            self._client = Groq(api_key=self.settings.groq_api_key)
            console.print(" [bold green]✓[/bold green]")
                
        return self._client

    def _build_messages(self) -> list[dict[str, str]]:
        """
        Build the messages list for the API call.

        Includes the system prompt + conversation history,
        trimmed to max_history to control token usage.
        """
        messages = [{"role": self.system_message.role, "content": self.system_message.content}]

        # Only keep the last N messages to avoid token overflow
        recent_history = self.history[-self.max_history :]
        for msg in recent_history:
            messages.append({"role": msg.role, "content": msg.content})

        return messages

    def send_message(self, user_input: str) -> tuple[str, InteractionMetrics]:
        """
        Send a user message and get the assistant's response.

        Args:
            user_input: The user's message text.

        Returns:
            tuple: (response_text, metrics)

        Raises:
            Various Groq exceptions on API failure (handled gracefully).
        """
        # Add user message to history
        self.history.append(Message(role="user", content=user_input))

        # Build the full message list
        messages = self._build_messages()

        # Time the API call with simple spinner
        start_time = time.perf_counter()

        try:
            # Simple spinner for API call
            from rich.console import Console
            console = Console()
            console.print("\n  [cyan]🤔 Thinking...[/cyan]", end="")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=False,
            )
            
            console.print(" [bold green]✓[/bold green]")
                
        except APIConnectionError:
            self.history.pop()  # Remove the failed user message
            return (
                "❌ Cannot connect to GroqCloud. Check your internet connection.",
                InteractionMetrics(),
            )
        except RateLimitError:
            self.history.pop()
            return (
                "⏳ Rate limit reached. Please wait a moment and try again.",
                InteractionMetrics(),
            )
        except APIError as e:
            self.history.pop()
            return (
                f"❌ API Error: {e.message}",
                InteractionMetrics(),
            )
        except Exception as e:
            self.history.pop()
            return (
                f"❌ Unexpected error: {str(e)}",
                InteractionMetrics(),
            )

        end_time = time.perf_counter()
        latency = end_time - start_time

        # Extract response
        assistant_message = response.choices[0].message.content
        self.history.append(Message(role="assistant", content=assistant_message))

        # Build metrics
        usage = response.usage
        metrics = InteractionMetrics(
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            latency_seconds=latency,
            model=self.model,
        )

        return assistant_message, metrics

    def clear_history(self) -> None:
        """Clear all conversation history."""
        self.history.clear()

    def get_history_display(self) -> str:
        """Get a formatted display of conversation history."""
        if not self.history:
            return "📭 No conversation history yet."

        lines = ["\n📜 Conversation History:\n" + "─" * 50]
        for i, msg in enumerate(self.history, 1):
            role_emoji = "👤 You" if msg.role == "user" else "🤖 Bot"
            # Truncate long messages for display
            content = msg.content[:150] + "..." if len(msg.content) > 150 else msg.content
            lines.append(f"  {i}. [{role_emoji}]: {content}")
        lines.append("─" * 50)
        return "\n".join(lines)

    def get_model_info(self) -> str:
        """Get current model configuration display."""
        return (
            f"\n🧠 Model Information:\n"
            f"   Model       : {self.model}\n"
            f"   Temperature : {self.temperature}\n"
            f"   Max Tokens  : {self.max_tokens}\n"
            f"   History Len : {len(self.history)} messages\n"
            f"   Max History : {self.max_history} messages\n"
        )