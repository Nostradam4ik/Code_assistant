"""Groq API client wrapper."""

from typing import Any

from groq import Groq


class GroqClient:
    """Wrapper around Groq API client."""
    
    def __init__(self, api_key: str, model: str) -> None:
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key
            model: Model name to use
            
        Raises:
            ValueError: If API key is empty
        """
        if not api_key:
            raise ValueError("GROQ_API_KEY cannot be empty")
        
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def create_message(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> Any:
        """
        Create a chat completion message.
        
        Args:
            messages: List of message dicts with role/content
            tools: Optional list of tool definitions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            API response object
        """
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        return self.client.chat.completions.create(**kwargs)
