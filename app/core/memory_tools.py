"""Tool definitions for memory operations."""

from app.tools.registry import Tool, ToolSchema
from app.tools.memory import save_memory

SAVE_MEMORY_TOOL = Tool(
    name="save_memory",
    description="Save important project details, architectural decisions, or key facts to remember across future sessions in MEMORY.md.",
    schema=ToolSchema(
        properties={
            "content": {
                "type": "string",
                "description": "The specific information or context to remember."
            }
        },
        required=["content"]
    ),
    func=save_memory,
)

# Export memory tools
MEMORY_TOOLS = [SAVE_MEMORY_TOOL]