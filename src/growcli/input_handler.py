"""
Enhanced Input Handler - Better input with multi-line support and shortcuts.

Features:
- Multi-line input (Enter twice to send)
- Keyboard shortcuts
- Input history navigation
- Auto-completion
"""

from typing import List, Optional, Callable
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console

console = Console()


class EnhancedInputHandler:
    """
    Enhanced input handler with advanced features.
    
    Features:
    - Multi-line input support
    - Command history
    - Auto-completion
    - Keyboard shortcuts
    """
    
    def __init__(self, commands: List[str] = None):
        """
        Initialize input handler.
        
        Args:
            commands: List of commands for auto-completion
        """
        self.history = InMemoryHistory()
        self.commands = commands or []
        
        # Create completer
        self.completer = WordCompleter(
            self.commands,
            ignore_case=True,
            sentence=True,
        )
        
        # Create key bindings
        self.bindings = self._create_key_bindings()
        
        # Create session
        self.session = PromptSession(
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.completer,
            key_bindings=self.bindings,
            multiline=False,  # We'll handle multi-line manually
            enable_history_search=True,
        )
        
        self.multiline_buffer: List[str] = []
        self.multiline_mode = False
    
    def _create_key_bindings(self) -> KeyBindings:
        """Create custom key bindings."""
        kb = KeyBindings()
        
        # Ctrl+L to clear screen
        @kb.add('c-l')
        def _(event):
            """Clear screen."""
            console.clear()
        
        # Ctrl+D to exit
        @kb.add('c-d')
        def _(event):
            """Exit application."""
            event.app.exit(result='/quit')
        
        return kb
    
    def get_input(self, prompt: str = "👤 You: ") -> str:
        """
        Get user input with enhanced features.
        
        Args:
            prompt: Prompt to display
            
        Returns:
            User input string
        """
        try:
            # Get input
            user_input = self.session.prompt(prompt)
            
            # Check for multi-line mode
            if user_input.endswith('\\'):
                # Start multi-line mode
                self.multiline_mode = True
                self.multiline_buffer = [user_input[:-1]]  # Remove backslash
                
                while self.multiline_mode:
                    line = self.session.prompt("   ... ")
                    
                    if line.endswith('\\'):
                        self.multiline_buffer.append(line[:-1])
                    else:
                        self.multiline_buffer.append(line)
                        self.multiline_mode = False
                
                # Join all lines
                result = '\n'.join(self.multiline_buffer)
                self.multiline_buffer = []
                return result
            
            return user_input
            
        except KeyboardInterrupt:
            return '/quit'
        except EOFError:
            return '/quit'
    
    def get_multiline_input(self, prompt: str = "👤 You: ") -> str:
        """
        Get multi-line input (press Enter twice to send).
        
        Args:
            prompt: Prompt to display
            
        Returns:
            Multi-line user input
        """
        console.print(f"{prompt}[dim](Press Enter twice to send)[/dim]")
        lines = []
        empty_count = 0
        
        try:
            while True:
                line = self.session.prompt("   ")
                
                if line.strip() == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            
            return '\n'.join(lines)
            
        except (KeyboardInterrupt, EOFError):
            return '/quit'
    
    def add_command(self, command: str):
        """Add a command to auto-completion."""
        if command not in self.commands:
            self.commands.append(command)
            self.completer = WordCompleter(
                self.commands,
                ignore_case=True,
                sentence=True,
            )
    
    def clear_history(self):
        """Clear input history."""
        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.completer,
            key_bindings=self.bindings,
        )


# Simple fallback for systems without prompt_toolkit
class SimpleInputHandler:
    """Simple input handler fallback."""
    
    def __init__(self, commands: List[str] = None):
        """Initialize simple handler."""
        self.commands = commands or []
    
    def get_input(self, prompt: str = "👤 You: ") -> str:
        """Get simple input."""
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            return '/quit'
    
    def get_multiline_input(self, prompt: str = "👤 You: ") -> str:
        """Get multi-line input."""
        console.print(f"{prompt}[dim](Enter empty line twice to send)[/dim]")
        lines = []
        empty_count = 0
        
        try:
            while True:
                line = input("   ")
                if line.strip() == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            
            return '\n'.join(lines)
        except (KeyboardInterrupt, EOFError):
            return '/quit'
    
    def add_command(self, command: str):
        """Add command (no-op for simple handler)."""
        pass
    
    def clear_history(self):
        """Clear history (no-op for simple handler)."""
        pass


# Factory function
def create_input_handler(commands: List[str] = None):
    """
    Create appropriate input handler.
    
    Args:
        commands: List of commands for auto-completion
        
    Returns:
        Input handler instance
    """
    # Always use simple handler for better compatibility
    return SimpleInputHandler(commands)
