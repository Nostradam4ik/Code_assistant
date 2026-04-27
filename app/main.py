#!/usr/bin/env python3
"""Main entry point for the AI coding assistant."""

import sys

from rich.console import Console

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.llm import GroqClient
from app.core import MemoryManager
from app.core.agent import Agent


def main() -> None:
    """Entry point for the application."""
    try:
        # Validate API key
        if not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY environment variable not set. "
                "Please set it before running the assistant."
            )
        
        # Initialize components
        client = GroqClient(api_key=GROQ_API_KEY, model=GROQ_MODEL)
        memory = MemoryManager()
        agent = Agent(client=client, memory=memory)
        
        # Run the agent
        agent.run()
    
    except RuntimeError as e:
        console = Console()
        console.print(f"[red]Error: {str(e)}[/red]", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        console = Console()
        console.print(f"[red]Fatal error: {str(e)}[/red]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
