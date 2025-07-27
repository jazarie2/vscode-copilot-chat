#!/usr/bin/env python3
"""
Setup script to transition from CLI Pilot to VSCodey CLI
"""

import shutil
import sys
from pathlib import Path


def cleanup_clipilot():
    """Remove the clipilot module and related files."""
    print("Cleaning up CLI Pilot files...")

    # Remove clipilot directory
    clipilot_dir = Path("clipilot")
    if clipilot_dir.exists():
        shutil.rmtree(clipilot_dir)
        print("✓ Removed clipilot/ directory")

    # Remove Python-specific files that are no longer needed
    files_to_remove = [
        "main.py",
        "requirements.txt",
        "install.py",
        "CLI_PILOT_README.md",
        "CLIPILOT_SETUP.md",
    ]

    for file in files_to_remove:
        file_path = Path(file)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Removed {file}")

    print("\n✓ CLI Pilot cleanup completed!")


def setup_vscodey():
    """Set up VSCodey CLI."""
    print("\nSetting up VSCodey CLI...")

    # Check if vscodey-cli.py exists
    vscodey_file = Path("vscodey-cli.py")
    if not vscodey_file.exists():
        print("✗ Error: vscodey-cli.py not found!")
        return False

    # Make it executable on Unix systems
    try:
        import stat

        current_mode = vscodey_file.stat().st_mode
        vscodey_file.chmod(current_mode | stat.S_IEXEC)
        print("✓ Made vscodey-cli.py executable")
    except Exception:
        pass  # Not critical on Windows

    print("✓ VSCodey CLI setup completed!")
    return True


def test_vscodey():
    """Test VSCodey CLI installation."""
    print("\nTesting VSCodey CLI...")

    import subprocess

    try:
        result = subprocess.run(
            [sys.executable, "vscodey-cli.py", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✓ VSCodey CLI is working correctly")
            print(f"  Version: {result.stdout.strip()}")
            return True
        else:
            print("✗ VSCodey CLI test failed")
            print(f"  Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error testing VSCodey CLI: {e}")
        return False


def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Transition to VSCodey CLI Complete!")
    print("=" * 60)

    print("\nWhat's New:")
    print("• Simple, focused CLI that opens VS Code with Copilot Chat")
    print("• Leverages native VS Code Copilot features (@workspace, @vscode, etc.)")
    print("• No complex configuration or multiple AI models to manage")
    print("• Always up-to-date with latest VS Code Copilot features")

    print("\nQuick Start:")
    print('  python vscodey-cli.py chat "How do I create a Python function?"')
    print('  python vscodey-cli.py chat "Explain this code" --file main.py')
    print("  python vscodey-cli.py interactive")
    print("  python vscodey-cli.py help")

    print("\nPrerequisites:")
    print("1. VS Code with 'code' command in PATH")
    print("2. GitHub Copilot Chat extension installed")
    print("3. Active GitHub Copilot subscription")

    print("\nDocumentation:")
    print("  See VSCODEY_README.md for detailed usage information")

    print("\nTo verify your setup:")
    print("  python vscodey-cli.py help")


def main():
    """Main setup function."""
    print("VSCodey CLI Setup")
    print("=" * 50)
    print("This will transition from CLI Pilot to VSCodey CLI")
    print("- Remove CLI Pilot files (clipilot/, main.py, etc.)")
    print("- Set up simple VSCodey CLI")
    print("- Test the new setup")

    response = input("\nContinue? (y/N): ").strip().lower()
    if response not in ["y", "yes"]:
        print("Setup cancelled.")
        return 1

    try:
        # Clean up old CLI Pilot
        cleanup_clipilot()

        # Set up VSCodey CLI
        if not setup_vscodey():
            return 1

        # Test the setup
        if not test_vscodey():
            print("\n⚠️  VSCodey CLI setup completed but testing failed.")
            print("   You may need to install VS Code or the Copilot Chat extension.")

        # Show next steps
        show_next_steps()

        return 0

    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
