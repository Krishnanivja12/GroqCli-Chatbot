"""
Utility functions for GroqCLI-Chatbot.

Provides text formatting, display helpers, and structured output.
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

# Custom theme for consistent styling
CUSTOM_THEME = Theme({
    "user": "cyan",
    "bot": "green",
    "error": "red",
    "info": "yellow",
    "command": "magenta",
})

console = Console(theme=CUSTOM_THEME)


def print_bot_response(text: str, bot_name: str, latency: float) -> None:
    """
    Display the bot's response with clean, structured formatting.
    
    Args:
        text: The response text (may contain markdown/code)
        bot_name: Name of the bot for the panel title
        latency: Response time in seconds
    """
    # Use Markdown for better structure
    md = Markdown(text)
    
    # Create panel with clear structure
    panel = Panel(
        md,
        title=f"🤖 {bot_name}",
        subtitle=f"⚡ {latency:.2f}s",
        border_style="green",
        padding=(1, 2),
    )
    
    console.print("\n")
    console.print(panel)
    console.print()


def print_structured_response(text: str, bot_name: str, latency: float) -> None:
    """
    Display response with enhanced structure for code blocks.
    
    Args:
        text: The response text
        bot_name: Bot name
        latency: Response time
    """
    import re
    
    # Check if response has code blocks
    has_code = '```' in text
    
    if has_code:
        # Print header
        console.print(f"\n[bold green]🤖 {bot_name}[/bold green] [dim]({latency:.2f}s)[/dim]")
        console.print("─" * 70)
        console.print()
        
        # Split by code blocks
        parts = re.split(r'```(\w+)?\n(.*?)```', text, flags=re.DOTALL)
        
        for i, part in enumerate(parts):
            if i % 3 == 0:
                # Regular text
                if part.strip():
                    md = Markdown(part.strip())
                    console.print(md)
                    console.print()
            elif i % 3 == 1:
                # Language identifier (stored for next part)
                language = part if part else 'text'
            elif i % 3 == 2:
                # Code block
                code = part.strip()
                if code:
                    console.print(f"[bold cyan]📝 {language.upper()} Code:[/bold cyan]")
                    console.print("─" * 70)
                    
                    # Print with line numbers for easy copying
                    for line_num, line in enumerate(code.split('\n'), 1):
                        console.print(f"[dim]{line_num:3d}[/dim] │ {line}")
                    
                    console.print("─" * 70)
                    console.print("[dim]💡 Tip: Select with mouse to copy[/dim]")
                    console.print()
        
        console.print("─" * 70)
        console.print()
    else:
        # No code blocks, use simple panel
        print_bot_response(text, bot_name, latency)


def print_error(message: str) -> None:
    """Display an error message."""
    console.print(f"\n[error]❌ {message}[/error]\n")


def print_info(message: str) -> None:
    """Display an informational message."""
    console.print(f"[info]{message}[/info]")


def print_success(message: str) -> None:
    """Display a success message."""
    console.print(f"[bold green]✅ {message}[/bold green]")


def print_welcome(welcome_text: str) -> None:
    """Display the welcome banner."""
    console.print(welcome_text, style="bold cyan")


def print_section_header(title: str) -> None:
    """Print a section header for better structure."""
    console.print(f"\n[bold cyan]{'═' * 70}[/bold cyan]")
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print(f"[bold cyan]{'═' * 70}[/bold cyan]\n")


def print_code_block(code: str, language: str = "text") -> None:
    """
    Print a code block with clear structure.
    
    Args:
        code: Code to display
        language: Programming language
    """
    console.print(f"\n[bold cyan]📝 {language.upper()} Code:[/bold cyan]")
    console.print("─" * 70)
    
    for line_num, line in enumerate(code.split('\n'), 1):
        console.print(f"[dim]{line_num:3d}[/dim] │ {line}")
    
    console.print("─" * 70)
    console.print("[dim]💡 Select with mouse to copy[/dim]\n")


def get_user_input(bot_name: str) -> str:
    """
    Get input from the user with a styled prompt.
    Handles multi-line input (lines ending with \\).
    
    Args:
        bot_name: Bot name to display in prompt context
        
    Returns:
        str: The complete user input
    """
    try:
        lines = []
        prompt = "\n👤 You: "
        while True:
            line = console.input(prompt)
            if line.endswith("\\"):
                lines.append(line[:-1])  # Remove the backslash
                prompt = "   ... "  # Continuation prompt
            else:
                lines.append(line)
                break
        return "\n".join(lines).strip()
    except EOFError:
        return "/quit"


def format_table_data(headers: list[str], rows: list[list[str]]) -> None:
    """
    Display data in a formatted table.
    
    Args:
        headers: Column headers
        rows: Data rows
    """
    from rich.table import Table
    
    table = Table(show_header=True, header_style="bold cyan")
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)
