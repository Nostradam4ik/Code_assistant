# CodeAssist 🤖

AI Code Assistant powered by **Groq** — modular Python CLI tool for coding tasks.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (get free at console.groq.com)
$env:GROQ_API_KEY="your_key_here"  # PowerShell
# OR
export GROQ_API_KEY=your_key_here  # Bash/Zsh

# Run the assistant
python assistant.py
```

## Architecture

Clean, modular design with separated concerns:

```
assistant.py     → Main CLI loop & chat handler (AIAssistant class)
├── config.py   → API keys, constants, system prompt
├── tools.py    → Tool implementations (read, write, edit, list, search, bash)
├── prompts.py  → Prompt building & formatting
└── memory.py   → MemoryManager for conversation persistence
```

### Key Modules

| File | Purpose |
|------|---------|
| **assistant.py** | AIAssistant class with chat loop, tool calling, response handling |
| **config.py** | GROQ_API_KEY, model name, MEMORY.md path, system prompt template |
| **tools.py** | 6 tool implementations + TOOLS definition for Groq API + tool executor |
| **prompts.py** | System prompt builder, message formatting helpers |
| **memory.py** | MemoryManager class — read/write/trim MEMORY.md entries |
| **MEMORY.md** | Persistent conversation context (auto-trimmed to 50 entries) |

## Features

✅ **Modular Architecture** — Each concern in its own module
✅ **Tool Calling** — Groq API function calling with 6 built-in tools
✅ **Persistent Memory** — Conversation history saved to MEMORY.md
✅ **Rich Terminal UI** — Colored panels, markdown rendering
✅ **Error Handling** — Safe bash execution, file validation
✅ **Extensible** — Easy to add new tools to tools.py

## Available Tools

| Tool | Description |
|------|-------------|
| 📖 **read_file** | Read file contents (with optional line range) |
| ✏️ **write_file** | Create or overwrite a file |
| ✏️ **edit_file** | Replace lines in a file (by line numbers) |
| 📁 **list_files** | List directory contents |
| 🔍 **search_files** | Search with regex pattern in Python files |
| ⚡ **run_bash** | Execute bash commands (with timeout) |

## CLI Commands

| Input | Action |
|-------|--------|
| Normal text | Send message to assistant |
| `exit` or `quit` | Exit the program |
| `clear` | Clear conversation memory |

## Example Usage

```
You: Create a Python function to parse CSV files

You: Add error handling to the login endpoint

You: Write tests for the UserService class

You: Search for all database queries in the project

You: Fix the Docker setup for development
```

The assistant will:
1. Understand your request
2. Use tools to read/modify files as needed
3. Run commands to test changes
4. Save important context to MEMORY.md
5. Report what was done

## How Tool Calling Works

1. **You** send a message
2. **Assistant** determines which tools are needed
3. **Groq API** returns tool calls (function names + arguments)
4. **assistant.py** executes each tool and collects results
5. **Results** sent back to Groq API for final response
6. **Memory** updated with conversation entry

## Safety Features

- ✅ Blocks dangerous bash commands (`rm -rf`, `sudo`, `dd`, `format`, etc.)
- ✅ File size limit (10MB) to prevent huge file reads
- ✅ Works only within current workspace directory
- ✅ 10-second timeout for bash commands

## Models Available (Groq Free Tier)

| Model | Context | Speed | Notes |
|-------|---------|-------|-------|
| `mixtral-8x7b-32768` | 32k | Fast | Default (good balance) |
| `llama-3.3-70b-versatile` | 128k | Fast | Versatile, recommended |
| `llama-3.1-8b-instant` | 128k | Ultra-fast | Quick tasks |

Change model in config.py: `GROQ_MODEL = "..."`

## Project Structure

```
code_assistant/
├── assistant.py       # Main entry point & chat loop
├── config.py         # Configuration
├── tools.py          # Tool implementations
├── prompts.py        # Prompt building
├── memory.py         # Memory management
├── MEMORY.md         # Persisted conversation
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key
1. Visit https://console.groq.com
2. Sign up (free)
3. Create an API key
4. Set environment variable:
   ```bash
   export GROQ_API_KEY=gsk_... # (Windows: use set instead of export)
   ```

### 3. Run
```bash
python assistant.py
```

## Extending with New Tools

To add a new tool:

1. **Implement function** in tools.py:
   ```python
   def my_new_tool(param1: str, param2: int) -> str:
       """Description."""
       return "result"
   ```

2. **Add to TOOLS list** with Groq schema

3. **Add to TOOL_MAP** in call_tool()

4. It's automatically available to the assistant!

## Troubleshooting

**"GROQ_API_KEY not set"**
→ Set environment variable before running

**Tool execution fails**
→ Check console output for error message, file paths exist, etc.

**Memory file too large**
→ It auto-trims to 50 entries; you can manually clear with `clear` command

## Performance

- First message: ~1-2s (API latency)
- Tool execution: ~100ms per tool
- File I/O: <100ms for typical files
- Memory management: <10ms

## Architecture Principles

- **Modularity**: Each module has a single responsibility
- **Extensibility**: Easy to add new tools or change prompts
- **Safety**: Input validation, command whitelisting
- **Transparency**: Clear console output of what's happening
- **Persistence**: Memory across sessions
