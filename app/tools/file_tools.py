"""Tool definitions for file operations."""

from app.tools.registry import Tool, ToolSchema
from app.tools.files import (
    read_file,
    write_file,
    edit_file,
    list_files,
)


# Define tool schemas with clear structure

READ_FILE_TOOL = Tool(
    name="read_file",
    description="Read the complete contents of a file. Use this to examine code, configuration, or any text file.",
    schema=ToolSchema(
        properties={
            "file_path": {
                "type": "string",
                "description": "Path to the file to read (relative or absolute)"
            }
        },
        required=["file_path"]
    ),
    func=read_file,
)

WRITE_FILE_TOOL = Tool(
    name="write_file",
    description="Write content to a file, creating it if it doesn't exist or overwriting if it does. Use for creating new files or complete rewrites.",
    schema=ToolSchema(
        properties={
            "file_path": {
                "type": "string",
                "description": "Path where to write the file"
            },
            "content": {
                "type": "string",
                "description": "Complete file content to write"
            }
        },
        required=["file_path", "content"]
    ),
    func=write_file,
)

EDIT_FILE_TOOL = Tool(
    name="edit_file",
    description="Replace specific lines in a file. Useful for surgical edits without rewriting the entire file.",
    schema=ToolSchema(
        properties={
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
                "description": "Text to replace the lines with"
            }
        },
        required=["file_path", "start_line", "end_line", "replacement"]
    ),
    func=edit_file,
)

LIST_FILES_TOOL = Tool(
    name="list_files",
    description="List files and directories in a directory. Use to explore the project structure or find files.",
    schema=ToolSchema(
        properties={
            "directory": {
                "type": "string",
                "description": "Directory path to list (defaults to current directory)"
            }
        },
        required=[]
    ),
    func=list_files,
)

# Export all file tools
FILE_TOOLS = [
    READ_FILE_TOOL,
    WRITE_FILE_TOOL,
    EDIT_FILE_TOOL,
    LIST_FILES_TOOL,
]
