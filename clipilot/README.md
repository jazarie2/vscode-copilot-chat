# CLI Pilot

CLI Pilot is a comprehensive command-line interface that brings GitHub Copilot Chat functionality to your terminal. It features multiple AI agents, real command execution, file system operations through MCP (Model Context Protocol) tools, and support for 7 different AI models.

## 🚀 Features

- **🤖 4 Specialized AI Agents**: Workspace, VS Code, Terminal, and Agent Mode
- **🧠 7 AI Models**: GPT-4.1, GPT-4o Mini, Claude 3.5/3.7 Sonnet, Gemini 2.0 Flash, O1, O1-mini
- **💬 Interactive Chat**: Persistent chat sessions with conversation history
- **🖥️ Real Command Execution**: Terminal agent executes actual shell commands
- **📁 MCP Tool Integration**: Filesystem, web search, and GitHub operations
- **🔧 Workspace Intelligence**: Automatic project analysis and context gathering
- **⚙️ Dynamic Configuration**: Model switching, agent selection, and MCP management
- **🔐 Secure Authentication**: GitHub OAuth and token management

## 🎯 AI Agents

### 🏢 **Workspace Agent** (Default)
Specializes in project-wide operations, file analysis, and code understanding.
```bash
python main.py chat "analyze the project structure" --agent workspace
python main.py chat "suggest architectural improvements" --agent workspace
```

### 🎨 **VS Code Agent**
Helps with VS Code features, extensions, settings, and editor functionality.
```bash
python main.py chat "how to configure debugging" --agent vscode
python main.py chat "recommend extensions for Python" --agent vscode
```

### 🖥️ **Terminal Agent**
Executes real shell commands and assists with terminal workflows.
```bash
python main.py chat "show current directory" --agent terminal
python main.py chat "list all Python files" --agent terminal
python main.py chat "find large files" --agent terminal
```

### 🤖 **Agent Mode**
Autonomous multi-step task execution with MCP tool integration.
```bash
python main.py chat "read main.py and analyze its structure" --agent agent
python main.py chat "search for TODO comments in all files" --agent agent
```

## 🧠 AI Models

Choose from 7 different AI models, each with unique capabilities:

```bash
# GPT Models
python main.py chat "hello" --model gpt-4.1-2025-04-14
python main.py chat "hello" --model gpt-4o-mini

# Claude Models  
python main.py chat "hello" --model claude-3.5-sonnet
python main.py chat "hello" --model claude-3.7-sonnet

# Gemini Models
python main.py chat "hello" --model gemini-2.0-flash-001

# OpenAI o1 Models (Advanced Reasoning)
python main.py chat "solve this complex algorithm" --model o1
python main.py chat "explain quantum computing" --model o1-mini
```

## 🔧 MCP (Model Context Protocol) Tools

CLI Pilot integrates with 3 MCP servers for enhanced functionality:

### 📁 **Filesystem MCP Server**
Real file operations and directory navigation.
```bash
# Agent mode automatically uses filesystem tools
python main.py chat "read config.py and summarize it" --agent agent
python main.py chat "list all Python files in src directory" --agent agent
```

### 🔍 **Brave Search MCP Server**  
Web search capabilities for research and documentation.
```bash
# Enable/disable search capabilities
python main.py mcp enable brave-search
python main.py mcp disable brave-search
```

### 🐙 **GitHub MCP Server**
GitHub repository operations and API access.
```bash
# Manage GitHub integration
python main.py mcp enable github
python main.py mcp disable github
```

### MCP Management Commands
```bash
# List all MCP servers
python main.py mcp list

# Enable a specific server
python main.py mcp enable filesystem

# Disable a specific server  
python main.py mcp disable brave-search
```

## 🚀 Quick Start

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

4. **List Available Options**:
   ```bash
   python main.py list-models    # View all 7 AI models
   python main.py list-agents    # View all 4 agents
   python main.py mcp list       # View MCP servers
   ```

## 💡 Comprehensive Usage Examples

### 🔍 **Code Analysis & Understanding**
```bash
# Analyze project structure
python main.py chat "analyze this project structure" --agent workspace

# Explain specific code files
python main.py chat "explain this code" --file main.py --agent workspace

# Get coding help with context
python main.py chat "how to improve this function" --file utils.py --context
```

### 🖥️ **Terminal Operations (Real Command Execution)**
```bash
# Get current directory (executes real pwd)
python main.py chat "show current directory" --agent terminal

# List files (executes real ls/dir)
python main.py chat "list all files" --agent terminal

# Find files by pattern
python main.py chat "find all Python files" --agent terminal

# Check disk usage
python main.py chat "show disk usage" --agent terminal
```

### 🤖 **Agent Mode - Autonomous File Operations**
```bash
# Read and analyze files using MCP tools
python main.py chat "read package.json and tell me about dependencies" --agent agent

# Search across codebase
python main.py chat "find all TODO comments in Python files" --agent agent

# Analyze multiple files
python main.py chat "compare main.py with cli_core.py" --agent agent

# Generate documentation from code
python main.py chat "create documentation for config.py" --agent agent
```

### 🎨 **VS Code Integration Help**
```bash
# Extension recommendations
python main.py chat "recommend extensions for Python development" --agent vscode

# Debugging setup
python main.py chat "how to configure Python debugging" --agent vscode

# Settings optimization
python main.py chat "optimize VS Code for large projects" --agent vscode

# Workspace configuration
python main.py chat "set up multi-root workspace" --agent vscode
```

### 🧠 **Model-Specific Capabilities**
```bash
# GPT-4.1 for code generation
python main.py chat "create a REST API in Python" --model gpt-4.1-2025-04-14

# Claude for code analysis
python main.py chat "review this code for best practices" --model claude-3.5-sonnet

# O1 for complex reasoning
python main.py chat "design a scalable microservices architecture" --model o1

# Gemini for fast responses
python main.py chat "quick syntax help for list comprehensions" --model gemini-2.0-flash-001
```

### 💬 **Interactive Sessions**
```bash
# Start interactive mode with specific agent/model
python main.py interactive --agent workspace --model claude-3.5-sonnet

# In interactive mode, use special commands:
/help      # Show available commands
/context   # Display workspace information
/files     # List relevant files
/history   # Show conversation history
/clear     # Clear session history
/exit      # Exit interactive mode
```

### ⚙️ **Configuration Management**
```bash
# Model management
python main.py list-models                    # List all available models
python main.py set-model claude-3.5-sonnet   # Set default model

# Agent management  
python main.py list-agents                    # List all agents
python main.py set-agent terminal             # Set default agent

# MCP server management
python main.py mcp list                       # Show all MCP servers
python main.py mcp enable filesystem         # Enable filesystem tools
python main.py mcp disable brave-search      # Disable web search
```

### 🔄 **Advanced Workflows**
```bash
# Multi-agent workflow
python main.py chat "pwd" --agent terminal
python main.py chat "analyze current project" --agent workspace  
python main.py chat "read main.py" --agent agent

# Model comparison
python main.py chat "explain recursion" --model gpt-4.1-2025-04-14
python main.py chat "explain recursion" --model claude-3.5-sonnet
python main.py chat "explain recursion" --model o1-mini

# Context-aware development
python main.py chat "fix this bug" --file buggy_script.py --context --agent workspace
python main.py chat "run tests" --agent terminal
python main.py chat "create unit tests" --file fixed_script.py --agent agent
```

### 🎯 **Specialized Use Cases**
```bash
# Code review workflow
python main.py chat "review this PR" --file changed_file.py --model claude-3.5-sonnet --agent workspace

# Learning and education
python main.py chat "explain design patterns with examples" --model o1 --agent workspace

# Quick scripting help
python main.py chat "create a file backup script" --model gpt-4o-mini --agent terminal

# Project setup assistance
python main.py chat "set up Python project structure" --agent workspace --context

# Documentation generation
python main.py chat "generate API docs" --file api.py --agent agent

# Performance optimization
python main.py chat "optimize this algorithm" --file slow_function.py --model o1 --agent workspace
```

## Configuration

CLI Pilot stores configuration in `~/.clipilot/config.json`. You can customize:

- Authentication tokens
- Default agents and models
- File inclusion/exclusion patterns
- UI preferences

## 📋 Command Reference

### 🔐 **Authentication Commands**
```bash
python main.py auth login              # GitHub OAuth authentication
python main.py auth status             # Check authentication status  
python main.py auth logout             # Remove stored credentials
python main.py setup --token <token>   # Manual token setup
```

### 💬 **Chat Commands**
```bash
# Basic chat
python main.py chat <message>

# With options
python main.py chat <message> [OPTIONS]
  --file, -f <path>          # Include specific files
  --context, -c              # Include workspace context
  --agent <agent-id>         # Use specific agent
  --model <model-id>         # Use specific model
  --workspace <path>         # Specify workspace directory
  --verbose                  # Enable verbose output
  --config <path>            # Custom configuration file
```

### 🔄 **Interactive Mode**
```bash
python main.py interactive [OPTIONS]
  --agent <agent-id>         # Start with specific agent
  --model <model-id>         # Start with specific model
```

### ⚙️ **Configuration Commands**
```bash
# Model management
python main.py list-models             # List all available models
python main.py set-model <model-id>    # Set default model

# Agent management
python main.py list-agents             # List all available agents  
python main.py set-agent <agent-id>    # Set default agent

# MCP server management
python main.py mcp list                # List MCP servers
python main.py mcp enable <server-id>  # Enable MCP server
python main.py mcp disable <server-id> # Disable MCP server
```

### 🆘 **Help & Information**
```bash
python main.py --help                  # Show main help
python main.py --version               # Show version
python main.py <command> --help        # Command-specific help
```

## 🎮 Interactive Commands

When in interactive mode (`python main.py interactive`), you can use these special commands:

### 📋 **Navigation Commands**
```bash
/help                    # Show available commands and usage tips
/context                 # Display current workspace context information  
/files                   # List relevant files in the workspace
/history                 # Show recent chat history
/clear                   # Clear the current chat history
/exit                    # Exit the interactive session
```

### 🔄 **Dynamic Switching**
```bash
/agent <agent-id>        # Switch to different agent mid-session
/model <model-id>        # Switch to different model mid-session
/mcp enable <server>     # Enable MCP server during session
/mcp disable <server>    # Disable MCP server during session
```

### 📁 **Context Management**
```bash
/file <path>             # Add file to current context
/workspace <path>        # Change workspace directory
/include <pattern>       # Include files matching pattern
/exclude <pattern>       # Exclude files matching pattern
```

## 🔧 Advanced Configuration

### 📝 **Configuration File Structure**
CLI Pilot stores configuration in `~/.clipilot/config.json`:

```json
{
  "auth": {
    "token": "your-github-copilot-token",
    "expires_at": "2025-12-31T23:59:59Z"
  },
  "chat": {
    "default_agent": "workspace",
    "default_model": "claude-3.5-sonnet", 
    "max_context_size": 8192,
    "temperature": 0.1
  },
  "agents": {
    "workspace": {
      "enabled": true,
      "capabilities": ["file_analysis", "workspace_context", "project_structure"]
    },
    "terminal": {
      "enabled": true,
      "shell": "powershell",
      "capabilities": ["shell_commands", "command_line", "scripting"]
    },
    "agent": {
      "enabled": true,
      "mcp_servers": ["filesystem", "brave-search", "github"]
    }
  },
  "mcp": {
    "enabled": true,
    "servers": {
      "filesystem": {
        "enabled": true,
        "command": "npx -y @modelcontextprotocol/server-filesystem /",
        "capabilities": ["file_read", "file_write", "directory_list"]
      },
      "brave-search": {
        "enabled": true,
        "command": "npx -y @modelcontextprotocol/server-brave-search",
        "environment": ["BRAVE_API_KEY"]
      },
      "github": {
        "enabled": true,
        "command": "npx -y @modelcontextprotocol/server-github",
        "environment": ["GITHUB_PERSONAL_ACCESS_TOKEN"]
      }
    }
  },
  "workspace": {
    "include_patterns": ["*.py", "*.js", "*.ts", "*.md", "*.json"],
    "exclude_patterns": ["node_modules/**", ".git/**", "__pycache__/**", "*.pyc"],
    "max_file_size": 1048576,
    "auto_context": true
  },
  "ui": {
    "color_output": true,
    "show_typing_indicator": true,
    "markdown_rendering": true,
    "code_highlighting": true
  },
  "models": {
    "gpt-4.1-2025-04-14": {
      "name": "GPT-4.1",
      "max_tokens": 4096,
      "supports_tools": true,
      "supports_vision": true
    },
    "claude-3.5-sonnet": {
      "name": "Claude 3.5 Sonnet", 
      "max_tokens": 8192,
      "supports_tools": true,
      "supports_vision": true
    }
  }
}
```

### 🎛️ **Environment Variables**
```bash
# Authentication
export GITHUB_TOKEN="your-token"
export CLIPILOT_CONFIG_PATH="/custom/config/path"

# MCP Server Configuration
export BRAVE_API_KEY="your-brave-search-key"
export GITHUB_PERSONAL_ACCESS_TOKEN="your-github-token"

# CLI Pilot Behavior
export CLIPILOT_DEFAULT_AGENT="terminal"
export CLIPILOT_DEFAULT_MODEL="claude-3.5-sonnet"
export CLIPILOT_VERBOSE="true"
```

### 🔧 **Advanced Usage Patterns**
```bash
# Workspace-specific configuration
python main.py --config ./project-config.json chat "analyze project"

# Custom workspace with specific patterns
python main.py --workspace /path/to/project chat "help with project" --context

# Pipeline usage with different models
python main.py chat "analyze code" --model claude-3.5-sonnet | 
python main.py chat "create tests based on this analysis" --model gpt-4.1-2025-04-14

# Batch processing with agent mode
for file in *.py; do
  python main.py chat "analyze $file" --file "$file" --agent agent
done
```

## 🎯 Real-World Usage Examples

### 🏗️ **Project Setup & Architecture**
```bash
# Initialize new Python project
python main.py chat "create Python project structure" --agent workspace --model gpt-4.1-2025-04-14

# Analyze existing project
python main.py chat "analyze project architecture and suggest improvements" --context --agent workspace

# Setup development environment
python main.py chat "configure VS Code for this project" --agent vscode --context

# Create Docker configuration
python main.py chat "create Dockerfile and docker-compose.yml" --context --agent agent
```

### 📊 **Data Analysis & Science**
```bash
# Data exploration
python main.py chat "analyze this dataset structure" --file data.csv --agent agent --model claude-3.5-sonnet

# Create analysis script
python main.py chat "create data visualization script" --file data.csv --agent workspace

# Statistical analysis
python main.py chat "perform statistical analysis on this data" --file results.json --model o1

# Machine learning workflow
python main.py chat "create ML model for this dataset" --file training_data.csv --agent agent
```

### 🌐 **Web Development**
```bash
# Frontend development
python main.py chat "create React component for user profile" --agent workspace --model gpt-4.1-2025-04-14

# Backend API design
python main.py chat "design REST API for this application" --context --agent workspace --model o1

# Database schema
python main.py chat "create database schema for user management" --agent workspace

# Deployment setup
python main.py chat "create deployment scripts" --context --agent terminal
```

### 🔧 **DevOps & Automation**
```bash
# CI/CD pipeline
python main.py chat "create GitHub Actions workflow" --context --agent agent --model gpt-4.1-2025-04-14

# Infrastructure as code
python main.py chat "create Terraform configuration" --agent workspace --model o1

# Monitoring setup
python main.py chat "setup application monitoring" --context --agent workspace

# Backup scripts
python main.py chat "create automated backup script" --agent terminal
```

### 🐛 **Debugging & Testing**
```bash
# Debug complex issue
python main.py interactive --agent workspace --model claude-3.5-sonnet
# Then: "I have a memory leak in my Python application. Help me debug it."

# Performance optimization
python main.py chat "optimize this slow function" --file slow_module.py --model o1 --agent workspace

# Create comprehensive tests
python main.py chat "create integration tests" --context --agent agent --model gpt-4.1-2025-04-14

# Security audit
python main.py chat "audit this code for security vulnerabilities" --file auth_module.py --model claude-3.5-sonnet
```

### 📚 **Learning & Documentation**
```bash
# Explain complex concepts
python main.py chat "explain microservices architecture with examples" --model o1

# Generate documentation
python main.py chat "create API documentation" --file api.py --agent agent

# Code reviews
python main.py chat "review this pull request" --file changed_files.diff --agent workspace --model claude-3.5-sonnet

# Learning new technology
python main.py chat "teach me GraphQL with practical examples" --model o1
```

### 🔄 **Migration & Refactoring**
```bash
# Language migration
python main.py chat "convert this JavaScript to Python" --file script.js --agent workspace

# Framework migration  
python main.py chat "migrate from Flask to FastAPI" --context --agent workspace --model claude-3.5-sonnet

# Code modernization
python main.py chat "modernize this Python 2 code to Python 3" --file legacy_code.py --agent workspace

# Architecture refactoring
python main.py chat "refactor monolith to microservices" --context --agent workspace --model o1
```

### 🚨 **Emergency Workflows**
```bash
# Production debugging
python main.py chat "analyze this production error" --file error_log.txt --agent workspace --model claude-3.5-sonnet

# Quick fixes
python main.py chat "urgent: fix this critical bug" --file broken_module.py --agent workspace --model gpt-4.1-2025-04-14

# System recovery
python main.py chat "recover from database corruption" --agent terminal --model o1

# Security incident response
python main.py chat "investigate security breach" --context --agent workspace --model claude-3.5-sonnet
```

### 🔬 **Research & Exploration**
```bash
# Technology research
python main.py chat "compare React vs Vue vs Angular for this project" --context --model o1

# Algorithm exploration
python main.py chat "implement different sorting algorithms and compare" --agent workspace --model claude-3.5-sonnet

# Best practices research
python main.py chat "research Python packaging best practices" --model o1

# Market analysis
python main.py chat "analyze competitor features" --agent workspace --model claude-3.5-sonnet
```

### ⚡ **Quick Daily Tasks**
```bash
# Code snippets
python main.py chat "regex for email validation" --model gpt-4o-mini

# Git help
python main.py chat "git commands for feature branch workflow" --agent terminal

# Quick debugging
python main.py chat "why is this not working?" --file broken_code.py --agent workspace

# Syntax help
python main.py chat "Python list comprehension syntax" --model gpt-4o-mini

# Configuration help
python main.py chat "VS Code settings for Python" --agent vscode
```

---

## 🌟 **Summary**

CLI Pilot provides a comprehensive AI-powered development environment with:

- **🤖 4 Specialized Agents** for different development contexts
- **🧠 7 AI Models** with unique capabilities and strengths  
- **🔧 3 MCP Servers** for real tool integration and file operations
- **💬 Interactive & Single-Shot** modes for flexible workflows
- **⚙️ Dynamic Configuration** for personalized development experience

Whether you're debugging complex issues, learning new technologies, setting up projects, or performing daily development tasks, CLI Pilot adapts to your workflow with the right agent, model, and tools for each situation.

**Get started today:**
```bash
python main.py setup
python main.py chat "Hello, help me get started with my project!" --agent workspace
```

---

*Happy coding with CLI Pilot! 🚀*

## 🌟 Best Practices & Tips

### 💡 **Getting Better Results**

1. **🎯 Be Specific**: Describe exactly what you want to achieve
   ```bash
   # ❌ Vague
   python main.py chat "help with code"
   
   # ✅ Specific  
   python main.py chat "refactor this function to use async/await" --file api_client.py
   ```

2. **📁 Include Context**: Use `--file` or `--context` for better understanding
   ```bash
   # Single file context
   python main.py chat "explain this algorithm" --file sorting.py
   
   # Full workspace context
   python main.py chat "suggest project improvements" --context
   ```

3. **🤖 Choose Right Agent**: Match agent to your task
   ```bash
   # Code analysis → Workspace Agent
   python main.py chat "review code quality" --agent workspace
   
   # Command help → Terminal Agent
   python main.py chat "git rebase commands" --agent terminal
   
   # File operations → Agent Mode
   python main.py chat "read all config files" --agent agent
   ```

4. **🧠 Select Appropriate Model**: Different models for different needs
   ```bash
   # Complex reasoning → O1
   python main.py chat "design system architecture" --model o1
   
   # Code analysis → Claude
   python main.py chat "review this code" --model claude-3.5-sonnet
   
   # Quick help → GPT-4o Mini
   python main.py chat "syntax help" --model gpt-4o-mini
   ```

5. **🔄 Use Interactive Mode**: For complex, multi-step tasks
   ```bash
   python main.py interactive --agent workspace --model claude-3.5-sonnet
   ```

### 🛠️ **Workflow Examples**

#### 🔍 **Code Review Workflow**
```bash
# Step 1: Analyze overall structure
python main.py chat "analyze project structure" --agent workspace --context

# Step 2: Review specific files  
python main.py chat "review this module" --file src/main.py --agent workspace

# Step 3: Check for issues
python main.py chat "find potential bugs" --file src/main.py --model claude-3.5-sonnet

# Step 4: Get improvement suggestions
python main.py chat "suggest optimizations" --file src/main.py --model o1
```

#### 🧪 **Testing Workflow**
```bash
# Step 1: Analyze code to test
python main.py chat "understand this function" --file utils.py --agent workspace

# Step 2: Generate test cases
python main.py chat "create unit tests" --file utils.py --agent agent --model gpt-4.1-2025-04-14

# Step 3: Run tests
python main.py chat "run pytest" --agent terminal

# Step 4: Analyze results
python main.py chat "explain test failures" --agent workspace
```

#### 🐛 **Debugging Workflow**
```bash
# Step 1: Understand the problem
python main.py chat "explain this error" --file error_log.txt --agent workspace

# Step 2: Analyze problematic code
python main.py chat "find the bug" --file buggy_code.py --context --model claude-3.5-sonnet

# Step 3: Get fix suggestions
python main.py chat "how to fix this issue" --file buggy_code.py --model o1

# Step 4: Verify fix
python main.py chat "test the fix" --agent terminal
```

## ⚠️ Troubleshooting

### 🔐 **Authentication Issues**

**Problem**: "Not authenticated" error
```bash
# Solution: Re-authenticate
python main.py auth logout
python main.py auth login
```

**Problem**: "Token verification failed"
```bash
# Check token status
python main.py auth status

# Refresh authentication
python main.py auth login
```

### 🤖 **Agent Issues**

**Problem**: Terminal agent not executing commands
```bash
# Check agent capabilities
python main.py list-agents

# Verify shell configuration
python main.py chat "check shell" --agent terminal --verbose
```

**Problem**: Agent mode not reading files
```bash
# Check MCP server status
python main.py mcp list

# Enable filesystem server
python main.py mcp enable filesystem
```

### 🔧 **MCP Server Issues**

**Problem**: MCP tools not available
```bash
# Check server status
python main.py mcp list

# Enable required servers
python main.py mcp enable filesystem
python main.py mcp enable brave-search
python main.py mcp enable github
```

**Problem**: MCP server startup failures
```bash
# Check Node.js installation
node --version
npm --version

# Install MCP packages manually
npx -y @modelcontextprotocol/server-filesystem
```

### 🧠 **Model Issues**

**Problem**: Model not responding correctly
```bash
# List available models
python main.py list-models

# Try different model
python main.py chat "test message" --model claude-3.5-sonnet
```

**Problem**: Model selection not working
```bash
# Check model configuration
python main.py chat "what model are you?" --model gpt-4.1-2025-04-14 --verbose
```

### 📁 **Context Issues**

**Problem**: Files not being included
```bash
# Check workspace directory
python main.py chat "show workspace info" --context --verbose

# Use absolute file paths
python main.py chat "analyze this" --file "/full/path/to/file.py"
```

**Problem**: Large context causing timeouts
```bash
# Reduce context size
python main.py chat "help" --file specific_file.py

# Use focused queries
python main.py chat "explain just this function" --file module.py
```

### 🔄 **Performance Issues**

**Problem**: Slow responses
```bash
# Use faster models
python main.py chat "quick help" --model gpt-4o-mini

# Reduce context
python main.py chat "help" --file small_file.py
```

**Problem**: High memory usage
```bash
# Exclude large directories
python main.py --workspace . chat "help" --context

# Clear interactive history
# In interactive mode: /clear
```

### 🛠️ **Configuration Issues**

**Problem**: Configuration not saving
```bash
# Check config file permissions
ls -la ~/.clipilot/config.json

# Manually create config directory
mkdir -p ~/.clipilot
```

**Problem**: Custom config not loading
```bash
# Verify config path
python main.py --config ./my-config.json chat "test" --verbose

# Check JSON syntax
python -m json.tool ./my-config.json
```

### 📋 **Common Error Messages & Solutions**

| Error | Cause | Solution |
|-------|-------|----------|
| "Module not found" | Missing dependencies | `pip install -r requirements.txt` |
| "Command not recognized" | Invalid command | `python main.py --help` |
| "Agent not found" | Invalid agent ID | `python main.py list-agents` |
| "Model not available" | Invalid model ID | `python main.py list-models` |
| "File not found" | Invalid file path | Use absolute paths or check file exists |
| "Permission denied" | File/directory permissions | Check read/write permissions |
| "Network error" | Connectivity issues | Check internet connection |
| "Rate limit exceeded" | Too many requests | Wait and retry |

### 🔧 **Debug Mode**

Enable verbose output for detailed troubleshooting:
```bash
# Verbose chat
python main.py --verbose chat "debug this" --agent workspace

# Verbose interactive mode
python main.py --verbose interactive

# Check all system information
python main.py --verbose auth status
python main.py --verbose list-models
python main.py --verbose list-agents  
python main.py --verbose mcp list
```