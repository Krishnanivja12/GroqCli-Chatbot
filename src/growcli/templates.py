"""
Template system for GroqCLI-Chatbot.

Provides pre-built conversation templates for common tasks.
Optimized with only essential templates.
"""

from dataclasses import dataclass
from typing import Dict
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class Template:
    """A conversation template with name, description, and prompt."""
    name: str
    category: str
    description: str
    prompt: str


class TemplateManager:
    """
    Manages conversation templates.
    Optimized with only 5 essential templates.
    """
    
    def __init__(self):
        """Initialize with essential templates only."""
        self.templates: Dict[str, Template] = {
            # Coding Templates (3)
            "code": Template(
                name="code",
                category="Coding",
                description="Get help writing code",
                prompt="You are an expert programmer. Provide clean, working code with clear structure:\n"
                       "1. Brief explanation first\n"
                       "2. Code in proper ```language blocks\n"
                       "3. Comments in code\n"
                       "4. Usage example if needed\n"
                       "Keep formatting clean and structured."
            ),
            "debug": Template(
                name="debug",
                category="Coding",
                description="Debug code and fix errors",
                prompt="You are a debugging expert. Structure your response:\n"
                       "1. Identify the issue\n"
                       "2. Explain why it happens\n"
                       "3. Provide fixed code in ```language blocks\n"
                       "4. Explain the fix\n"
                       "Keep formatting clean and easy to copy."
            ),
            "review": Template(
                name="review",
                category="Coding",
                description="Review code quality",
                prompt="You are a code reviewer. Structure your review:\n"
                       "1. Overall assessment\n"
                       "2. Issues found (list format)\n"
                       "3. Improved code in ```language blocks\n"
                       "4. Explanation of improvements\n"
                       "Keep formatting clean and structured."
            ),
            
            # Learning Template (1)
            "explain": Template(
                name="explain",
                category="Learning",
                description="Explain concepts clearly",
                prompt="You are a patient teacher. Structure your explanation:\n"
                       "1. Simple definition\n"
                       "2. Key points (bullet list)\n"
                       "3. Example with code in ```language blocks if applicable\n"
                       "4. Summary\n"
                       "Keep formatting clean and easy to read."
            ),
            
            # Productivity Template (1)
            "summarize": Template(
                name="summarize",
                category="Productivity",
                description="Summarize text or content",
                prompt="You are a summarization expert. Structure your summary:\n"
                       "1. Main topic\n"
                       "2. Key points (bullet list)\n"
                       "3. Conclusion\n"
                       "Keep formatting clean and concise."
            ),
        }
    
    def get_template(self, name: str) -> Template | None:
        """Get a template by name."""
        return self.templates.get(name.lower())
    
    def list_templates(self) -> list[Template]:
        """Get all templates."""
        return list(self.templates.values())
    
    def format_template_list(self) -> str:
        """Format templates as clean text list."""
        output = "\n[bold cyan]📋 Available Templates (5 Essential)[/bold cyan]\n\n"
        
        # Group by category
        categories = {
            "Coding": [],
            "Learning": [],
            "Productivity": []
        }
        
        for template in self.templates.values():
            categories[template.category].append(template)
        
        # Format each category
        for category, templates in categories.items():
            if templates:
                output += f"[bold yellow]{category}:[/bold yellow]\n"
                for t in templates:
                    output += f"  [cyan]/{t.name:<12}[/cyan] {t.description}\n"
                output += "\n"
        
        output += "[dim]Usage: /template <name> or /t <name>[/dim]\n"
        output += "[dim]Example: /template code[/dim]\n"
        
        return output
