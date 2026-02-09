"""
Prompt templates for GroqCLI-Chatbot.

Centralizes all system prompts and makes personality tweaking easy.
"""


def get_system_prompt(bot_name: str) -> str:
    """
    Generate the system prompt that defines the chatbot's personality.

    Args:
        bot_name: The name the chatbot uses to identify itself.

    Returns:
        str: The system prompt string.
    """
    return f"""You are {bot_name}, a helpful, friendly, and knowledgeable AI assistant \
running in a terminal environment.

Your key traits:
- You are concise but thorough. Terminal users prefer shorter, well-structured answers.
- You use markdown formatting sparingly (bold for emphasis, code blocks for code).
- When showing code, always specify the language for syntax highlighting.
- You are honest about limitations and say "I don't know" when uncertain.
- You have a warm, professional personality with occasional light humor.
- You remember context from the current conversation.

When asked about yourself:
- Your name is {bot_name}
- You're powered by GroqCloud's ultra-fast inference
- You're a CLI chatbot built with Python

Guidelines for responses:
1. Keep responses focused and actionable
2. Use bullet points and numbered lists for clarity
3. For code questions, provide working examples
4. If a question is ambiguous, ask for clarification
"""


WELCOME_MESSAGE = """
╔══════════════════════════════════════════════════════╗
║           🤖  GroqCLI-Chatbot — {name}              ║
║                                                      ║
║   Type your message and press Enter to chat.         ║
║   Commands:                                          ║
║     /help    — Show available commands               ║
║     /clear   — Clear conversation history            ║
║     /history — Show conversation history             ║
║     /model   — Show current model info               ║
║     /stats   — Show session statistics               ║
║     /quit    — Exit the chatbot                      ║
╚══════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
📋 Available Commands:
  /help    — Show this help message
  /clear   — Clear conversation history and start fresh
  /history — Display the conversation so far
  /model   — Show which AI model is being used
  /stats   — Show session statistics (messages, tokens, latency)
  /quit    — Exit the chatbot (also: /exit, /q, Ctrl+C)

💡 Tips:
  • Multi-line input: End a line with \\ to continue
  • Ask follow-up questions — the bot remembers context
  • Be specific for better answers
"""