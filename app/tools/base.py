"""Base tool class and utilities."""

from pathlib import Path
from typing import Any

from app.config import MAX_FILE_SIZE


class ToolError(Exception):
    """Base exception for tool errors."""
    pass


def is_safe_path(path: Path) -> bool:
    """Check if path is within the current working directory (security)."""
    try:
        cwd = Path.cwd().resolve()
        path.resolve().relative_to(cwd)
        return True
    except ValueError:
        return False


def format_size(bytes_count: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024:
            return f"{bytes_count:.1f}{unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f}TB"


def get_tool_schema(
    name: str,
    description: str,
    parameters: dict[str, Any]
) -> dict[str, Any]:
    """Create a Groq API tool schema."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters.get("properties", {}),
                "required": parameters.get("required", [])
            }
        }
    }
