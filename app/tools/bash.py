"""Bash command execution tool."""

import subprocess

from app.tools.base import ToolError


# Dangerous commands to block for safety
DANGEROUS_COMMANDS = [
    "rm -rf", "sudo", "dd", "format", ":(){", 
    "chmod", "chown", "mkfs", "shutdown", "reboot"
]


def run_bash(command: str) -> str:
    """
    Run a bash command and return output.
    
    Args:
        command: Bash command to run
        
    Returns:
        Command output
        
    Raises:
        ToolError: If command fails or is unsafe
    """
    try:
        # Security: block dangerous commands
        cmd_clean = command.lower().strip()
        if any(dangerous in cmd_clean for dangerous in DANGEROUS_COMMANDS):
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
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Error running command: {str(e)}")
