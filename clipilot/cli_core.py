"""
Core CLI functionality for Copilot Chat without VSCode.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import subprocess
import tempfile

from .config import CLIConfig
from .context_manager import WorkspaceContextManager
from .chat_interface import ChatInterface
from .interactive_session import InteractiveSession
from .github_auth import GitHubAuth, perform_github_login, verify_github_token


class CLIPilot:
    """Main CLI Pilot class that orchestrates chat functionality."""
    
    def __init__(self, workspace: str = ".", verbose: bool = False, config_path: Optional[str] = None):
        """Initialize CLI Pilot.
        
        Args:
            workspace: Path to workspace directory
            verbose: Enable verbose logging
            config_path: Path to configuration file
        """
        self.workspace = Path(workspace).resolve()
        self.verbose = verbose
        self.config = CLIConfig(config_path)
        self.context_manager = WorkspaceContextManager(self.workspace, verbose=verbose)
        self.chat_interface = ChatInterface(self.config, verbose=verbose)
        
        if verbose:
            print(f"Initialized CLI Pilot in workspace: {self.workspace}")
    
    def handle_auth_login(self, client_id: Optional[str] = None) -> int:
        """Handle GitHub OAuth login.
        
        Args:
            client_id: Optional custom client ID
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            print("Starting GitHub authentication...")
            
            # Create GitHub auth instance
            github_auth = GitHubAuth(client_id=client_id, verbose=self.verbose)
            
            # Perform authentication
            token = github_auth.authenticate()
            
            if token:
                # Save token to config
                self.config.set_token(token)
                
                # Get user info to display confirmation
                user_info = github_auth.get_user_info(token)
                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    print(f"✓ Successfully authenticated as {name} ({username})")
                else:
                    print("✓ Authentication successful!")
                
                return 0
            else:
                print("✗ Authentication failed")
                return 1
                
        except Exception as e:
            print(f"Authentication error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def handle_auth_status(self) -> int:
        """Handle authentication status check.
        
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            token = self.config.get_token()
            
            if not token:
                print("Not authenticated. Run 'python main.py auth login' to authenticate.")
                return 1
            
            print("Checking authentication status...")
            
            # Verify token is still valid
            if verify_github_token(token, verbose=self.verbose):
                # Get user info
                github_auth = GitHubAuth(verbose=self.verbose)
                user_info = github_auth.get_user_info(token)
                
                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    avatar_url = user_info.get("avatar_url", "")
                    
                    print("✓ Authentication Status: Valid")
                    print(f"  User: {name} ({username})")
                    if avatar_url:
                        print(f"  Profile: https://github.com/{username}")
                else:
                    print("✓ Authentication Status: Valid (unable to get user details)")
                
                return 0
            else:
                print("✗ Authentication Status: Invalid or expired")
                print("Run 'python main.py auth login' to re-authenticate.")
                return 1
                
        except Exception as e:
            print(f"Error checking authentication status: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def handle_auth_logout(self) -> int:
        """Handle authentication logout (remove stored token).
        
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            token = self.config.get_token()
            
            if not token:
                print("Not currently authenticated.")
                return 0
            
            # Remove token from config
            self.config.set_token(None)
            print("✓ Successfully logged out. Authentication token removed.")
            
            return 0
            
        except Exception as e:
            print(f"Error during logout: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def handle_chat(self, message: str, files: List[str] = None, 
                   include_context: bool = False, agent: Optional[str] = None) -> int:
        """Handle a single chat message.
        
        Args:
            message: The chat message
            files: List of files to include as context
            include_context: Whether to include workspace context
            agent: Specific agent to use
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check authentication before processing chat
            if not self._check_authentication():
                return 1
            
            if self.verbose:
                print(f"Processing chat message: {message[:50]}...")
            
            # Gather context
            context = self._gather_context(files, include_context)
            
            # Send to chat interface
            response = self.chat_interface.send_message(
                message=message,
                context=context,
                agent=agent
            )
            
            # Display response
            self._display_response(response)
            
            return 0
            
        except Exception as e:
            print(f"Error processing chat message: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def start_interactive(self, agent: Optional[str] = None) -> int:
        """Start an interactive chat session.
        
        Args:
            agent: Specific agent to use
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check authentication before starting interactive session
            if not self._check_authentication():
                return 1
            
            session = InteractiveSession(
                chat_interface=self.chat_interface,
                context_manager=self.context_manager,
                agent=agent,
                verbose=self.verbose
            )
            return session.run()
            
        except Exception as e:
            print(f"Error in interactive session: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def setup(self, token: Optional[str] = None) -> int:
        """Setup CLI Pilot configuration manually.
        
        Args:
            token: GitHub Copilot token
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            print("Setting up CLI Pilot manually...")
            print("Note: For OAuth authentication, use 'python main.py auth login' instead.")
            
            if not token:
                token = input("Enter your GitHub token: ").strip()
            
            if not token:
                print("Error: Token is required")
                return 1
            
            # Verify token before saving
            if verify_github_token(token, verbose=self.verbose):
                self.config.set_token(token)
                print("✓ Token verified and saved successfully!")
                
                # Get user info to display confirmation
                github_auth = GitHubAuth(verbose=self.verbose)
                user_info = github_auth.get_user_info(token)
                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    print(f"✓ Authenticated as {name} ({username})")
                
                return 0
            else:
                print("✗ Token verification failed. Please check your token.")
                return 1
                
        except Exception as e:
            print(f"Error during setup: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _check_authentication(self) -> bool:
        """Check if user is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        token = self.config.get_token()
        if not token:
            print("Not authenticated. Please run one of the following:")
            print("  python main.py auth login        # OAuth authentication")
            print("  python main.py setup --token ... # Manual token setup")
            return False
        
        # Verify token is still valid
        if not verify_github_token(token, verbose=self.verbose):
            print("Authentication token is invalid or expired.")
            print("Please re-authenticate with: python main.py auth login")
            return False
        
        return True
    
    def _gather_context(self, files: Optional[List[str]] = None, 
                       include_workspace_context: bool = False) -> Dict[str, Any]:
        """Gather context for the chat request.
        
        Args:
            files: List of files to include
            include_workspace_context: Whether to include workspace context
            
        Returns:
            Context dictionary
        """
        context = {
            "workspace": str(self.workspace),
            "files": [],
            "workspace_info": {}
        }
        
        # Add specific files
        if files:
            for file_path in files:
                try:
                    full_path = self.workspace / file_path
                    if full_path.exists() and full_path.is_file():
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        context["files"].append({
                            "path": file_path,
                            "content": content,
                            "size": len(content)
                        })
                        if self.verbose:
                            print(f"Added file to context: {file_path}")
                    else:
                        print(f"Warning: File not found: {file_path}")
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")
        
        # Add workspace context if requested
        if include_workspace_context:
            try:
                workspace_info = self.context_manager.get_workspace_context()
                context["workspace_info"] = workspace_info
                if self.verbose:
                    print("Added workspace context")
            except Exception as e:
                print(f"Warning: Could not gather workspace context: {e}")
        
        return context
    
    def _display_response(self, response: Dict[str, Any]):
        """Display the chat response.
        
        Args:
            response: Response from chat interface
        """
        if "error" in response:
            print(f"Error: {response['error']}")
            return
        
        if "content" in response:
            print("\n" + "="*60)
            print("Copilot Response:")
            print("="*60)
            print(response["content"])
            print("="*60 + "\n")
        
        if "references" in response and response["references"]:
            print("References:")
            for ref in response["references"]:
                print(f"  - {ref}")
            print()
    
    def _test_configuration(self) -> bool:
        """Test the current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Simple test message
            test_response = self.chat_interface.send_message(
                message="Hello, this is a test message.",
                context={},
                agent=None
            )
            return "error" not in test_response
        except Exception as e:
            if self.verbose:
                print(f"Configuration test failed: {e}")
            return False