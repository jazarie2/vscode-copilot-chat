# VSCodey CLI

A simple command-line interface to interact with GitHub Copilot Chat in VS Code.

## Overview

VSCodey CLI is a streamlined tool that focuses specifically on interfacing with VS Code's built-in GitHub Copilot Chat functionality. Instead of implementing its own AI models and chat systems, it leverages VS Code's `vscode.copilot` API and chat participants.

## Features

- **Direct VS Code Integration**: Opens VS Code with Copilot Chat for seamless workflow
- **File Context**: Include specific files as context for your questions
- **Workspace Context**: Add workspace information to your chat
- **Simple Interface**: Minimal, focused command-line interface
- **Native Copilot Experience**: Uses VS Code's native Copilot Chat with all its features

## Prerequisites

1. **VS Code**: Must be installed with the `code` command available in PATH
2. **GitHub Copilot Chat Extension**: Must be installed and configured in VS Code
3. **GitHub Copilot Subscription**: Active GitHub Copilot subscription

## Installation

Simply download `vscodey-cli.py` - no additional dependencies required beyond Python 3.6+.

## Usage

### Basic Chat
```bash
python vscodey-cli.py chat "How do I create a Python function?"
```

### Chat with File Context
```bash
python vscodey-cli.py chat "Explain this code" --file main.py
python vscodey-cli.py chat "Review this function" --file src/utils.py --file src/helpers.py
```

### Chat with Workspace Context
```bash
python vscodey-cli.py chat "Analyze the project structure" --context
python vscodey-cli.py chat "Suggest improvements" --file main.py --context
```

### Interactive Mode
```bash
python vscodey-cli.py interactive
```

### Help
```bash
python vscodey-cli.py help
```

## How It Works

VSCodey CLI:

1. **Validates** that VS Code and GitHub Copilot Chat are available
2. **Prepares context** from files and workspace (if requested)
3. **Opens VS Code** in your workspace
4. **Displays the formatted message** for you to paste into Copilot Chat

This approach ensures you get the full VS Code Copilot experience with all its features:
- All chat participants (`@workspace`, `@vscode`, `@terminal`, etc.)
- Slash commands (`/explain`, `/fix`, `/help`, etc.)
- Code actions and inline editing
- Full integration with your VS Code environment

## VS Code Copilot Chat Features

When VS Code opens, you can use all native Copilot Chat features:

### Chat Participants
- `@copilot` - General programming help and code assistance
- `@workspace` - Workspace-wide code analysis and operations
- `@vscode` - VS Code features, settings, and extensions help
- `@terminal` - Command-line and shell assistance

### Slash Commands
- `/explain` - Explain selected code
- `/fix` - Fix problems in selected code
- `/help` - Get help with VS Code features
- `/new` - Create new files or projects
- `/clear` - Clear chat history

### Keyboard Shortcuts
- `Ctrl+Alt+I` (or `Cmd+Alt+I` on Mac) - Open Copilot Chat
- `Ctrl+I` - Start inline chat for code editing

## Examples

### Code Review Workflow
```bash
# Review a specific file
python vscodey-cli.py chat "Please review this code for best practices and potential issues" --file src/app.py

# Analyze project structure
python vscodey-cli.py chat "Analyze the overall architecture of this project" --context

# Get debugging help
python vscodey-cli.py chat "Help me debug this error" --file error_log.txt --file problematic_file.py
```

### Learning and Documentation
```bash
# Understand code
python vscodey-cli.py chat "Explain how this algorithm works" --file algorithms.py

# Get help with specific technologies
python vscodey-cli.py chat "How do I set up testing for this Python project?" --context

# Generate documentation
python vscodey-cli.py chat "Generate documentation for this API" --file api.py
```

### Development Tasks
```bash
# Get implementation suggestions
python vscodey-cli.py chat "Implement a user authentication system" --context

# Optimize code
python vscodey-cli.py chat "Optimize this function for better performance" --file slow_function.py

# Create tests
python vscodey-cli.py chat "Create unit tests for this module" --file my_module.py
```

## Benefits of This Approach

1. **Full Feature Access**: Get all VS Code Copilot Chat features without reimplementation
2. **Native Experience**: Familiar VS Code interface and keyboard shortcuts
3. **Always Updated**: Automatically benefits from VS Code and Copilot updates
4. **Simple Maintenance**: Minimal code to maintain vs. complex AI integration
5. **Workspace Integration**: Full access to VS Code's workspace understanding
6. **Extension Ecosystem**: Works with all your VS Code extensions

## Troubleshooting

### VS Code Not Found
```bash
# Install VS Code command line tools
# In VS Code: View > Command Palette > "Shell Command: Install 'code' command in PATH"
```

### Copilot Extension Not Found
```bash
# Install from VS Code marketplace or command line
code --install-extension GitHub.copilot-chat
```

### Permission Issues
Make sure your GitHub Copilot subscription is active and you're signed in to VS Code.

## Command Reference

```bash
# Basic usage
python vscodey-cli.py chat "your message"

# With options
python vscodey-cli.py chat "your message" [OPTIONS]
  --file, -f <path>          # Include specific files (can be used multiple times)
  --context, -c              # Include workspace context
  --workspace <path>         # Specify workspace directory
  --verbose, -v              # Enable verbose output

# Interactive mode
python vscodey-cli.py interactive

# Help and information
python vscodey-cli.py help
python vscodey-cli.py --help
python vscodey-cli.py --version
```

## Why This Approach?

Instead of building a complex CLI tool that tries to replicate VS Code's Copilot functionality, VSCodey CLI takes a different approach:

- **Leverage existing tools**: Use VS Code's mature Copilot integration
- **Maintain simplicity**: Minimal codebase to maintain
- **Ensure compatibility**: Always compatible with latest Copilot features
- **Provide convenience**: Bridge between command line and VS Code workflows

This makes VSCodey CLI a lightweight, reliable tool that enhances your development workflow without duplicating functionality that already exists in VS Code.
