# AI Agent

This is a toy version of something like Cursor/Zed's Agentic Mode, or Claude Code, utilizing the free gemini model. We hardcoded the working directory to be /calculator, such that access of the agent is restricted to it and its subdirectories.

The AI Agent can:
- view the directory-structure
- read files
- write files
- run python code

To use it, run main.py, followed by the user prompt in quotes. Optionally, a --verbose tag can be added to give more info about tokens spent etc.
