"""Prompt building and system message construction."""

from datetime import datetime
from typing import Any

from app.config import SYSTEM_PROMPT


def build_system_prompt(memory: str | None = None) -> str:
    """
    Build the system prompt with context and memory.
    
    Args:
        memory: Previous conversation memory (optional)
        
    Returns:
        Complete system prompt
    """
    prompt = SYSTEM_PROMPT
    
    if memory:
        prompt += f"\n\n## Previous Context:\n{memory}"
    
    prompt += f"\n\nCurrent time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return prompt


def format_tool_result(tool_call_id: str, result: str) -> dict[str, Any]:
    """Format tool execution result for the API."""
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": result
    }


def format_message(role: str, content: str) -> dict[str, str]:
    """Format a message for the API."""
    return {"role": role, "content": content}
