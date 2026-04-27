"""Common utilities and base exceptions for tools."""

from pathlib import Path
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
    val = float(bytes_count)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if val < 1024:
            return f"{val:.1f}{unit}"
        val /= 1024
    return f"{val:.1f}TB"