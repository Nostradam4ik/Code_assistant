"""File search tool."""

import re
from pathlib import Path
from typing import Any

from app.tools.base import ToolError, is_safe_path, get_tool_schema


def search_files(pattern: str, directory: str = ".") -> str:
    """
    Search for a regex pattern in files.
    
    Args:
        pattern: Regex pattern to search for
        directory: Directory to search in (defaults to current)
        
    Returns:
        Search results with file paths and line numbers
        
    Raises:
        ToolError: If search fails
    """
    try:
        path = Path(directory).resolve()
        
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {directory} is outside workspace")
        
        if not path.exists():
            raise ToolError(f"Directory not found: {directory}")
        
        # Compile regex
        try:
            regex = re.compile(pattern, re.MULTILINE)
        except re.error as e:
            raise ToolError(f"Invalid regex pattern: {str(e)}")
        
        results = []
        
        # Search through Python files
        for file_path in path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            rel_path = file_path.relative_to(path)
                            results.append(f"  {rel_path}:{line_num}: {line.rstrip()}")
            except Exception:
                continue
        
        if not results:
            return f"No matches found for pattern: {pattern}"
        
        return f"Search results for '{pattern}':\n" + "\n".join(results[:50])
    
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error searching files: {str(e)}")


# Tool schema for Groq API
SEARCH_FILES_SCHEMA = get_tool_schema(
    "search_files",
    "Search for a regex pattern in files",
    {
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Regex pattern to search for"
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in (defaults to current)"
            }
        },
        "required": ["pattern"]
    }
)

SEARCH_TOOLS_SCHEMAS = [SEARCH_FILES_SCHEMA]
