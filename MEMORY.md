# Conversation Memory

This file stores conversation context and important information about the project discussed with the AI assistant.

## Architecture

The assistant is built with modular components:

- **assistant.py**: Main CLI chat loop (AIAssistant class)
- **config.py**: Configuration, API keys, constants
- **tools.py**: File and bash operations (read, write, edit, list, search, run)
- **prompts.py**: System prompt building
- **memory.py**: MemoryManager class for persistence

## Features

- ✅ Groq API integration with function calling
- ✅ Rich terminal UI with colors and panels
- ✅ Persistent memory in MEMORY.md
- ✅ Modular tools for extensibility
- ✅ Error handling and safety checks (prevents unsafe bash commands)

## Usage

```bash
# Set API key
export GROQ_API_KEY=your_key_here

# Run the assistant
python assistant.py
```

---
