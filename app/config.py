"""Configuration and constants for the AI coding assistant."""

import os
from typing import Dict

# Groq API Configuration
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GROQ_MODEL: str = "mixtral-8x7b-32768"

# Assistant Configuration
ASSISTANT_NAME: str = "Code Assistant"
MEMORY_FILE: str = "MEMORY.md"
MAX_TOOL_ITERATIONS: int = 10
MAX_MEMORY_ENTRIES: int = 50
MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

# Rich Terminal Configuration
THEME: Dict[str, str] = {
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "tool": "magenta",
    "user": "blue",
    "assistant": "green",
}

# System Prompt
SYSTEM_PROMPT: str = """You are an AI coding assistant. You help users write, debug, and refactor code.

You have access to tools to interact with the file system and run commands. Use them to:
- Read files to understand code structure
- Write new files or modify existing ones
- Search for patterns in code
- Run bash commands for compilation, testing, etc.
- List directory contents to navigate projects

Guidelines:
- Always explain your actions before using tools
- Ask for clarification if requirements are ambiguous
- Provide code explanations, not just implementations
- Suggest improvements and best practices
- Handle errors gracefully

Remember: You're helping a developer write better code. Focus on education and clarity."""
