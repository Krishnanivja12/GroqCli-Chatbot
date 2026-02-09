import random
from rich.console import Console
from rich.text import Text

console = Console()

# =============================================================================
# LOGO (RAW – NO SPACING ASSUMPTIONS)
# =============================================================================

GROQ = [
    " ██████╗ ██████╗  ██████╗  ██████╗ ",
    "██╔════╝ ██╔══██╗██╔═══██╗██╔═══██╗",
    "██║  ███╗██████╔╝██║   ██║██║   ██║",
    "██║   ██║██╔══██╗██║   ██║██║▄▄ ██║",
    "╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝",
    " ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══▀▀═╝ ",
]

CLI = [
    " ██████╗██╗     ██╗",
    "██╔════╝██║     ██║",
    "██║     ██║     ██║",
    "██║     ██║     ██║",
    "╚██████╗███████╗██║",
    " ╚═════╝╚══════╝╚═╝",
]

TAGLINE = "AI-Powered Command Line Chatbot"

STARTUP_TIPS = [
    "Tip: Use /help to view commands",
    "Tip: Use /templates to explore templates",
    "Tip: Use /save json to export chat history",
    "Tip: Press Ctrl+C to exit",
]

# =============================================================================
# CORE RENDERER
# =============================================================================

def show_banner(style="cyan"):
    console.clear()

    combined = [f"{g} {c}" for g, c in zip(GROQ, CLI)]
    content_width = max(len(line) for line in combined + [TAGLINE])
    box_width = content_width + 8

    def border(top=True):
        char = "═"
        return f"{'╔' if top else '╚'}{char * (box_width - 2)}{'╗' if top else '╝'}"

    console.print()
    console.print(border(True), style=f"bold {style}")

    console.print(f"║{' ' * (box_width - 2)}║", style=f"bold {style}")

    for g, c in zip(GROQ, CLI):
        text = Text()
        text.append(g, style=f"bold {style}")
        text.append(" ")
        text.append(c, style="bold white")

        padded = text.plain.ljust(content_width)
        console.print(
            f"║   {text}{' ' * (content_width - len(text.plain))}   ║",
            style=f"bold {style}",
        )

    console.print(f"║{' ' * (box_width - 2)}║", style=f"bold {style}")

    tagline_pad = (content_width - len(TAGLINE)) // 2
    console.print(
        f"║   {' ' * tagline_pad}{TAGLINE}{' ' * (content_width - len(TAGLINE) - tagline_pad)}   ║",
        style=f"bold {style}",
    )

    console.print(f"║{' ' * (box_width - 2)}║", style=f"bold {style}")
    console.print(border(False), style=f"bold {style}")

    console.print()
    console.print("GroqCLI Chatbot initialized", style="bold green")
    console.print("Type /help for available commands", style="dim")


def show_startup_tip():
    console.print(random.choice(STARTUP_TIPS), style="yellow")


# =============================================================================
# ALIAS FOR COMPATIBILITY
# =============================================================================

def show_animated_banner():
    """Alias for show_banner() - for compatibility with main.py"""
    show_banner(style="cyan")


def show_gradient_banner():
    """Gradient style banner"""
    show_banner(style="magenta")


def show_minimal_banner():
    """Minimal style banner"""
    show_banner(style="white")


def show_simple_banner():
    """Simple style banner"""
    show_banner(style="cyan")


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    show_banner()
    show_startup_tip()
