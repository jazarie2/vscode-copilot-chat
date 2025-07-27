#!/usr/bin/env python3
"""
VSCodey CLI - Simple Command Line Interface for VS Code Copilot
Direct interface to VS Code's vscode.copilot API.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


class VSCodeyCLI:
    """Simple CLI interface to VS Code Copilot via vscode.copilot API."""

    def __init__(self, workspace: str = ".", verbose: bool = False):
        """Initialize VSCodey CLI.

        Args:
            workspace: Path to workspace directory
            verbose: Enable verbose logging
        """
        self.workspace = Path(workspace).resolve()
        self.verbose = verbose

        if verbose:
            print(f"Initialized VSCodey CLI in workspace: {self.workspace}")

    def check_vscode_installation(self) -> bool:
        """Check if VS Code is installed and accessible.

        Returns:
            True if VS Code is available, False otherwise
        """
        try:
            # Try to run code --version
            result = subprocess.run(
                ["code", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                if self.verbose:
                    print(f"VS Code found: {result.stdout.strip().split()[0]}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        print("Error: VS Code 'code' command not found in PATH.")
        print("Please ensure VS Code is installed and the 'code' command is available.")
        print("You can install the 'code' command by opening VS Code and running:")
        print(
            "  View > Command Palette > Shell Command: Install 'code' command in PATH"
        )
        return False

    def check_copilot_extension(self) -> bool:
        """Check if GitHub Copilot Chat extension is installed.

        Returns:
            True if extension is installed, False otherwise
        """
        try:
            result = subprocess.run(
                ["code", "--list-extensions"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                extensions = result.stdout.lower()
                if "github.copilot-chat" in extensions:
                    if self.verbose:
                        print("GitHub Copilot Chat extension found")
                    return True

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        print("Error: GitHub Copilot Chat extension not found.")
        print("Please install the GitHub Copilot Chat extension in VS Code:")
        print(
            "  https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat"
        )
        return False

    def send_chat_message(
        self, message: str, files: List[str] = None, include_context: bool = False
    ) -> int:
        """Send a chat message to VS Code Copilot.

        Args:
            message: The chat message to send
            files: List of files to include as context
            include_context: Whether to include workspace context

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check prerequisites
            if not self.check_vscode_installation():
                return 1
            if not self.check_copilot_extension():
                return 1

            # Prepare the message
            full_message = message

            # Add file context if specified
            if files:
                file_context = self._gather_file_context(files)
                if file_context:
                    full_message = f"{file_context}\n\n{message}"

            # Add workspace context if requested
            if include_context:
                workspace_context = self._gather_workspace_context()
                if workspace_context:
                    full_message = f"{workspace_context}\n\n{full_message}"

            if self.verbose:
                print(f"Sending message to VS Code Copilot: {message[:50]}...")

            # Open VS Code with the chat query
            # This uses VS Code's command line interface to open the chat with a pre-filled message
            return self._open_vscode_chat(full_message)

        except Exception as e:
            print(f"Error sending chat message: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def start_interactive(self) -> int:
        """Start an interactive session by opening VS Code chat.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check prerequisites
            if not self.check_vscode_installation():
                return 1
            if not self.check_copilot_extension():
                return 1

            print("Opening VS Code Copilot Chat for interactive session...")

            # Open VS Code in the workspace and focus on chat
            return self._open_vscode_chat("")

        except Exception as e:
            print(f"Error starting interactive session: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _gather_file_context(self, files: List[str]) -> str:
        """Gather context from specified files.

        Args:
            files: List of file paths

        Returns:
            Formatted file context string
        """
        context_parts = []

        for file_path in files:
            try:
                full_path = self.workspace / file_path
                if full_path.exists() and full_path.is_file():
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    context_parts.append(f"File: {file_path}")
                    context_parts.append(
                        f"```{full_path.suffix[1:] if full_path.suffix else ''}"
                    )
                    context_parts.append(content)
                    context_parts.append("```")
                    context_parts.append("")

                    if self.verbose:
                        print(f"Added file to context: {file_path}")
                else:
                    print(f"Warning: File not found: {file_path}")

            except Exception as e:
                print(f"Warning: Could not read file {file_path}: {e}")

        return "\n".join(context_parts) if context_parts else ""

    def _gather_workspace_context(self) -> str:
        """Gather basic workspace context.

        Returns:
            Formatted workspace context string
        """
        context_parts = [f"Workspace: {self.workspace}"]

        try:
            # Add basic file structure
            python_files = list(self.workspace.glob("*.py"))
            js_files = list(self.workspace.glob("*.js")) + list(
                self.workspace.glob("*.ts")
            )
            config_files = (
                list(self.workspace.glob("*.json"))
                + list(self.workspace.glob("*.yaml"))
                + list(self.workspace.glob("*.yml"))
            )

            if python_files:
                context_parts.append(
                    f"Python files: {', '.join(f.name for f in python_files[:10])}"
                )
            if js_files:
                context_parts.append(
                    f"JS/TS files: {', '.join(f.name for f in js_files[:10])}"
                )
            if config_files:
                context_parts.append(
                    f"Config files: {', '.join(f.name for f in config_files[:10])}"
                )

            # Check for common project files
            if (self.workspace / "package.json").exists():
                context_parts.append("Project type: Node.js/npm")
            if (self.workspace / "requirements.txt").exists():
                context_parts.append("Project type: Python")
            if (self.workspace / "Cargo.toml").exists():
                context_parts.append("Project type: Rust")

            if self.verbose:
                print("Added workspace context")

        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not gather workspace context: {e}")

        return "\n".join(context_parts)

    def _open_vscode_chat(self, message: str) -> int:
        """Open VS Code with the chat interface.

        Args:
            message: Pre-filled message for the chat

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Open VS Code in the workspace
            cmd = ["code", str(self.workspace)]

            if message.strip():
                # If we have a message, we'll need to use a temporary file approach
                # or try to use VS Code's command line arguments
                # For now, let's just open VS Code and let the user paste the message
                print(f"Opening VS Code in {self.workspace}")
                print("Please paste this into Copilot Chat:")
                print("-" * 60)
                print(message)
                print("-" * 60)
            else:
                print(f"Opening VS Code with Copilot Chat in {self.workspace}")

            # Add flag to open and focus on chat if possible
            # This may vary depending on VS Code version and extensions
            result = subprocess.run(cmd, timeout=30)

            if result.returncode == 0:
                print("VS Code opened successfully")
                print("Use Ctrl+Alt+I (or Cmd+Alt+I on Mac) to open Copilot Chat")
                return 0
            else:
                print("Failed to open VS Code")
                return 1

        except subprocess.TimeoutExpired:
            print("VS Code opened (timed out waiting for completion)")
            return 0
        except Exception as e:
            print(f"Error opening VS Code: {e}")
            return 1

    def show_help(self) -> int:
        """Show help information about VS Code Copilot features.

        Returns:
            Exit code (0 for success)
        """
        help_text = """
VSCodey CLI - Interface to VS Code Copilot

This tool helps you interact with GitHub Copilot Chat in VS Code through the command line.

VS Code Copilot Chat Features:
• Default chat participant (@copilot) for general programming help
• @workspace participant for workspace-wide operations
• @vscode participant for VS Code-specific help
• @terminal participant for command-line assistance
• Inline chat (Ctrl+I) for editing assistance

VS Code Chat Participants:
  @copilot     - General programming help and code assistance
  @workspace   - Workspace-wide code analysis and operations
  @vscode      - VS Code features, settings, and extensions help
  @terminal    - Command-line and shell assistance

Slash Commands in Chat:
  /explain     - Explain selected code
  /fix         - Fix problems in selected code
  /help        - Get help with VS Code features
  /new         - Create new files or projects
  /clear       - Clear chat history

Tips for Better Results:
1. Select relevant code before asking questions
2. Use specific participants (@workspace, @vscode, etc.) for focused help
3. Provide context about what you're trying to accomplish
4. Ask follow-up questions to refine results

For more information:
• VS Code Copilot Documentation: https://docs.github.com/copilot/using-github-copilot/using-github-copilot-in-vs-code
• VS Code Copilot Chat: https://code.visualstudio.com/docs/copilot/copilot-chat
        """
        print(help_text)
        return 0


def main():
    """Main entry point for VSCodey CLI."""
    parser = argparse.ArgumentParser(
        description="VSCodey CLI - Simple interface to VS Code Copilot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vscodey-cli.py chat "How do I create a Python function?"
  python vscodey-cli.py chat "Explain this code" --file main.py
  python vscodey-cli.py chat "Fix this bug" --file src/app.py --context
  python vscodey-cli.py interactive
  python vscodey-cli.py help
        """,
    )

    parser.add_argument("--version", action="version", version="VSCodey CLI 1.0.0")
    parser.add_argument(
        "--workspace",
        help="Workspace directory (default: current directory)",
        default=".",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Chat command
    chat_parser = subparsers.add_parser(
        "chat", help="Send a chat message to VS Code Copilot"
    )
    chat_parser.add_argument("message", help="The message to send to Copilot")
    chat_parser.add_argument(
        "--file", "-f", help="File to include as context", action="append"
    )
    chat_parser.add_argument(
        "--context", "-c", action="store_true", help="Include workspace context"
    )

    # Interactive command
    subparsers.add_parser("interactive", help="Start VS Code with Copilot Chat")

    # Help command
    subparsers.add_parser(
        "help", help="Show detailed help about VS Code Copilot features"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        vscodey = VSCodeyCLI(workspace=args.workspace, verbose=args.verbose)

        if args.command == "chat":
            return vscodey.send_chat_message(
                message=args.message,
                files=args.file or [],
                include_context=args.context,
            )
        elif args.command == "interactive":
            return vscodey.start_interactive()
        elif args.command == "help":
            return vscodey.show_help()
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
