"""Tool definitions for search operations."""

from app.tools.registry import Tool, ToolSchema
from app.tools.search import search_files


SEARCH_FILES_TOOL = Tool(
    name="search_files",
    description="Search for a regex pattern across files in a directory. Useful for finding code patterns, functions, or configuration values.",
    schema=ToolSchema(
        properties={
            "pattern": {
                "type": "string",
                "description": "Regex pattern to search for (e.g., 'def get_user' or 'import.*os')"
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in (defaults to current directory)"
            }
        },
        required=["pattern"]
    ),
    func=search_files,
)

# Export all search tools
SEARCH_TOOLS = [SEARCH_FILES_TOOL]
