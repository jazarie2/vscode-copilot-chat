# CLI Pilot - GitHub Copilot Chat for Command Line

**CLI Pilot** brings GitHub Copilot Chat functionality to your command line interface, allowing you to interact with Copilot without needing VS Code.

## Features

- 🔐 **GitHub OAuth Authentication** - Secure device flow authentication
- 💬 **Interactive Chat** - Full conversational AI experience in terminal
- 📁 **File Context** - Include specific files or entire workspace context
- 🔧 **Configuration Management** - Persistent settings and authentication
- 🎯 **Multiple Agents** - Support for different AI agents and contexts

## Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd cli-pilot
   ```

2. **Install dependencies:**
   ```bash
   python3 install.py
   ```
   
   This will create a virtual environment and install all dependencies. The installer also creates a `clipilot` launcher script for easy usage.
   
   **Manual installation:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Authentication Setup

### Option 1: OAuth Authentication (Recommended)

The easiest way to authenticate is using GitHub's OAuth device flow:

```bash
./clipilot auth login
```

Or if using the virtual environment directly:
```bash
source venv/bin/activate
python main.py auth login
```

This will:
1. Display a device code and verification URL
2. Open your browser automatically
3. Prompt you to enter the code on GitHub
4. Save the authentication token securely

### Option 2: Manual Token Setup

If you have a GitHub personal access token:

```bash
./clipilot setup --token YOUR_GITHUB_TOKEN
```

## Usage

### Check Authentication Status

```bash
./clipilot auth status
```

### Basic Chat

```bash
./clipilot chat "How do I create a Python function?"
```

### Chat with File Context

```bash
./clipilot chat "Explain this code" --file main.py
```

### Chat with Workspace Context

```bash
./clipilot chat "Fix this bug" --file src/app.py --context
```

### Interactive Session

```bash
./clipilot interactive
```

### Logout

```bash
./clipilot auth logout
```

## Command Reference

### Authentication Commands

- `./clipilot auth login` - Login with GitHub OAuth
- `./clipilot auth status` - Check authentication status
- `./clipilot auth logout` - Remove stored authentication

### Chat Commands

- `./clipilot chat <message>` - Send a single message
  - `--file <path>` - Include specific file(s) as context
  - `--context` - Include workspace context
  - `--agent <agent>` - Use specific agent

### Other Commands

- `./clipilot interactive` - Start interactive session
- `./clipilot setup --token <token>` - Manual token setup
- `./clipilot --help` - Show help message

## Configuration

CLI Pilot stores configuration in `~/.clipilot/config.json`. You can:

- View current settings with `./clipilot auth status`
- Manually edit the config file if needed
- Use `--config <path>` to specify custom config location

## Examples

### Getting Help with Code

```bash
# Ask for general coding help
./clipilot chat "How do I handle exceptions in Python?"

# Get help with specific code
./clipilot chat "Explain this function" --file utils.py

# Debug with context
./clipilot chat "Why is this not working?" --file app.py --context
```

### Interactive Development

```bash
# Start an interactive session
./clipilot interactive

# In interactive mode, you can:
# - Send multiple messages
# - Include files dynamically
# - Switch between agents
# - Get continuous assistance
```

## Troubleshooting

### Authentication Issues

If you encounter authentication problems:

1. **Check your status:**
   ```bash
   ./clipilot auth status
   ```

2. **Re-authenticate:**
   ```bash
   ./clipilot auth logout
   ./clipilot auth login
   ```

3. **Check network connectivity:**
   - Ensure you can access github.com
   - Check firewall/proxy settings

### Common Errors

- **"Not authenticated"** - Run `./clipilot auth login`
- **"Token verification failed"** - Your token may be expired, re-authenticate
- **"Module not found"** - Run `python3 install.py` to reinstall dependencies

## Development

### Project Structure

```
cli-pilot/
├── main.py                 # Main CLI entry point
├── clipilot/               # Core package
│   ├── cli_core.py        # Main CLI logic
│   ├── github_auth.py     # GitHub authentication
│   ├── config.py          # Configuration management
│   ├── chat_interface.py  # Chat functionality
│   └── ...
├── requirements.txt        # Python dependencies
└── install.py             # Installation script
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security

- Tokens are stored securely in your local config
- OAuth flow uses GitHub's official endpoints
- No tokens are logged or transmitted insecurely
- You can revoke access anytime in GitHub settings

## Requirements

- Python 3.7+
- Internet connection for GitHub API
- GitHub account with appropriate permissions

## License

See LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Open an issue in the repository
- Review GitHub Copilot documentation