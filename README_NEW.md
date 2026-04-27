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
app/
├── main.py           → Entry point, initializes components
├── config.py         → Configuration, API keys, constants
├── llm/
│   └── groq_client.py    → Groq API wrapper
├── core/
│   ├── agent.py          → Agent class (main chat loop)
│   ├── prompts.py        → Prompt building utilities
│   └── memory.py         → MemoryManager for persistence
└── tools/
    ├── base.py       → Tool utilities & schema helpers
    ├── files.py      → File operations (read, write, edit, list)
    ├── bash.py       → Bash command execution
    └── search.py     → File pattern searching
```

### Key Modules

| Module | Purpose |
|--------|---------|
| **app/main.py** | Application entry point, dependency initialization |
| **app/config.py** | API keys, model, constants, system prompt template |
| **app/llm/groq_client.py** | Groq API client wrapper with clean interface |
| **app/core/agent.py** | Agent class with chat loop, tool calling, response handling |
| **app/core/prompts.py** | System prompt builder, message formatting |
| **app/core/memory.py** | MemoryManager — read/write/trim MEMORY.md |
| **app/tools/base.py** | Shared utilities, safety checks, schema helpers |
| **app/tools/files.py** | File I/O tools with schemas |
| **app/tools/bash.py** | Bash execution tool (sandboxed) |
| **app/tools/search.py** | Regex search tool for files |

## Features

✅ **Modular Architecture** — Each concern in its own module, easy to extend
✅ **Type Hints** — Full type annotations throughout codebase
✅ **Tool Calling** — Groq API function calling with 6 built-in tools
✅ **Persistent Memory** — Conversation history saved to MEMORY.md
✅ **Rich Terminal UI** — Colored panels, markdown rendering
✅ **Error Handling** — Safe bash execution, file validation
✅ **Clean Imports** — Well-organized with __init__.py files
✅ **Extensible** — Easy to add new tools or change behavior

## Available Tools

| Tool | Module | Description |
|------|--------|-------------|
| 📖 **read_file** | tools/files.py | Read file contents (with validation) |
| ✏️ **write_file** | tools/files.py | Create or overwrite a file |
| ✏️ **edit_file** | tools/files.py | Replace lines in a file |
| 📁 **list_files** | tools/files.py | List directory contents |
| 🔍 **search_files** | tools/search.py | Regex pattern search in files |
| ⚡ **run_bash** | tools/bash.py | Execute bash commands (safe) |

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
2. **Agent** determines which tools are needed
3. **Groq API** returns tool calls (function names + arguments)
4. **app/tools/** executes each tool and collects results
5. **Results** sent back to Groq API for final response
6. **Memory** updated with conversation entry

## Safety Features

- ✅ Blocks dangerous bash commands (`rm -rf`, `sudo`, `dd`, etc.)
- ✅ File size limit (10MB) to prevent huge reads
- ✅ Works only within current workspace directory
- ✅ 10-second timeout for bash commands
- ✅ Path validation on all file operations

## Models Available (Groq Free Tier)

| Model | Context | Speed | Notes |
|-------|---------|-------|-------|
| `mixtral-8x7b-32768` | 32k | Fast | Default (good balance) |
| `llama-3.3-70b-versatile` | 128k | Fast | Versatile, recommended |
| `llama-3.1-8b-instant` | 128k | Ultra-fast | Quick tasks |

Change model in [app/config.py](app/config.py): `GROQ_MODEL = "..."`

## Project Structure

```
code_assistant/
├── app/                   # Main application package
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── config.py         # Configuration
│   ├── llm/              # LLM integration
│   │   ├── __init__.py
│   │   └── groq_client.py
│   ├── core/             # Core functionality
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── memory.py
│   └── tools/            # Tool implementations
│       ├── __init__.py
│       ├── base.py
│       ├── files.py
│       ├── bash.py
│       └── search.py
├── assistant.py          # Wrapper entry point
├── MEMORY.md            # Persisted conversation
├── requirements.txt     # Dependencies
└── README.md            # This file
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
   $env:GROQ_API_KEY="gsk_..."  # PowerShell
   # OR
   export GROQ_API_KEY=gsk_...  # Bash/Zsh
   ```

### 3. Run
```bash
python assistant.py
```

## Extending with New Tools

### 1. Create tool function in appropriate module
Example: Add to `app/tools/files.py`:
```python
def my_operation(param: str) -> str:
    """Description."""
    return "result"
```

### 2. Create schema
```python
MY_SCHEMA = get_tool_schema(
    "my_operation",
    "Description",
    {
        "properties": {
            "param": {"type": "string", "description": "..."}
        },
        "required": ["param"]
    }
)
```

### 3. Export from __init__.py
```python
# app/tools/__init__.py
MY_TOOLS_SCHEMAS = [MY_SCHEMA]
# Add to TOOLS list at bottom
TOOLS = FILE_TOOLS_SCHEMAS + BASH_TOOLS_SCHEMAS + SEARCH_TOOLS_SCHEMAS + MY_TOOLS_SCHEMAS

# Add to TOOL_FUNCTIONS
TOOL_FUNCTIONS = {
    ...
    "my_operation": my_operation,
}
```

It's automatically available to the assistant!

## Troubleshooting

**"GROQ_API_KEY not set"**
→ Set environment variable before running

**Tool execution fails**
→ Check console output for error message, validate file paths, etc.

**Memory file too large**
→ It auto-trims to 50 entries; manually clear with `clear` command

**Import errors after refactor**
→ Ensure you're running from project root directory

## Performance

- First message: ~1-2s (API latency)
- Tool execution: ~100ms per tool
- File I/O: <100ms for typical files
- Memory management: <10ms

## Architecture Principles

- **Modularity**: Each module has a single responsibility
- **Extensibility**: Easy to add new tools or modify behavior
- **Type Safety**: Full type hints for IDE support
- **Safety**: Input validation, command whitelisting, path checks
- **Clean Imports**: Well-organized module hierarchy
- **Transparency**: Clear console output of operations
- **Persistence**: Memory across sessions
