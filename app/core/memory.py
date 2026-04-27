"""Memory management for conversation persistence."""

from datetime import datetime
from pathlib import Path

from app.config import MEMORY_FILE
from app.tools.base import ToolError


class MemoryManager:
    """Manages reading and writing conversation history to a markdown file."""

    def __init__(self, memory_file: str = "MEMORY.md") -> None:
        """Initialize with memory file path."""
        self.memory_file = Path(memory_file)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Create the memory file if it doesn't exist."""
        if not self.memory_file.exists():
            self.memory_file.write_text("# Conversation Memory\n\n", encoding="utf-8")

    def add_entry(self, role: str, content: str) -> None:
        """Appends a timestamped entry to the memory file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"### {timestamp} - {role.upper()}\n{content}\n\n"
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def read_memory(self) -> str:
        """Reads and returns the full memory file content."""
        if not self.memory_file.exists():
            return ""
        return self.memory_file.read_text(encoding="utf-8")

    def clear(self) -> None:
        """Clears the memory file content."""
        self.memory_file.write_text("# Conversation Memory\n\n", encoding="utf-8")


def save_memory(content: str) -> str:
    """
    Append important information to the MEMORY.md file for long-term persistence.
    """
    try:
        path = Path("MEMORY.md")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n### {timestamp} - PERSISTENT CONTEXT\n{content}\n"
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
        return "Information successfully saved to persistent memory."
    except Exception as e:
        raise ToolError(f"Failed to save to memory: {str(e)}")