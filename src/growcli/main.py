"""
Main entry point for GroqCLI-Chatbot - Enhanced Edition.

Provides the interactive terminal chat loop with advanced features:
- Conversation save/load
- Templates
- Enhanced input with multi-line support
- Syntax highlighting
- Keyboard shortcuts
- Progress indicators
"""

import sys
import atexit
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from growcli import __version__, __app_name__
from growcli.config import load_settings
from growcli.chat_engine import ChatEngine
from growcli.prompts import WELCOME_MESSAGE, HELP_TEXT
from growcli.utils import (
    print_bot_response,
    print_error,
    print_info,
    print_welcome,
    console,
)

# Import new modules
from growcli.conversation_manager import ConversationManager
from growcli.templates import TemplateManager
from growcli.input_handler import create_input_handler
from growcli.syntax_highlighter import SyntaxHighlighter


# Commands that trigger special actions
QUIT_COMMANDS = {"/quit", "/exit", "/q"}

# Global instances (initialized in app())
conversation_manager: ConversationManager = None
template_manager: TemplateManager = None
input_handler = None
syntax_highlighter: SyntaxHighlighter = None


def handle_command(
    command: str,
    engine: ChatEngine,
) -> bool:
    """
    Handle slash commands with enhanced features.

    Args:
        command: The command string (e.g., "/help").
        engine: The chat engine instance.

    Returns:
        bool: True if the app should continue, False to quit.
    """
    global conversation_manager, template_manager, syntax_highlighter
    
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # ═══════════════════════════════════════════════════════════
    # Basic Commands
    # ═══════════════════════════════════════════════════════════
    
    if cmd in QUIT_COMMANDS:
        return False

    elif cmd == "/help" or cmd == "/h":
        show_help()

    elif cmd == "/clear" or cmd == "/c":
        engine.clear_history()
        conversation_manager.current_conversation = []
        console.clear()
        print_info("🧹 Conversation history cleared. Starting fresh!")

    elif cmd == "/history":
        print_info(engine.get_history_display())

    elif cmd == "/model" or cmd == "/m":
        print_info(engine.get_model_info())

    elif cmd == "/stats" or cmd == "/s":
        print_info(f"\n{conversation_manager.get_conversation_summary()}")

    # ═══════════════════════════════════════════════════════════
    # Conversation Management Commands
    # ═══════════════════════════════════════════════════════════
    
    elif cmd == "/save":
        format_type = args.lower() if args else "json"
        
        if format_type == "json":
            filepath = conversation_manager.save_json()
        elif format_type in ["md", "markdown"]:
            filepath = conversation_manager.save_markdown()
        elif format_type in ["txt", "text"]:
            filepath = conversation_manager.save_text()
        else:
            print_error(f"Unknown format: {format_type}. Use: json, md, or txt")
            return True
        
        print_info(f"💾 Conversation saved to: {filepath}")

    elif cmd == "/load":
        if not args:
            conversations = conversation_manager.list_conversations()
            if conversations:
                print_info("\n📂 Available conversations:")
                for i, conv in enumerate(conversations[:10], 1):
                    print_info(f"  {i}. {Path(conv).name}")
                print_info("\n💡 Usage: /load <filename>")
            else:
                print_info("No saved conversations found.")
        else:
            filepath = args if "/" in args or "\\" in args else f"conversations/{args}"
            if conversation_manager.load_conversation(filepath):
                for msg in conversation_manager.current_conversation:
                    if msg.role in ["user", "assistant"]:
                        from growcli.chat_engine import Message
                        engine.history.append(Message(role=msg.role, content=msg.content))

    elif cmd == "/list":
        conversations = conversation_manager.list_conversations()
        if conversations:
            table = Table(title="📂 Saved Conversations")
            table.add_column("#", style="cyan")
            table.add_column("Filename", style="green")
            
            for i, conv in enumerate(conversations[:20], 1):
                path = Path(conv)
                table.add_row(str(i), path.name)
            
            console.print(table)
        else:
            print_info("No saved conversations found.")

    # ═══════════════════════════════════════════════════════════
    # Template Commands
    # ═══════════════════════════════════════════════════════════
    
    elif cmd == "/template" or cmd == "/t":
        if not args:
            console.print(template_manager.format_template_list())
        else:
            template = template_manager.get_template(args)
            if template:
                print_info(f"📋 Using template: {template.name}")
                print_info(f"   {template.description}\n")
                return True
            else:
                print_error(f"Template not found: {args}")

    elif cmd == "/templates":
        print_info(template_manager.format_template_list())

    # ═══════════════════════════════════════════════════════════
    # UI Commands
    # ═══════════════════════════════════════════════════════════
    
    elif cmd == "/cls" or cmd == "/clear-screen":
        console.clear()

    else:
        print_error(f"Unknown command: {cmd}. Type /help for available commands.")

    return True


def show_help():
    """Display clean, professional help message."""
    help_text = """
[bold cyan]═══════════════════════════════════════════════════════════════════[/bold cyan]
[bold cyan]                    GroqCLI-Chatbot Commands                        [/bold cyan]
[bold cyan]═══════════════════════════════════════════════════════════════════[/bold cyan]

[bold yellow]Basic Commands:[/bold yellow]
  /help, /h              Show this help
  /clear, /c             Clear conversation history
  /quit, /exit, /q       Exit chatbot

[bold yellow]Templates:[/bold yellow]
  /templates             List all 5 templates
  /template <name>       Use a template (e.g., /template code)
  /t <name>              Short form

[bold yellow]Conversation:[/bold yellow]
  /save [format]         Save conversation (json/md/txt)
  /load [file]           Load conversation
  /list                  List saved conversations

[bold yellow]Info:[/bold yellow]
  /history               Show conversation history
  /model, /m             Show model info
  /stats, /s             Show session statistics

[bold yellow]Available Templates:[/bold yellow]
  [cyan]code[/cyan]      - Write code
  [cyan]debug[/cyan]     - Fix errors
  [cyan]review[/cyan]    - Review code
  [cyan]explain[/cyan]   - Learn concepts
  [cyan]summarize[/cyan] - Summarize content

[dim]💡 Tip: End line with \\ to continue on next line[/dim]
[bold cyan]═══════════════════════════════════════════════════════════════════[/bold cyan]
"""
    console.print(help_text)


@click.command()
@click.option(
    "--model",
    default=None,
    help="Override the GroqCloud model (e.g., llama-3.1-8b-instant)",
)
@click.option(
    "--temperature",
    default=None,
    type=float,
    help="Override temperature (0.0 - 2.0)",
)
@click.option(
    "--no-highlight",
    is_flag=True,
    help="Disable syntax highlighting",
)
@click.version_option(version=__version__, prog_name=__app_name__)
def app(model: str | None, temperature: float | None, no_highlight: bool) -> None:
    """🤖 GroqCLI-Chatbot — Your AI assistant in the terminal with advanced features."""

    global conversation_manager, template_manager, input_handler, syntax_highlighter

    # Import banner module
    from growcli.banner import show_animated_banner
    
    # Show beautiful banner (clean, no extra text)
    show_animated_banner()
    
    # Simple loading - no verbose output
    import time
    
    # Load configuration silently
    settings = load_settings()
    
    # Apply CLI overrides
    if model:
        settings.groq_model = model
    if temperature is not None:
        settings.temperature = temperature
    
    # Initialize everything silently
    engine = ChatEngine(settings)
    conversation_manager = ConversationManager()
    conversation_manager.start_session(settings.groq_model, settings.temperature)
    template_manager = TemplateManager()
    input_handler = create_input_handler([
        "/help", "/clear", "/history", "/model", "/stats", "/quit",
        "/save", "/load", "/list", "/template", "/templates",
        "/cls", "/clear-screen"
    ])
    syntax_highlighter = SyntaxHighlighter() if not no_highlight else None
    
    # Register auto-save on exit
    def auto_save_on_exit():
        if len(conversation_manager.current_conversation) > 0:
            conversation_manager.auto_save()
    
    atexit.register(auto_save_on_exit)

    # ── Display Simple Help Commands ─────────────────
    console.print()
    console.print("[bold cyan]Quick Commands:[/bold cyan]")
    console.print("  [cyan]/templates[/cyan] - View templates  |  [cyan]/help[/cyan] - All commands  |  [cyan]/quit[/cyan] - Exit")
    console.print()
    console.print("─" * 70)
    console.print()

    # ── Main Chat Loop ──────────────────────────────────────────
    try:
        while True:
            # Get user input
            user_input = input_handler.get_input("\n👤 You: ")

            # Skip empty input
            if not user_input or not user_input.strip():
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                should_continue = handle_command(user_input, engine)
                if not should_continue:
                    break
                continue

            # Check if using template
            active_template = None
            if user_input.startswith("/t ") or user_input.startswith("/template "):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    template = template_manager.get_template(parts[1])
                    if template:
                        active_template = template
                        user_input = input_handler.get_input("   [dim]Your question:[/dim] ")
                        if not user_input:
                            continue
                        user_input = f"{template.prompt}\n\n{user_input}"

            # ── Send to AI and get response ─────────────────────
            response_text, metrics = engine.send_message(user_input)

            # Add to conversation manager
            conversation_manager.add_message(
                "user",
                user_input,
                metrics.prompt_tokens,
                0
            )
            conversation_manager.add_message(
                "assistant",
                response_text,
                metrics.completion_tokens,
                metrics.latency_seconds
            )

            # Display the response with clean, structured formatting
            if syntax_highlighter and "```" in response_text:
                # Response has code blocks - use structured format
                console.print(f"\n[bold green]🤖 {settings.chatbot_name}[/bold green] [dim]({metrics.latency_seconds:.2f}s)[/dim]")
                console.print("─" * 70)
                console.print()
                syntax_highlighter.format_response(response_text)
                console.print("─" * 70)
                console.print(f"[dim]💡 Tokens: {metrics.total_tokens} | Latency: {metrics.latency_seconds:.2f}s[/dim]\n")
            else:
                # Plain text response - use simple panel
                print_bot_response(
                    text=response_text,
                    bot_name=settings.chatbot_name,
                    latency=metrics.latency_seconds,
                )

    except KeyboardInterrupt:
        console.print("\n")

    # ── Cleanup ─────────────────────────────────────────────────
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    print_info(f"\n{conversation_manager.get_conversation_summary()}")
    
    # Auto-save
    if len(conversation_manager.current_conversation) > 0:
        conversation_manager.auto_save()
    
    goodbye_panel = Panel(
        f"[bold cyan]Thank you for using GroqCLI-Chatbot![/bold cyan]\n\n"
        f"Your conversation has been auto-saved.\n"
        f"Type [bold]uv run growcli[/bold] to start again.\n\n"
        f"[dim]� Quick commands for next time:[/dim]\n"
        f"[dim]  • /templates - See all templates[/dim]\n"
        f"[dim]  • /template code - Get coding help[/dim]\n"
        f"[dim]  • /save json - Save your work[/dim]\n"
        f"[dim]  • /help - Show all commands[/dim]",
        title="👋 Goodbye",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(goodbye_panel)
    console.print()


if __name__ == "__main__":
    app()
