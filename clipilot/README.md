# CLI Pilot

CLI Pilot is a command-line interface that provides GitHub Copilot Chat functionality without requiring VSCode. It allows you to interact with AI-powered coding assistance directly from your terminal.

## Features

- **Chat Interface**: Get coding help through a command-line chat interface
- **Interactive Mode**: Start interactive chat sessions with persistent history
- **Workspace Context**: Automatically gather and use workspace information for better responses
- **File Analysis**: Include specific files in your chat context
- **Multiple Agents**: Support for different specialized agents (workspace, general, etc.)
- **Configuration Management**: Flexible configuration system with defaults

## Quick Start

1. **Setup**: Configure CLI Pilot with your credentials
   ```bash
   python main.py setup
   ```

2. **Single Chat**: Ask a quick question
   ```bash
   python main.py chat "How do I create a Python function?"
   ```

3. **Interactive Mode**: Start a persistent chat session
   ```bash
   python main.py interactive
   ```

## Usage Examples

### Basic Chat
```bash
# Simple question
python main.py chat "Explain how recursion works"

# Include a specific file
python main.py chat "Explain this code" --file main.py

# Include workspace context
python main.py chat "Help me refactor this project" --context
```

### Interactive Mode
```bash
python main.py interactive

# In interactive mode, you can use commands:
/help     - Show help
/context  - Show workspace context
/files    - List workspace files
/history  - Show chat history
/clear    - Clear chat history
/exit     - Exit session
```

### Advanced Options
```bash
# Use specific workspace
python main.py --workspace /path/to/project chat "Help with this project"

# Verbose output
python main.py --verbose chat "Debug this issue" --file buggy_script.py

# Custom configuration
python main.py --config /path/to/config.json interactive
```

## Configuration

CLI Pilot stores configuration in `~/.clipilot/config.json`. You can customize:

- Authentication tokens
- Default agents and models
- File inclusion/exclusion patterns
- UI preferences

## Commands

### `setup`
Configure CLI Pilot with authentication and preferences.

### `chat <message>`
Send a single message to Copilot and get a response.

Options:
- `--file`, `-f`: Include specific files in context
- `--context`, `-c`: Include full workspace context
- `--agent`: Use a specific agent

### `interactive`
Start an interactive chat session with persistent history.

Options:
- `--agent`: Use a specific agent

## Interactive Commands

When in interactive mode, you can use these special commands:

- `/help` - Show available commands and usage tips
- `/context` - Display current workspace context information
- `/files` - List relevant files in the workspace
- `/history` - Show recent chat history
- `/clear` - Clear the current chat history
- `/exit` - Exit the interactive session

## Workspace Context

CLI Pilot automatically analyzes your workspace to provide better assistance:

- **File Structure**: Directory tree and file organization
- **Project Type**: Detects Python, Node.js, Java, etc.
- **Git Information**: Current branch, remote URL, recent commits
- **File Analysis**: Relevant source files with content
- **Statistics**: File counts, sizes, and types

## Configuration Options

The configuration file supports these sections:

```json
{
  "auth": {
    "token": "your-github-copilot-token"
  },
  "chat": {
    "default_agent": "workspace",
    "max_context_size": 4096,
    "temperature": 0.1
  },
  "workspace": {
    "include_patterns": ["*.py", "*.js", "*.md"],
    "exclude_patterns": ["node_modules/**", ".git/**"],
    "max_file_size": 1048576
  },
  "ui": {
    "color_output": true,
    "show_typing_indicator": true
  }
}
```

## Tips for Better Results

1. **Be Specific**: Describe exactly what you want to achieve
2. **Include Context**: Use `--file` or `--context` for better understanding
3. **Follow Up**: Ask clarifying questions in interactive mode
4. **Use Examples**: Provide examples of input/output or desired behavior
5. **Mention Constraints**: Specify language, framework, or style preferences

## Troubleshooting

### Configuration Issues
- Run `python main.py setup` to reconfigure
- Check that your token is valid
- Verify file permissions for config directory

### Context Problems
- Ensure you're in the right workspace directory
- Check file patterns in configuration
- Use `--verbose` flag for debugging information

### Performance Issues
- Reduce context size in configuration
- Exclude large directories (build/, node_modules/)
- Limit file inclusion patterns