"""Execution logic for memory operations."""

from datetime import datetime
from pathlib import Path
from app.config import MEMORY_FILE
from app.tools.base import ToolError

def save_memory(content: str) -> str:
    """
    Append important information to the MEMORY.md file for long-term persistence.
    """
    try:
        path = Path(MEMORY_FILE)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n### {timestamp} - PERSISTENT CONTEXT\n{content}\n"
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
        return "Information successfully saved to persistent memory."
    except Exception as e:
        raise ToolError(f"Failed to save to memory: {str(e)}")