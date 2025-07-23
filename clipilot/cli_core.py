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
        """Setup CLI Pilot configuration.
        
        Args:
            token: GitHub Copilot token
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            print("Setting up CLI Pilot...")
            
            if not token:
                token = input("Enter your GitHub Copilot token: ").strip()
            
            if not token:
                print("Error: Token is required")
                return 1
            
            self.config.set_token(token)
            print("Configuration saved successfully!")
            
            # Test the configuration
            if self._test_configuration():
                print("✓ Configuration test passed!")
                return 0
            else:
                print("✗ Configuration test failed. Please check your token.")
                return 1
                
        except Exception as e:
            print(f"Error during setup: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
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