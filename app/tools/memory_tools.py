"""Tool definitions and execution logic for persistent memory operations."""

from datetime import datetime
from pathlib import Path

from app.config import MEMORY_FILE
from app.tools.base import ToolError
from app.tools.registry import Tool, ToolSchema


def read_memory() -> str:
    """
    Read the full content of the MEMORY.md file.
    
    Returns:
        The content of the memory file.
    """
    try:
        path = Path(MEMORY_FILE)
        if not path.exists():
            # Gracefully handle missing file by creating it with a header
            path.write_text("# Conversation Memory\n\n", encoding="utf-8")
            return "Memory is currently empty."
        
        content = path.read_text(encoding="utf-8")
        return content if content.strip() else "Memory is currently empty."
    except Exception as e:
        raise ToolError(f"Failed to read memory: {str(e)}")


def write_memory(content: str) -> str:
    """
    Append content to the MEMORY.md file with a timestamp.
    
    Args:
        content: The information to save.
        
    Returns:
        Success message.
    """
    try:
        path = Path(MEMORY_FILE)
        if not path.exists():
            path.write_text("# Conversation Memory\n\n", encoding="utf-8")
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n### {timestamp} - PERSISTENT CONTEXT\n{content}\n"
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
        return "Information successfully saved to persistent memory."
    except Exception as e:
        raise ToolError(f"Failed to save to memory: {str(e)}")


def clear_memory() -> str:
    """
    Clear the content of the memory file.
    
    Returns:
        Success message.
    """
    try:
        path = Path(MEMORY_FILE)
        path.write_text("# Conversation Memory\n\n", encoding="utf-8")
        return "Persistent memory cleared."
    except Exception as e:
        raise ToolError(f"Failed to clear memory: {str(e)}")


# Tool definitions for registration in ToolRegistry
READ_MEMORY_TOOL = Tool(
    name="read_memory",
    description="Read the entire contents of the persistent memory file (MEMORY.md). Use this to recall long-term context, project rules, or architectural decisions saved in previous sessions.",
    schema=ToolSchema(
        properties={},
        required=[]
    ),
    func=read_memory,
)

WRITE_MEMORY_TOOL = Tool(
    name="write_memory",
    description="Append important project details, architectural decisions, or key facts to remember across future sessions in MEMORY.md.",
    schema=ToolSchema(
        properties={
            "content": {
                "type": "string",
                "description": "The specific information or context to remember."
            }
        },
        required=["content"]
    ),
    func=write_memory,
)

CLEAR_MEMORY_TOOL = Tool(
    name="clear_memory",
    description="Wipe all entries from the persistent memory file (MEMORY.md). Use this only when starting a completely fresh project context.",
    schema=ToolSchema(
        properties={},
        required=[]
    ),
    func=clear_memory,
)

# Export memory tools list as expected by app/tools/__init__.py
MEMORY_TOOLS = [READ_MEMORY_TOOL, WRITE_MEMORY_TOOL, CLEAR_MEMORY_TOOL]