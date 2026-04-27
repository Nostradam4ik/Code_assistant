import pytest
from pathlib import Path
from unittest.mock import MagicMock
from app.tools.registry import ToolRegistry

@pytest.fixture
def registry():
    """Provides a clean ToolRegistry for testing."""
    return ToolRegistry()

@pytest.fixture
def mock_groq():
    """Provides a mocked Groq client."""
    client = MagicMock()
    # Default setup for a successful non-tool response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Default assistant response"
    mock_response.choices[0].message.tool_calls = None
    client.create_message.return_value = mock_response
    return client

@pytest.fixture
def mock_memory():
    """Provides a mocked Memory manager."""
    memory = MagicMock()
    memory.read_memory.return_value = ""
    return memory

@pytest.fixture
def mock_cwd(tmp_path, monkeypatch):
    """Ensures all file operations happen within a safe temporary directory."""
    monkeypatch.chdir(tmp_path)
    # Mock both pathlib and os-level CWD if necessary, 
    # but primary safety check uses Path.cwd()
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    return tmp_path