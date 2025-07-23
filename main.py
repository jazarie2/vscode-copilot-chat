#!/usr/bin/env python3
"""
CLI Pilot - Command Line Interface for Copilot Chat
Run GitHub Copilot Chat functionality without VSCode.
"""

import argparse
import sys
import os
from pathlib import Path

# Add clipilot to Python path
sys.path.insert(0, str(Path(__file__).parent / "clipilot"))

from clipilot.cli_core import CLIPilot


def main():
    """Main entry point for CLI Pilot."""
    parser = argparse.ArgumentParser(
        description="CLI Pilot - Run GitHub Copilot Chat without VSCode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py auth login                           # Login with GitHub OAuth
  python main.py auth status                          # Check authentication status
  python main.py chat "How do I create a Python function?"
  python main.py chat "Explain this code" --file main.py
  python main.py chat "Fix this bug" --file src/app.py --context
  python main.py interactive
  python main.py setup --token <your-token>          # Manual token setup
  python main.py --help
        """
    )
    
    parser.add_argument("--version", action="version", version="CLI Pilot 1.0.0")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--workspace", help="Workspace directory (default: current directory)", default=".")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Authentication command
    auth_parser = subparsers.add_parser("auth", help="GitHub authentication management")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", help="Authentication commands")
    
    # Auth login command
    login_parser = auth_subparsers.add_parser("login", help="Login with GitHub OAuth")
    login_parser.add_argument("--client-id", help="Custom GitHub OAuth client ID")
    
    # Auth status command
    status_parser = auth_subparsers.add_parser("status", help="Check authentication status")
    
    # Auth logout command
    logout_parser = auth_subparsers.add_parser("logout", help="Remove stored authentication")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Send a chat message to Copilot")
    chat_parser.add_argument("message", help="The message to send to Copilot")
    chat_parser.add_argument("--file", "-f", help="File to include as context", action="append")
    chat_parser.add_argument("--context", "-c", action="store_true", help="Include workspace context")
    chat_parser.add_argument("--agent", help="Specific agent to use (workspace, vscode, etc.)")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive chat session")
    interactive_parser.add_argument("--agent", help="Specific agent to use")
    
    # Setup command (for manual token setup)
    setup_parser = subparsers.add_parser("setup", help="Setup CLI Pilot configuration manually")
    setup_parser.add_argument("--token", help="GitHub Copilot token")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        clipilot = CLIPilot(
            workspace=args.workspace,
            verbose=args.verbose,
            config_path=args.config
        )
        
        if args.command == "auth":
            if not args.auth_command:
                auth_parser.print_help()
                return 1
            
            if args.auth_command == "login":
                return clipilot.handle_auth_login(client_id=getattr(args, 'client_id', None))
            elif args.auth_command == "status":
                return clipilot.handle_auth_status()
            elif args.auth_command == "logout":
                return clipilot.handle_auth_logout()
        
        elif args.command == "chat":
            return clipilot.handle_chat(
                message=args.message,
                files=args.file or [],
                include_context=args.context,
                agent=args.agent
            )
        elif args.command == "interactive":
            return clipilot.start_interactive(agent=args.agent)
        elif args.command == "setup":
            return clipilot.setup(token=args.token)
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())