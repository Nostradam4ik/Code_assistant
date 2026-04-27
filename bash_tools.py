"""Definition for bash tools."""

from app.tools.registry import Tool, ToolSchema
from app.tools.bash import run_bash

BASH_TOOL = Tool(
    name="bash",
    description="Execute a bash command in the local environment. Use for running tests, installing dependencies, or git operations.",
    schema=ToolSchema(
        properties={
            "command": {
                "type": "string",
                "description": "The full bash command to execute"
            }
        },
        required=["command"]
    ),
    func=run_bash
)

BASH_TOOLS = [BASH_TOOL]