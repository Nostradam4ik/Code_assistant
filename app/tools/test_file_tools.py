import pytest
import os
from pathlib import Path
from app.tools.files import read_file, write_file, edit_file, list_files
from app.tools.base import ToolError

@pytest.fixture(autouse=True)
def mock_cwd(tmp_path, monkeypatch):
    """Ensure all file operations happen within a safe temporary directory."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    return tmp_path

def test_write_and_read_file(mock_cwd):
    file_path = "test.txt"
    content = "hello world"
    
    write_result = write_file(file_path, content)
    assert "Successfully wrote" in write_result
    
    read_result = read_file(file_path)
    assert read_result == content

def test_read_non_existent_file():
    with pytest.raises(ToolError, match="File not found"):
        read_file("ghost.txt")

def test_edit_file(mock_cwd):
    file_path = "lines.txt"
    original = "line1\nline2\nline3"
    write_file(file_path, original)
    
    # Replace line 2 (1-indexed)
    edit_file(file_path, 2, 2, "new line 2")
    
    result = read_file(file_path)
    assert result == "line1\nnew line 2\nline3"

def test_edit_file_range(mock_cwd):
    file_path = "lines.txt"
    original = "a\nb\nc\nd"
    write_file(file_path, original)
    
    # Replace b and c with 'x'
    edit_file(file_path, 2, 3, "x")
    
    result = read_file(file_path)
    assert result == "a\nx\nd"

def test_list_files(mock_cwd):
    write_file("file1.txt", "content")
    (mock_cwd / "subdir").mkdir()
    write_file("subdir/file2.txt", "content")
    
    result = list_files(".")
    assert "file1.txt" in result
    assert "subdir/" in result

def test_security_boundary(tmp_path, monkeypatch):
    # Create a path outside the 'safe' directory
    outside_dir = tmp_path.parent / "outside"
    outside_dir.mkdir(exist_ok=True)
    
    with pytest.raises(ToolError, match="outside workspace"):
        read_file(str(outside_dir / "secret.txt"))

def test_edit_file_ensures_newline(mock_cwd):
    file_path = "newline_test.txt"
    write_file(file_path, "line1\nline2\nline3")
    
    # Replace line 2 with content missing a newline
    edit_file(file_path, 2, 2, "new_line_2_no_nl")
    
    content = read_file(file_path)
    # Should still have 3 distinct lines
    assert content == "line1\nnew_line_2_no_nl\nline3"