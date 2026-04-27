"""Tool implementations for file operations and bash commands."""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional
from config import MAX_FILE_SIZE


class ToolError(Exception):
    """Base exception for tool errors."""
    pass


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
        
        # Security: prevent reading outside workspace
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
        
        # Security check
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {file_path} is outside workspace")
        
        # Create parent directories if needed
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
        
        # Validate line numbers (1-indexed)
        if start_line < 1 or end_line < start_line or end_line > len(lines):
            raise ToolError(
                f"Invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)"
            )
        
        # Replace lines (convert to 0-indexed)
        new_lines = lines[:start_line - 1] + [replacement] + lines[end_line:]
        
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
        
        # Search through Python files (can be extended)
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


def run_bash(command: str) -> str:
    """
    Run a bash command and return output.
    
    Args:
        command: Bash command to run
        
    Returns:
        Command output
        
    Raises:
        ToolError: If command fails
    """
    try:
        # Security: block dangerous commands
        dangerous_commands = ["rm -rf", "sudo", "dd", "format", ":(){"]
        if any(cmd in command.lower() for cmd in dangerous_commands):
            raise ToolError(f"Command denied for safety: {command}")
        
        # Run command with timeout
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr
        
        if result.returncode != 0:
            return f"Command failed with exit code {result.returncode}:\n{output}"
        
        return output.strip() if output.strip() else "(No output)"
    
    except subprocess.TimeoutExpired:
        raise ToolError("Command timed out (10 second limit)")
    except Exception as e:
        raise ToolError(f"Error running command: {str(e)}")


def is_safe_path(path: Path) -> bool:
    """Check if path is within the current working directory (security)."""
    try:
        cwd = Path.cwd().resolve()
        path.resolve().relative_to(cwd)
        return True
    except ValueError:
        return False


def format_size(bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"


# Tool definitions for Groq API
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file (creates or overwrites)",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace specific lines in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to edit"
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Starting line number (1-indexed)"
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Ending line number (1-indexed, inclusive)"
                    },
                    "replacement": {
                        "type": "string",
                        "description": "Text to replace with"
                    }
                },
                "required": ["file_path", "start_line", "end_line", "replacement"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path (defaults to current directory)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for a regex pattern in files",
            "parameters": {
                "type": "object",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Run a bash command and return output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Bash command to run"
                    }
                },
                "required": ["command"]
            }
        }
    }
]


def call_tool(name: str, **kwargs) -> str:
    """Call a tool by name with given arguments."""
    tools_map = {
        "read_file": read_file,
        "write_file": write_file,
        "edit_file": edit_file,
        "list_files": list_files,
        "search_files": search_files,
        "run_bash": run_bash,
    }
    
    if name not in tools_map:
        raise ToolError(f"Unknown tool: {name}")
    
    try:
        return tools_map[name](**kwargs)
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Tool execution error: {str(e)}")
