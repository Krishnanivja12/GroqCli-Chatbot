"""
Model selection interface for GroqCLI-Chatbot.

Allows users to choose AI model at startup.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class ModelSelector:
    """
    Interactive model selection interface.
    """
    
    def __init__(self):
        """Initialize with available models."""
        self.models = [
            {
                "id": "llama-3.3-70b-versatile",
                "name": "Llama 3.3 70B",
                "description": "Best quality, most capable",
                "speed": "Medium",
                "context": "8K tokens"
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B",
                "description": "Fast responses, good quality",
                "speed": "Very Fast",
                "context": "8K tokens"
            },
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral 8x7B",
                "description": "Large context window",
                "speed": "Fast",
                "context": "32K tokens"
            },
            {
                "id": "gemma2-9b-it",
                "name": "Gemma 2 9B",
                "description": "Efficient, instruction-tuned",
                "speed": "Fast",
                "context": "8K tokens"
            },
        ]
    
    def show_models(self) -> None:
        """Display available models in a table."""
        table = Table(
            title="🤖 Available AI Models",
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("#", style="cyan", width=3)
        table.add_column("Model", style="green", width=20)
        table.add_column("Description", style="white", width=30)
        table.add_column("Speed", style="yellow", width=12)
        table.add_column("Context", style="magenta", width=10)
        
        for i, model in enumerate(self.models, 1):
            table.add_row(
                str(i),
                model["name"],
                model["description"],
                model["speed"],
                model["context"]
            )
        
        console.print()
        console.print(table)
        console.print()
    
    def select_model(self, default: str = None) -> str:
        """
        Interactive model selection.
        
        Args:
            default: Default model ID
            
        Returns:
            str: Selected model ID
        """
        # Find default index
        default_idx = 1
        if default:
            for i, model in enumerate(self.models, 1):
                if model["id"] == default:
                    default_idx = i
                    break
        
        self.show_models()
        
        console.print(f"[bold cyan]Select model [1-{len(self.models)}] (default: {default_idx}):[/bold cyan] ", end="")
        
        try:
            choice = input().strip()
            
            if not choice:
                choice = str(default_idx)
            
            idx = int(choice) - 1
            
            if 0 <= idx < len(self.models):
                selected = self.models[idx]
                console.print(f"\n[bold green]✓ Selected: {selected['name']}[/bold green]\n")
                return selected["id"]
            else:
                console.print(f"\n[yellow]Invalid choice. Using default: {self.models[default_idx-1]['name']}[/yellow]\n")
                return self.models[default_idx-1]["id"]
                
        except (ValueError, KeyboardInterrupt):
            console.print(f"\n[yellow]Using default: {self.models[default_idx-1]['name']}[/yellow]\n")
            return self.models[default_idx-1]["id"]
    
    def get_model_info(self, model_id: str) -> dict:
        """Get information about a model."""
        for model in self.models:
            if model["id"] == model_id:
                return model
        return self.models[0]  # Default
