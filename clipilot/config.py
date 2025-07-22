"""
Configuration management for CLI Pilot.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class CLIConfig:
    """Manages configuration for CLI Pilot."""
    
    DEFAULT_CONFIG_DIR = Path.home() / ".clipilot"
    DEFAULT_CONFIG_FILE = "config.json"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Custom path to configuration file
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self.DEFAULT_CONFIG_DIR / self.DEFAULT_CONFIG_FILE
        
        self.config_dir = self.config_path.parent
        self._config_data = {}
        
        self._ensure_config_dir()
        self._load_config()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                self._config_data = {}
        else:
            self._config_data = self._get_default_config()
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2)
        except IOError as e:
            raise Exception(f"Could not save config to {self.config_path}: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "1.0.0",
            "auth": {
                "token": None,
                "token_type": "github_copilot"
            },
            "chat": {
                "default_agent": "workspace",
                "max_context_size": 4096,
                "temperature": 0.1
            },
            "workspace": {
                "include_patterns": ["*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.h"],
                "exclude_patterns": ["node_modules/**", ".git/**", "__pycache__/**", "*.pyc"],
                "max_file_size": 1024 * 1024  # 1MB
            },
            "ui": {
                "color_output": True,
                "show_typing_indicator": True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'auth.token')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        self._save_config()
    
    def get_token(self) -> Optional[str]:
        """Get authentication token.
        
        Returns:
            Authentication token or None
        """
        # Try environment variable first
        token = os.getenv('GITHUB_COPILOT_TOKEN')
        if token:
            return token
        
        # Try configuration file
        return self.get('auth.token')
    
    def set_token(self, token: str):
        """Set authentication token.
        
        Args:
            token: Authentication token
        """
        self.set('auth.token', token)
    
    def get_chat_config(self) -> Dict[str, Any]:
        """Get chat configuration.
        
        Returns:
            Chat configuration dictionary
        """
        return self.get('chat', {})
    
    def get_workspace_config(self) -> Dict[str, Any]:
        """Get workspace configuration.
        
        Returns:
            Workspace configuration dictionary
        """
        return self.get('workspace', {})
    
    def is_configured(self) -> bool:
        """Check if CLI Pilot is properly configured.
        
        Returns:
            True if configured, False otherwise
        """
        return self.get_token() is not None
    
    def reset(self):
        """Reset configuration to defaults."""
        self._config_data = self._get_default_config()
        self._save_config()
    
    def export_config(self, path: str):
        """Export configuration to a file.
        
        Args:
            path: Path to export file
        """
        export_path = Path(path)
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(self._config_data, f, indent=2)
    
    def import_config(self, path: str):
        """Import configuration from a file.
        
        Args:
            path: Path to import file
        """
        import_path = Path(path)
        if not import_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(import_path, 'r', encoding='utf-8') as f:
            imported_config = json.load(f)
        
        self._config_data.update(imported_config)
        self._save_config()