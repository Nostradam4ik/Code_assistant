# Copilot Instructions

## Project goal
Build a local AI coding assistant for software development tasks.

## Stack
- Python 3.11+
- Groq API
- CLI-first architecture
- Rich for terminal UI
- Optional FastAPI backend later
- Optional React frontend later

## Coding principles
- Prefer simple, modular architecture.
- Keep files small and focused.
- Avoid unnecessary abstractions.
- Use type hints in Python code.
- Prefer dataclasses or Pydantic models for structured data.
- Keep side effects isolated.
- Do not add dependencies unless necessary.
- Reuse existing utilities before creating new ones.

## Architecture rules
- Separate LLM orchestration from tool implementations.
- Keep tools in their own module.
- Put prompt-building logic in a dedicated module.
- Keep memory/state management separate from chat loop.
- Make every tool return structured results.
- Design for future support of multiple models, not only Groq.

## Tooling rules
- Before editing code, inspect existing project structure.
- When adding a feature, update related tests if tests exist.
- For bug fixes, prefer minimal safe changes.
- For refactors, preserve behavior unless explicitly asked otherwise.

## Output expectations
- Explain the short plan first.
- Then implement the change.
- Then show changed files.
- Then suggest validation steps.