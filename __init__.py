"""Central entry point for tools."""

from .registry import get_registry, ToolError
from .file_tools import FILE_TOOLS
from .bash_tools import BASH_TOOLS
from .search_tools import SEARCH_TOOLS

# Initialize global registry
registry = get_registry()

# Register all tools
for tool in FILE_TOOLS + BASH_TOOLS + SEARCH_TOOLS:
    registry.register(tool)

# Export main interface
def call_tool(name: str, **kwargs) -> str:
    return registry.execute(name, **kwargs)

TOOLS = registry.get_all_schemas()