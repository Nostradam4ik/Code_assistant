"""Execution logic for bash commands."""

import subprocess
from app.tools.base import ToolError

def run_bash(command: str) -> str:
    try:
        dangerous = ["rm -rf", "sudo", "dd", "format"]
        if any(cmd in command.lower() for cmd in dangerous):
            raise ToolError(f"Command denied for safety: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[Errors]\n{result.stderr}"
        
        return output if output.strip() else "(Command executed with no output)"
    except subprocess.TimeoutExpired:
        raise ToolError("Command timed out after 30 seconds")
    except Exception as e:
        raise ToolError(f"Execution failed: {str(e)}")