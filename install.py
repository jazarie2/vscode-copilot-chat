#!/usr/bin/env python3
"""
Installation script for CLI Pilot dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout.strip():
            print(f"  Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Command: {command}")
        print(f"  Exit code: {e.returncode}")
        if e.stdout.strip():
            print(f"  Output: {e.stdout.strip()}")
        if e.stderr.strip():
            print(f"  Error: {e.stderr.strip()}")
        return False


def create_launch_script():
    """Create a launch script that activates the virtual environment."""
    launch_script = """#!/bin/bash
# CLI Pilot launcher script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate virtual environment and run main.py
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/main.py" "$@"
"""
    
    with open("clipilot", "w") as f:
        f.write(launch_script)
    
    # Make it executable
    os.chmod("clipilot", 0o755)
    print("✓ Created 'clipilot' launcher script")


def main():
    """Main installation function."""
    print("CLI Pilot - Installation Script")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: Please run this script from the CLI Pilot root directory")
        return 1
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return 1
    
    print(f"Using Python {sys.version.split()[0]}")
    
    # Create virtual environment
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists")
    else:
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            print("\nFailed to create virtual environment.")
            print("Make sure you have python3-venv installed:")
            print("  sudo apt install python3-venv")
            return 1
    
    # Install requirements in virtual environment
    pip_command = "./venv/bin/pip install -r requirements.txt"
    if not run_command(pip_command, "Installing requirements in virtual environment"):
        print("\nInstallation failed. Please check the error messages above.")
        return 1
    
    # Create launcher script
    create_launch_script()
    
    print("\n" + "="*50)
    print("✓ Installation completed successfully!")
    print("\nNext steps:")
    print("1. Authenticate with GitHub:")
    print("   ./clipilot auth login")
    print("\n2. Or manually set up with a token:")
    print("   ./clipilot setup --token YOUR_TOKEN")
    print("\n3. Start chatting:")
    print("   ./clipilot chat 'Hello, Copilot!'")
    print("   ./clipilot interactive")
    print("\nAlternatively, you can activate the virtual environment manually:")
    print("   source venv/bin/activate")
    print("   python main.py auth login")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())