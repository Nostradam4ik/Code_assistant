"""Execution logic for searching files."""

import re
from pathlib import Path
from app.tools.base import ToolError, is_safe_path

def search_files(pattern: str, directory: str = ".") -> str:
    try:
        path = Path(directory).resolve()
        if not is_safe_path(path):
            raise ToolError(f"Access denied: {directory} is outside workspace")
            
        regex = re.compile(pattern)
        results = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                try:
                    content = file_path.read_text(errors='ignore')
                    if regex.search(content):
                        results.append(str(file_path.relative_to(path.parent)))
                except: continue
        
        return f"Matches for '{pattern}':\n" + "\n".join(results) if results else "No matches found."
    except Exception as e:
        raise ToolError(f"Search failed: {str(e)}")