import pytest
from unittest.mock import MagicMock
from app.core.agent import Agent

def test_agent_chat_basic_flow(mock_groq, mock_memory):
    """Test that agent correctly processes a simple user message."""
    agent = Agent(client=mock_groq, memory=mock_memory)
    
    user_input = "Hello, assistant!"
    response = agent.chat(user_input)
    
    assert response == "Default assistant response"
    # Verify history: 1 user message + 1 assistant message
    assert len(agent.conversation_history) == 2
    assert agent.conversation_history[0]["role"] == "user"
    assert agent.conversation_history[0]["content"] == user_input
    
    # Verify memory was updated
    assert mock_memory.add_entry.call_count == 2

def test_agent_chat_with_tool_loop(mock_groq, mock_memory):
    """Test that agent handles tool calls and continues the conversation."""
    agent = Agent(client=mock_groq, memory=mock_memory)
    
    # First response triggers a tool
    tool_call = MagicMock()
    tool_call.id = "call_123"
    tool_call.function.name = "list_files"
    tool_call.function.arguments = "{}"
    
    resp_with_tool = MagicMock()
    resp_with_tool.choices = [MagicMock()]
    resp_with_tool.choices[0].message.content = "Checking files..."
    resp_with_tool.choices[0].message.tool_calls = [tool_call]
    
    # Final response after tool execution
    final_resp = MagicMock()
    final_resp.choices = [MagicMock()]
    final_resp.choices[0].message.content = "I found 0 files."
    final_resp.choices[0].message.tool_calls = None
    
    mock_groq.create_message.side_effect = [resp_with_tool, final_resp]
    
    response = agent.chat("What files are here?")
    
    assert response == "I found 0 files."
    assert mock_groq.create_message.call_count == 2