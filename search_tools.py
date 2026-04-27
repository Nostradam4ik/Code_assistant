"""Definition for search tools."""

from app.tools.registry import Tool, ToolSchema
from app.tools.search import search_files

SEARCH_TOOL = Tool(
    name="search_in_files",
    description="Search for a regex pattern across all files in a directory.",
    schema=ToolSchema(
        properties={
            "pattern": {
                "type": "string",
                "description": "Regex pattern to search for"
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in (default: current)"
            }
        },
        required=["pattern"]
    ),
    func=search_files
)

SEARCH_TOOLS = [SEARCH_TOOL]