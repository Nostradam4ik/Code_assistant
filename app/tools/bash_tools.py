"""Tool definitions for bash operations."""

from app.tools.registry import Tool, ToolSchema
from app.tools.bash import run_bash


RUN_BASH_TOOL = Tool(
    name="run_bash",
    description="Execute a bash/shell command and get the output. Useful for running tests, installations, git commands, and system operations. Commands are sandboxed with a 10-second timeout.",
    schema=ToolSchema(
        properties={
            "command": {
                "type": "string",
                "description": "The bash/shell command to execute (e.g., 'python -m pytest' or 'git status')"
            }
        },
        required=["command"]
    ),
    func=run_bash,
)

# Export all bash tools
BASH_TOOLS = [RUN_BASH_TOOL]
