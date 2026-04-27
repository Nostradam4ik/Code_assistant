"""Tool registry and management system."""

from dataclasses import dataclass
from typing import Any, Callable, Optional
import json

from app.tools.base import ToolError


@dataclass
class ToolSchema:
    """JSON Schema for tool inputs."""
    
    type: str = "object"
    properties: dict[str, Any] | None = None
    required: list[str] | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for Groq API."""
        return {
            "type": self.type,
            "properties": self.properties or {},
            "required": self.required or []
        }


class Tool:
    """Represents a single tool that the AI can call."""
    
    def __init__(
        self,
        name: str,
        description: str,
        schema: ToolSchema,
        func: Callable[..., str],
    ) -> None:
        """
        Initialize a tool.
        
        Args:
            name: Tool name (used in tool calls)
            description: Human-readable description
            schema: Input schema (what parameters the tool accepts)
            func: Python function to execute the tool
        """
        self.name = name
        self.description = description
        self.schema = schema
        self.func = func
    
    def to_groq_schema(self) -> dict[str, Any]:
        """Convert to Groq API tool schema format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.schema.to_dict()
            }
        }
    
    def execute(self, **kwargs: Any) -> str:
        """
        Execute the tool with given arguments.
        
        Args:
            **kwargs: Arguments matching the schema
            
        Returns:
            Tool result as string
            
        Raises:
            ToolError: If execution fails
        """
        try:
            return self.func(**kwargs)
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Tool execution failed: {str(e)}")


class ToolRegistry:
    """Registry and dispatcher for all available tools."""
    
    def __init__(self) -> None:
        """Initialize empty tool registry."""
        self._tools: dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool: Tool to register
            
        Raises:
            ValueError: If tool name already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Tool:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool object
            
        Raises:
            ToolError: If tool not found
        """
        if name not in self._tools:
            raise ToolError(f"Unknown tool: {name}")
        return self._tools[name]
    
    def execute(self, name: str, **kwargs: Any) -> str:
        """
        Execute a tool by name.
        
        Args:
            name: Tool name
            **kwargs: Tool arguments
            
        Returns:
            Tool result
            
        Raises:
            ToolError: If tool not found or execution fails
        """
        tool = self.get(name)
        return tool.execute(**kwargs)
    
    def get_all_schemas(self) -> list[dict[str, Any]]:
        """
        Get schemas for all registered tools (for Groq API).
        
        Returns:
            List of tool schemas in Groq format
        """
        return [tool.to_groq_schema() for tool in self._tools.values()]
    
    def get_tools_list(self) -> list[Tool]:
        """Get list of all registered tools."""
        return list(self._tools.values())
    
    def __len__(self) -> int:
        """Number of registered tools."""
        return len(self._tools)
    
    def __contains__(self, name: str) -> bool:
        """Check if tool is registered."""
        return name in self._tools


# Global registry instance
_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def register_tool(tool: Tool) -> None:
    """Register a tool in the global registry."""
    get_registry().register(tool)


def execute_tool(name: str, **kwargs: Any) -> str:
    """Execute a tool by name using the global registry."""
    return get_registry().execute(name, **kwargs)
