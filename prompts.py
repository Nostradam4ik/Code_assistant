"""Prompt building and system message construction."""

from datetime import datetime
from typing import Optional
from config import SYSTEM_PROMPT


def build_system_prompt(memory: Optional[str] = None) -> str:
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


def format_tool_result(tool_name: str, result: str, is_error: bool = False) -> dict:
    """
    Format tool execution result for the API.
    
    Args:
        tool_name: Name of the tool that was called
        result: Result from the tool execution
        is_error: Whether this is an error result
        
    Returns:
        Formatted tool result for API
    """
    return {
        "type": "tool_result",
        "tool_use_id": tool_name,  # In real implementation, use actual ID from API
        "content": result,
        "is_error": is_error
    }


def format_message(role: str, content: str) -> dict:
    """Format a message for the API."""
    return {"role": role, "content": content}
