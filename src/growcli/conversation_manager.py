"""
Conversation Manager - Handle saving, loading, and exporting conversations.

Features:
- Save conversations in multiple formats (JSON, Markdown, Text)
- Load previous conversations
- Auto-save on exit
- Export with metadata
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@dataclass
class ConversationMessage:
    """Single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    tokens: int = 0
    latency: float = 0.0


@dataclass
class ConversationMetadata:
    """Metadata for a conversation."""
    session_id: str
    model: str
    temperature: float
    start_time: str
    end_time: Optional[str] = None
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0


class ConversationManager:
    """
    Manages conversation persistence and export.
    
    Features:
    - Save/load conversations
    - Multiple export formats
    - Auto-save functionality
    - Search conversations
    """
    
    def __init__(self, save_dir: str = "conversations"):
        """
        Initialize conversation manager.
        
        Args:
            save_dir: Directory to save conversations
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        self.current_conversation: List[ConversationMessage] = []
        self.metadata: Optional[ConversationMetadata] = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def start_session(self, model: str, temperature: float):
        """Start a new conversation session."""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metadata = ConversationMetadata(
            session_id=self.session_id,
            model=model,
            temperature=temperature,
            start_time=datetime.now().isoformat(),
        )
        self.current_conversation = []
    
    def add_message(
        self,
        role: str,
        content: str,
        tokens: int = 0,
        latency: float = 0.0
    ):
        """Add a message to current conversation."""
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            tokens=tokens,
            latency=latency,
        )
        self.current_conversation.append(message)
        
        if self.metadata:
            self.metadata.total_messages += 1
            self.metadata.total_tokens += tokens
    
    def save_json(self, filename: Optional[str] = None) -> str:
        """
        Save conversation as JSON.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            filename = f"conversation_{self.session_id}.json"
        
        filepath = self.save_dir / filename
        
        data = {
            "metadata": asdict(self.metadata) if self.metadata else {},
            "messages": [asdict(msg) for msg in self.current_conversation]
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Saving conversation..."),
            transient=True,
        ) as progress:
            progress.add_task("Saving", total=None)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_markdown(self, filename: Optional[str] = None) -> str:
        """
        Save conversation as Markdown.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            filename = f"conversation_{self.session_id}.md"
        
        filepath = self.save_dir / filename
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Exporting to Markdown..."),
            transient=True,
        ) as progress:
            progress.add_task("Exporting", total=None)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# Conversation - {self.session_id}\n\n")
                
                if self.metadata:
                    f.write("## Metadata\n\n")
                    f.write(f"- **Model**: {self.metadata.model}\n")
                    f.write(f"- **Temperature**: {self.metadata.temperature}\n")
                    f.write(f"- **Start Time**: {self.metadata.start_time}\n")
                    f.write(f"- **Total Messages**: {self.metadata.total_messages}\n")
                    f.write(f"- **Total Tokens**: {self.metadata.total_tokens}\n\n")
                
                f.write("---\n\n")
                f.write("## Conversation\n\n")
                
                # Write messages
                for msg in self.current_conversation:
                    role_emoji = "👤" if msg.role == "user" else "🤖"
                    role_name = "You" if msg.role == "user" else "Assistant"
                    
                    f.write(f"### {role_emoji} {role_name}\n\n")
                    f.write(f"{msg.content}\n\n")
                    
                    if msg.tokens > 0:
                        f.write(f"*Tokens: {msg.tokens} | Latency: {msg.latency:.2f}s*\n\n")
                    
                    f.write("---\n\n")
        
        return str(filepath)
    
    def save_text(self, filename: Optional[str] = None) -> str:
        """
        Save conversation as plain text.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            filename = f"conversation_{self.session_id}.txt"
        
        filepath = self.save_dir / filename
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Exporting to text..."),
            transient=True,
        ) as progress:
            progress.add_task("Exporting", total=None)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"Conversation - {self.session_id}\n")
                f.write("=" * 60 + "\n\n")
                
                if self.metadata:
                    f.write("Metadata:\n")
                    f.write(f"  Model: {self.metadata.model}\n")
                    f.write(f"  Temperature: {self.metadata.temperature}\n")
                    f.write(f"  Start Time: {self.metadata.start_time}\n")
                    f.write(f"  Total Messages: {self.metadata.total_messages}\n")
                    f.write(f"  Total Tokens: {self.metadata.total_tokens}\n\n")
                
                f.write("-" * 60 + "\n\n")
                
                # Write messages
                for msg in self.current_conversation:
                    role_name = "You" if msg.role == "user" else "Assistant"
                    
                    f.write(f"{role_name}:\n")
                    f.write(f"{msg.content}\n")
                    
                    if msg.tokens > 0:
                        f.write(f"(Tokens: {msg.tokens} | Latency: {msg.latency:.2f}s)\n")
                    
                    f.write("\n" + "-" * 60 + "\n\n")
        
        return str(filepath)
    
    def load_conversation(self, filepath: str) -> bool:
        """
        Load a conversation from JSON file.
        
        Args:
            filepath: Path to conversation file
            
        Returns:
            True if loaded successfully
        """
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Loading conversation..."),
                transient=True,
            ) as progress:
                progress.add_task("Loading", total=None)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load metadata
                if 'metadata' in data:
                    self.metadata = ConversationMetadata(**data['metadata'])
                
                # Load messages
                self.current_conversation = [
                    ConversationMessage(**msg) for msg in data['messages']
                ]
            
            console.print(f"[green]✓[/green] Loaded {len(self.current_conversation)} messages")
            return True
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error loading conversation: {e}")
            return False
    
    def list_conversations(self) -> List[str]:
        """List all saved conversations."""
        conversations = []
        for file in self.save_dir.glob("conversation_*.json"):
            conversations.append(str(file))
        return sorted(conversations, reverse=True)
    
    def auto_save(self):
        """Auto-save current conversation."""
        if len(self.current_conversation) > 0:
            filepath = self.save_json()
            console.print(f"[dim]Auto-saved to: {filepath}[/dim]")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of current conversation."""
        if not self.current_conversation:
            return "No messages in current conversation"
        
        user_msgs = sum(1 for msg in self.current_conversation if msg.role == "user")
        assistant_msgs = sum(1 for msg in self.current_conversation if msg.role == "assistant")
        total_tokens = sum(msg.tokens for msg in self.current_conversation)
        
        return (
            f"Messages: {len(self.current_conversation)} "
            f"(You: {user_msgs}, Assistant: {assistant_msgs}) | "
            f"Tokens: {total_tokens}"
        )
