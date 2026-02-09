"""
Cost tracking for GroqCLI-Chatbot.

Monitors token usage and calculates costs.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class CostData:
    """Cost data for a session."""
    date: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float


class CostTracker:
    """
    Track and calculate costs for API usage.
    
    Groq pricing (approximate):
    - Prompt tokens: $0.0001 per 1K tokens
    - Completion tokens: $0.0002 per 1K tokens
    """
    
    def __init__(self):
        """Initialize cost tracker."""
        self.cost_file = Path("conversations/.cost_history.json")
        self.cost_file.parent.mkdir(exist_ok=True)
        
        # Pricing (per 1K tokens)
        self.prompt_price = 0.0001
        self.completion_price = 0.0002
        
        # Session tracking
        self.session_prompt_tokens = 0
        self.session_completion_tokens = 0
        self.session_cost = 0.0
        
        # Load history
        self.history = self._load_history()
    
    def _load_history(self) -> list[CostData]:
        """Load cost history from file."""
        if self.cost_file.exists():
            try:
                with open(self.cost_file, 'r') as f:
                    data = json.load(f)
                    return [CostData(**item) for item in data]
            except Exception:
                return []
        return []
    
    def _save_history(self):
        """Save cost history to file."""
        try:
            data = [
                {
                    "date": item.date,
                    "prompt_tokens": item.prompt_tokens,
                    "completion_tokens": item.completion_tokens,
                    "total_tokens": item.total_tokens,
                    "estimated_cost": item.estimated_cost
                }
                for item in self.history
            ]
            with open(self.cost_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def add_usage(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Add token usage and calculate cost.
        
        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            
        Returns:
            float: Cost for this interaction
        """
        # Calculate cost
        cost = (
            (prompt_tokens / 1000 * self.prompt_price) +
            (completion_tokens / 1000 * self.completion_price)
        )
        
        # Update session
        self.session_prompt_tokens += prompt_tokens
        self.session_completion_tokens += completion_tokens
        self.session_cost += cost
        
        return cost
    
    def get_session_cost(self) -> dict:
        """Get current session cost data."""
        return {
            "prompt_tokens": self.session_prompt_tokens,
            "completion_tokens": self.session_completion_tokens,
            "total_tokens": self.session_prompt_tokens + self.session_completion_tokens,
            "estimated_cost": self.session_cost
        }
    
    def get_total_cost(self) -> float:
        """Get total cost from history."""
        return sum(item.estimated_cost for item in self.history)
    
    def save_session(self):
        """Save current session to history."""
        if self.session_prompt_tokens > 0:
            cost_data = CostData(
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                prompt_tokens=self.session_prompt_tokens,
                completion_tokens=self.session_completion_tokens,
                total_tokens=self.session_prompt_tokens + self.session_completion_tokens,
                estimated_cost=self.session_cost
            )
            self.history.append(cost_data)
            self._save_history()
    
    def format_cost_display(self) -> str:
        """Format cost information for display."""
        session = self.get_session_cost()
        total = self.get_total_cost()
        
        return f"""
💰 Cost Tracking:
   Session Cost       : ${session['estimated_cost']:.4f}
   Session Tokens     : {session['total_tokens']:,}
   Total Cost (All)   : ${total:.4f}
   
   [dim]Note: Costs are estimates based on typical pricing[/dim]
"""
