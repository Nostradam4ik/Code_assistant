"""Tools module with structured tool definitions and registry."""

from typing import Any

from app.tools.base import ToolError
from app.tools.registry import (
    Tool,
    ToolSchema,
    ToolRegistry,
    get_registry,
    register_tool,
    execute_tool,
)
from app.tools.file_tools import FILE_TOOLS
from app.tools.bash_tools import BASH_TOOLS
from app.tools.search_tools import SEARCH_TOOLS
from app.tools.memory_tools import MEMORY_TOOLS

# Register all tools in the global registry
_registry = get_registry()
for tool in FILE_TOOLS + BASH_TOOLS + SEARCH_TOOLS + MEMORY_TOOLS:
    _registry.register(tool)

# Export for convenience
TOOLS = _registry.get_all_schemas()  # For Groq API


def call_tool(name: str, **kwargs: Any) -> str:
    """
    Call a tool by name with given arguments.
    
    Args:
        name: Tool name
        **kwargs: Tool arguments
        
    Returns:
        Tool result
        
    Raises:
        ToolError: If tool fails
    """
    return execute_tool(name, **kwargs)


__all__ = [
    "ToolError",
    "Tool",
    "ToolSchema",
    "ToolRegistry",
    "get_registry",
    "register_tool",
    "execute_tool",
    "call_tool",
    "TOOLS",
    "FILE_TOOLS",
    "BASH_TOOLS",
    "SEARCH_TOOLS",
    "MEMORY_TOOLS",
]
