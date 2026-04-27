import pytest
from pathlib import Path
from app.core.memory import save_memory
from app.config import MEMORY_FILE

@pytest.fixture(autouse=True)
def clean_memory(tmp_path, monkeypatch):
    """Redirect memory file to a temp location for testing."""
    temp_mem = tmp_path / "TEST_MEMORY.md"
    monkeypatch.setattr("app.core.memory.MEMORY_FILE", str(temp_mem))
    return temp_mem

def test_save_memory_creates_file(clean_memory):
    content = "Project uses FastAPI."
    result = save_memory(content)
    
    assert "successfully saved" in result
    assert clean_memory.exists()
    
    file_content = clean_memory.read_text()
    assert content in file_content
    assert "PERSISTENT CONTEXT" in file_content