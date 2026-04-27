from app.core.prompts import build_system_prompt
from app.config import SYSTEM_PROMPT

def test_build_system_prompt_basic():
    prompt = build_system_prompt()
    assert SYSTEM_PROMPT in prompt
    assert "Current time:" in prompt

def test_build_system_prompt_with_memory():
    memory = "User likes Python."
    prompt = build_system_prompt(memory)
    
    assert SYSTEM_PROMPT in prompt
    assert "Previous Context:" in prompt
    assert memory in prompt