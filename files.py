"""Execution logic for file operations."""

from pathlib import Path
from app.tools.base import ToolError, is_safe_path, format_size
from app.config import MAX_FILE_SIZE

def read_file(file_path: str) -> str:
    try:
        path = Path(file_path).resolve()
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        if not path.exists():
            raise ToolError(f"File not found: {file_path}")
        if path.stat().st_size > MAX_FILE_SIZE:
            raise ToolError(f"File too large: {format_size(path.stat().st_size)}")
        
        return path.read_text(encoding='utf-8')
    except Exception as e:
        raise ToolError(f"Error reading file: {str(e)}")

def write_file(file_path: str, content: str) -> str:
    try:
        path = Path(file_path).resolve()
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        raise ToolError(f"Error writing file: {str(e)}")

def edit_file(file_path: str, start_line: int, end_line: int, replacement: str) -> str:
    try:
        path = Path(file_path).resolve()
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        lines = path.read_text().splitlines(keepends=True)
        if start_line < 1 or end_line > len(lines):
            raise ToolError(f"Line range {start_line}-{end_line} out of bounds")
        
        lines[start_line-1:end_line] = [replacement + ('\n' if not replacement.endswith('\n') else '')]
        path.write_text("".join(lines))
        return f"Successfully edited lines {start_line}-{end_line} in {file_path}"
    except Exception as e:
        raise ToolError(f"Error editing file: {str(e)}")

def list_files(directory: str = ".") -> str:
    try:
        path = Path(directory).resolve()
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {directory} is outside workspace")
        
        items = sorted(path.iterdir())
        result = [f"Contents of {directory}:"]
        for item in items:
            prefix = "📁" if item.is_dir() else "📄"
            result.append(f"  {prefix} {item.name}")
        return "\n".join(result)
    except Exception as e:
        raise ToolError(f"Error listing files: {str(e)}")