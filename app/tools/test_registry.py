import pytest
from app.tools.registry import ToolRegistry, Tool, ToolSchema, ToolError

def dummy_func(arg: str) -> str:
    return f"processed {arg}"

@pytest.fixture
def registry():
    return ToolRegistry()

@pytest.fixture
def sample_tool():
    return Tool(
        name="test_tool",
        description="A test tool",
        schema=ToolSchema(properties={"arg": {"type": "string"}}, required=["arg"]),
        func=dummy_func
    )

def test_register_and_get_tool(registry, sample_tool):
    registry.register(sample_tool)
    assert registry.get("test_tool") == sample_tool
    assert len(registry.get_all_schemas()) == 1

def test_register_duplicate_fails(registry, sample_tool):
    registry.register(sample_tool)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(sample_tool)

def test_execute_tool(registry, sample_tool):
    registry.register(sample_tool)
    result = registry.execute("test_tool", arg="hello")
    assert result == "processed hello"

def test_execute_unknown_tool_fails(registry):
    with pytest.raises(ToolError, match="Unknown tool"):
        registry.execute("non_existent")

def test_tool_execution_error_wrapping(registry):
    def failing_func():
        raise Exception("Original error")
    
    tool = Tool("fail", "desc", ToolSchema(), failing_func)
    registry.register(tool)
    with pytest.raises(ToolError, match="Tool execution failed: Original error"):
        registry.execute("fail")