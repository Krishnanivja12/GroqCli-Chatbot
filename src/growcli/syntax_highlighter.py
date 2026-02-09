"""
Syntax highlighting for code blocks in GroqCLI-Chatbot responses.

Provides beautiful, structured code formatting with clear separation.
"""

import re
from typing import Optional
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


class SyntaxHighlighter:
    """
    Handles syntax highlighting for code in bot responses.
    Optimized for clean, structured output that's easy to copy.
    """
    
    def __init__(self):
        """Initialize the syntax highlighter."""
        self.supported_languages = {
            'python', 'javascript', 'java', 'c', 'cpp', 'csharp',
            'go', 'rust', 'ruby', 'php', 'swift', 'kotlin',
            'typescript', 'html', 'css', 'sql', 'bash', 'shell',
            'json', 'yaml', 'xml', 'markdown'
        }
    
    def format_response(self, text: str) -> None:
        """
        Format response with proper structure and syntax highlighting.
        
        Args:
            text: The response text with potential code blocks
        """
        # Split by code blocks (```language ... ```)
        parts = re.split(r'```(\w+)?\n(.*?)```', text, flags=re.DOTALL)
        
        for i, part in enumerate(parts):
            if i % 3 == 0:
                # Regular text (not code)
                if part.strip():
                    # Use Markdown for better formatting
                    md = Markdown(part.strip())
                    console.print(md)
                    console.print()  # Add spacing
            elif i % 3 == 1:
                # Language identifier
                language = part.lower() if part else 'text'
            elif i % 3 == 2:
                # Code block
                self._print_code_block(part, language)
    
    def _print_code_block(self, code: str, language: str) -> None:
        """
        Print a code block with syntax highlighting and clear structure.
        
        Args:
            code: The code to highlight
            language: Programming language
        """
        # Clean the code
        code = code.strip()
        
        if not code:
            return
        
        # Validate language
        if language not in self.supported_languages:
            language = 'text'
        
        # Create syntax-highlighted code
        syntax = Syntax(
            code,
            language,
            theme="monokai",
            line_numbers=True,
            word_wrap=False,
            background_color="default"
        )
        
        # Print in a panel for clear separation
        panel = Panel(
            syntax,
            title=f"[bold cyan]📝 {language.upper()} Code[/bold cyan]",
            subtitle="[dim]Select and copy with mouse[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
        
        console.print(panel)
        console.print()  # Add spacing after code block
    
    def format_simple(self, text: str) -> None:
        """
        Simple formatting without code highlighting.
        For when highlighting is disabled.
        
        Args:
            text: The response text
        """
        # Split by code blocks
        parts = re.split(r'```(\w+)?\n(.*?)```', text, flags=re.DOTALL)
        
        for i, part in enumerate(parts):
            if i % 3 == 0:
                # Regular text
                if part.strip():
                    console.print(part.strip())
                    console.print()
            elif i % 3 == 2:
                # Code block (no highlighting)
                code = part.strip()
                if code:
                    # Print with clear separation
                    console.print("\n" + "─" * 60)
                    console.print(f"[bold cyan]CODE:[/bold cyan]")
                    console.print("─" * 60)
                    
                    # Print code with line numbers
                    for line_num, line in enumerate(code.split('\n'), 1):
                        console.print(f"{line_num:3d} | {line}")
                    
                    console.print("─" * 60)
                    console.print("[dim]Select and copy with mouse[/dim]")
                    console.print("─" * 60 + "\n")


def detect_language(code: str) -> str:
    """
    Auto-detect programming language from code.
    
    Args:
        code: Code snippet
        
    Returns:
        str: Detected language or 'text'
    """
    # Simple heuristics
    if 'def ' in code or 'import ' in code or 'print(' in code:
        return 'python'
    elif 'function ' in code or 'const ' in code or 'let ' in code:
        return 'javascript'
    elif 'public class' in code or 'public static void' in code:
        return 'java'
    elif '#include' in code:
        return 'cpp'
    elif 'SELECT ' in code.upper() or 'FROM ' in code.upper():
        return 'sql'
    else:
        return 'text'
