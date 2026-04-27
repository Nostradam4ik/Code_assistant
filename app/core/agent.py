"""AI Assistant agent with tool calling."""

import json
from typing import Any, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from app.config import ASSISTANT_NAME, THEME, MAX_TOOL_ITERATIONS, MAX_HISTORY_MESSAGES
from app.llm import GroqClient
from app.core import MemoryManager, build_system_prompt
from app.tools import get_registry, ToolError


class Agent:
    """AI coding assistant with Groq API and tool support."""
    
    def __init__(self, client: GroqClient, memory: MemoryManager) -> None:
        """
        Initialize the agent.
        
        Args:
            client: Groq API client
            memory: Memory manager for persistence
        """
        self.client = client
        self.memory = memory
        self.console = Console()
        self.registry = get_registry()
        self.conversation_history: list[dict[str, Any]] = []
    
    def chat(self, user_message: str) -> Optional[str]:
        """
        Send a message and get a response from the assistant.
        
        Args:
            user_message: User's input message
            
        Returns:
            Assistant's response, or None if error
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Build system prompt with memory
        memory_context = self.memory.read_memory()
        system_prompt = build_system_prompt(memory_context if memory_context else None)
        
        # Trim history before the first API call
        self._trim_history()
        
        try:
            # Call Groq API
            response = self.client.create_message(
                messages=[
                    {"role": "system", "content": system_prompt},
                    *self.conversation_history
                ],
                tools=self.registry.get_all_schemas(),
                max_tokens=2048,
            )
            
            # Process response
            assistant_message = response.choices[0].message
            
            # Handle tool calls in a loop
            iterations = 0
            while assistant_message.tool_calls and iterations < MAX_TOOL_ITERATIONS:
                iterations += 1
                # Print assistant's thinking
                if assistant_message.content:
                    self._print_response(assistant_message.content)
                
                # Add assistant message to history
                assistant_history_entry = {
                    "role": "assistant",
                    "content": assistant_message.content or ""
                }
                if assistant_message.tool_calls:
                    assistant_history_entry["tool_calls"] = assistant_message.tool_calls
                self.conversation_history.append(assistant_history_entry)
                
                # Execute tool calls
                tool_results = self._execute_tool_calls(assistant_message.tool_calls)
                
                # Add tool results to history
                self.conversation_history.extend(tool_results)
                
                # Trim history before subsequent API calls in the tool loop
                self._trim_history()
                
                # Get next response from assistant
                response = self.client.create_message(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history
                    ],
                    tools=self.registry.get_all_schemas(),
                    max_tokens=2048,
                )
                
                assistant_message = response.choices[0].message
            
            if iterations >= MAX_TOOL_ITERATIONS:
                self.console.print(
                    f"[{THEME['warning']}]⚠️ Maximum tool iterations ({MAX_TOOL_ITERATIONS}) reached. Stopping.[/{THEME['warning']}]"
                )

            # Print final response
            if assistant_message.content:
                self._print_response(assistant_message.content)
            
            # Add final message to history
            final_message_entry = {
                "role": "assistant",
                "content": assistant_message.content or ""
            }
            if assistant_message.tool_calls:
                final_message_entry["tool_calls"] = assistant_message.tool_calls
            self.conversation_history.append(final_message_entry)
            
            # Store in memory
            self.memory.add_entry("user", user_message)
            self.memory.add_entry("assistant", assistant_message.content or "(no response)")
            
            return assistant_message.content
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.console.print(f"[{THEME['error']}]{error_msg}[/{THEME['error']}]")
            return None

    def _trim_history(self) -> None:
        """Keep only the first message and the last N messages to manage context window."""
        if len(self.conversation_history) > MAX_HISTORY_MESSAGES:
            first_message = self.conversation_history[0]
            self.conversation_history = [first_message] + self.conversation_history[-MAX_HISTORY_MESSAGES:]
    
    def _execute_tool_calls(self, tool_calls: Any) -> list[dict[str, Any]]:
        """
        Execute tool calls and return results.
        
        Args:
            tool_calls: Tool calls from API response
            
        Returns:
            List of tool results
        """
        tool_results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = tool_call.function.arguments
            
            # Parse JSON arguments
            if isinstance(tool_args, str):
                try:
                    tool_args = json.loads(tool_args)
                except json.JSONDecodeError:
                    tool_args = {}
            
            self.console.print(
                f"\n[{THEME['tool']}]🔧 Calling tool: {tool_name}[/{THEME['tool']}]"
            )
            
            try:
                result = self.registry.execute(tool_name, **tool_args)
                self.console.print(f"[{THEME['success']}]✓ Success[/{THEME['success']}]\n{result}")
                
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            except ToolError as e:
                error_msg = str(e)
                self.console.print(f"[{THEME['error']}]✗ Error: {error_msg}[/{THEME['error']}]")
                
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Error: {error_msg}"
                })
        
        return tool_results
    
    def _print_response(self, content: str) -> None:
        """Print a response in a panel."""
        self.console.print(
            Panel(
                content,
                title=f"[{THEME['assistant']}]{ASSISTANT_NAME}[/{THEME['assistant']}]",
                border_style=THEME['assistant']
            )
        )
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        welcome_text = f"""
# Welcome to {ASSISTANT_NAME}

A local Python-based AI coding assistant powered by Groq.

**Features:**
- 📝 Read, write, and edit files
- 🔍 Search code patterns
- 💻 Run bash commands
- 💾 Persistent conversation memory
- ⚡ Fast inference with Groq API

**Commands:**
- Type your request to interact with the assistant
- Type `clear` to clear conversation memory
- Type `exit` or `quit` to exit

---
"""
        self.console.print(Markdown(welcome_text))
    
    def run(self) -> None:
        """Main chat loop."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask(
                    f"[{THEME['user']}]You[/{THEME['user']}]"
                ).strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit"]:
                    self.console.print(
                        f"[{THEME['info']}]Goodbye![/{THEME['info']}]"
                    )
                    break
                
                if user_input.lower() == "clear":
                    self.memory.clear()
                    self.conversation_history.clear()
                    self.console.print(
                        f"[{THEME['success']}]✓ Memory and conversation cleared[/{THEME['success']}]"
                    )
                    continue
                
                # Process user message
                self.chat(user_input)
                
            except KeyboardInterrupt:
                self.console.print(
                    f"\n[{THEME['info']}]Interrupted by user[/{THEME['info']}]"
                )
                break
            except Exception as e:
                self.console.print(
                    f"[{THEME['error']}]Unexpected error: {str(e)}[/{THEME['error']}]"
                )
