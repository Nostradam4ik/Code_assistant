"""File operation tools."""

from pathlib import Path

from app.config import MAX_FILE_SIZE
from app.tools.base import ToolError, is_safe_path, format_size


def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as a string
        
    Raises:
        ToolError: If file doesn't exist or is too large
    """
    try:
        path = Path(file_path).resolve()
        
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        if not path.exists():
            raise ToolError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ToolError(f"Not a file: {file_path}")
        
        if path.stat().st_size > MAX_FILE_SIZE:
            raise ToolError(f"File too large: {path.stat().st_size} bytes (max {MAX_FILE_SIZE})")
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error reading file: {str(e)}")


def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file (creates or overwrites).
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        
    Returns:
        Success message
        
    Raises:
        ToolError: If write fails
    """
    try:
        path = Path(file_path).resolve()
        
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully wrote {len(content)} bytes to {file_path}"
    
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error writing file: {str(e)}")


def edit_file(file_path: str, start_line: int, end_line: int, replacement: str) -> str:
    """
    Replace lines in a file.
    
    Args:
        file_path: Path to the file to edit
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed, inclusive)
        replacement: Text to replace with
        
    Returns:
        Success message
        
    Raises:
        ToolError: If edit fails
    """
    try:
        path = Path(file_path).resolve()
        
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        if not path.exists():
            raise ToolError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if start_line < 1 or end_line < start_line or end_line > len(lines):
            raise ToolError(
                f"Invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)"
            )
        
        # Ensure the replacement ends with a newline to preserve file structure
        formatted_replacement = replacement
        if not formatted_replacement.endswith('\n'):
            formatted_replacement += '\n'
            
        new_lines = lines[:start_line - 1] + [formatted_replacement] + lines[end_line:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return f"Successfully edited {file_path} (lines {start_line}-{end_line})"
    
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error editing file: {str(e)}")


def list_files(directory: str = ".") -> str:
    """
    List files and directories in a directory.
    
    Args:
        directory: Directory path (defaults to current directory)
        
    Returns:
        Formatted list of files and directories
        
    Raises:
        ToolError: If directory doesn't exist
    """
    try:
        path = Path(directory).resolve()
        
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {directory} is outside workspace")
        
        if not path.exists():
            raise ToolError(f"Directory not found: {directory}")
        
        if not path.is_dir():
            raise ToolError(f"Not a directory: {directory}")
        
        items = sorted(path.iterdir())
        result = []
        
        for item in items:
            if item.is_dir():
                result.append(f"  📁 {item.name}/")
            else:
                size = item.stat().st_size
                size_str = format_size(size)
                result.append(f"  📄 {item.name} ({size_str})")
        
        if not result:
            return f"Directory is empty: {directory}"
        
        return f"Contents of {directory}:\n" + "\n".join(result)
    
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error listing directory: {str(e)}")
