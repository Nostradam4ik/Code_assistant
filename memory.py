"""Memory management for conversation persistence."""

from pathlib import Path
from datetime import datetime
from typing import Optional
from config import MEMORY_FILE, MAX_MEMORY_ENTRIES


class MemoryManager:
    """Manages conversation memory in MEMORY.md file."""
    
    def __init__(self, memory_file: str = MEMORY_FILE):
        self.memory_file = Path(memory_file)
        self.ensure_memory_file()
    
    def ensure_memory_file(self):
        """Create memory file if it doesn't exist."""
        if not self.memory_file.exists():
            self.memory_file.write_text(
                "# Conversation Memory\n\n"
                "This file stores conversation context for the AI assistant.\n\n"
            )
    
    def read_memory(self) -> str:
        """Read the current memory content."""
        if not self.memory_file.exists():
            return ""
        
        content = self.memory_file.read_text()
        # Skip the header
        lines = content.split('\n')[3:]
        return '\n'.join(lines).strip()
    
    def add_entry(self, role: str, content: str, tools_used: Optional[list] = None):
        """
        Add an entry to memory.
        
        Args:
            role: "user" or "assistant"
            content: The message content
            tools_used: List of tools called (optional)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Read current content
        current = self.memory_file.read_text()
        
        # Build new entry
        entry = f"\n### {timestamp} - {role.upper()}\n{content[:500]}..."  # Truncate long entries
        
        if tools_used:
            entry += f"\nTools used: {', '.join(tools_used)}"
        
        # Append entry
        self.memory_file.write_text(current + entry + "\n")
        
        # Trim if too many entries
        self.trim_memory()
    
    def trim_memory(self):
        """Keep memory file under MAX_MEMORY_ENTRIES entries."""
        content = self.memory_file.read_text()
        lines = content.split('\n')
        
        # Count entries (lines starting with ###)
        entries = [i for i, line in enumerate(lines) if line.startswith('###')]
        
        if len(entries) > MAX_MEMORY_ENTRIES:
            # Keep header and last N entries
            keep_from = entries[len(entries) - MAX_MEMORY_ENTRIES]
            new_content = '\n'.join(lines[:3] + lines[keep_from:])
            self.memory_file.write_text(new_content)
    
    def clear(self):
        """Clear all memory entries."""
        self.memory_file.write_text(
            "# Conversation Memory\n\n"
            "This file stores conversation context for the AI assistant.\n\n"
        )
