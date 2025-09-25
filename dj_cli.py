#!/usr/bin/env python3
"""
Deep Learning Git Hook DJ - Command Line Interface
Easy setup and management for the Git Hook DJ system.
"""

import argparse
import subprocess
import sys
import os
import json
from pathlib import Path

# Color codes for beautiful terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def color_print(text: str, color: str = Colors.WHITE, bold: bool = False) -> None:
    """Print colored text to terminal."""
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.END}")
    else:
        print(f"{color}{text}{Colors.END}")

def print_banner():
    """Print the DJ CLI banner."""
    color_print("🎵 Deep Learning Git Hook DJ CLI 🎵", Colors.CYAN, bold=True)
    color_print("=" * 50, Colors.CYAN)
    print()

def check_git_repo():
    """Check if we're in a git repository."""
    try:
        subprocess.run(["git", "status"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        missing.append("Python 3.7+")
    
    # Check if gcc is available
    try:
        subprocess.run(["gcc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("gcc (for compiling audio program)")
    
    return missing

def install_dependencies():
    """Install Python dependencies."""
    color_print("📦 Installing Python dependencies...", Colors.BLUE)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        color_print("✅ Dependencies installed successfully!", Colors.GREEN)
        return True
    except subprocess.CalledProcessError:
        color_print("❌ Failed to install dependencies", Colors.RED)
        return False

def compile_audio_program():
    """Compile the C audio program."""
    color_print("🔨 Compiling audio program...", Colors.BLUE)
    
    if not os.path.exists("beep.c"):
        color_print("❌ beep.c not found", Colors.RED)
        return False
    
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["gcc", "-o", "beep", "beep.c", "-framework", "AudioToolbox"], check=True)
        else:  # Linux/other
            subprocess.run(["gcc", "-o", "beep", "beep.c"], check=True)
        
        os.chmod("beep", 0o755)
        color_print("✅ Audio program compiled successfully!", Colors.GREEN)
        return True
    except subprocess.CalledProcessError:
        color_print("❌ Failed to compile audio program", Colors.RED)
        return False

def install_git_hook():
    """Install the git pre-commit hook."""
    color_print("📋 Installing git pre-commit hook...", Colors.BLUE)
    
    if not os.path.exists(".git/hooks"):
        color_print("❌ Not in a git repository", Colors.RED)
        return False
    
    try:
        # Copy the pre-commit hook
        subprocess.run(["cp", "pre-commit", ".git/hooks/pre-commit"], check=True)
        subprocess.run(["chmod", "+x", ".git/hooks/pre-commit"], check=True)
        color_print("✅ Git hook installed successfully!", Colors.GREEN)
        return True
    except subprocess.CalledProcessError:
        color_print("❌ Failed to install git hook", Colors.RED)
        return False

def test_system():
    """Test the complete system."""
    color_print("🧪 Testing the system...", Colors.BLUE)
    
    try:
        # Test the beep player
        result = subprocess.run([sys.executable, "beep_player.py"], capture_output=True, text=True)
        if result.returncode == 0:
            color_print("✅ Audio system working!", Colors.GREEN)
        else:
            color_print("⚠️  Audio system has issues (fallback will be used)", Colors.YELLOW)
        
        # Test the main script
        result = subprocess.run([sys.executable, "git_dj.py"], capture_output=True, text=True)
        if result.returncode == 0:
            color_print("✅ Main analysis system working!", Colors.GREEN)
        else:
            color_print("❌ Main analysis system failed", Colors.RED)
            return False
        
        return True
    except Exception as e:
        color_print(f"❌ Test failed: {e}", Colors.RED)
        return False

def show_status():
    """Show the current status of the system."""
    color_print("📊 System Status", Colors.CYAN, bold=True)
    color_print("-" * 20, Colors.CYAN)
    
    # Check git repository
    if check_git_repo():
        color_print("✅ Git repository: OK", Colors.GREEN)
    else:
        color_print("❌ Git repository: Not found", Colors.RED)
    
    # Check dependencies
    missing = check_dependencies()
    if not missing:
        color_print("✅ Dependencies: All installed", Colors.GREEN)
    else:
        color_print(f"⚠️  Missing dependencies: {', '.join(missing)}", Colors.YELLOW)
    
    # Check compiled program
    if os.path.exists("beep") and os.access("beep", os.X_OK):
        color_print("✅ Audio program: Compiled", Colors.GREEN)
    else:
        color_print("❌ Audio program: Not compiled", Colors.RED)
    
    # Check git hook
    if os.path.exists(".git/hooks/pre-commit"):
        color_print("✅ Git hook: Installed", Colors.GREEN)
    else:
        color_print("❌ Git hook: Not installed", Colors.RED)
    
    # Check karma file
    if os.path.exists(".git/karma.json"):
        try:
            with open(".git/karma.json", 'r') as f:
                karma = json.load(f)
            color_print(f"📈 Karma: {karma.get('total', 0)} commits tracked", Colors.BLUE)
        except:
            color_print("📈 Karma: File exists but corrupted", Colors.YELLOW)
    else:
        color_print("📈 Karma: No commits tracked yet", Colors.BLUE)

def demo_system():
    """Run the demo."""
    color_print("🎬 Running demo...", Colors.BLUE)
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
        color_print("✅ Demo completed!", Colors.GREEN)
    except subprocess.CalledProcessError:
        color_print("❌ Demo failed", Colors.RED)

def uninstall_system():
    """Uninstall the git hook."""
    color_print("🗑️  Uninstalling git hook...", Colors.BLUE)
    
    if os.path.exists(".git/hooks/pre-commit"):
        try:
            os.remove(".git/hooks/pre-commit")
            color_print("✅ Git hook removed successfully!", Colors.GREEN)
        except Exception as e:
            color_print(f"❌ Failed to remove git hook: {e}", Colors.RED)
    else:
        color_print("ℹ️  Git hook not found", Colors.BLUE)

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Deep Learning Git Hook DJ - Easy setup and management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dj_cli.py install     # Install everything
  dj_cli.py status      # Check system status
  dj_cli.py demo        # Run demo
  dj_cli.py uninstall   # Remove git hook
        """
    )
    
    parser.add_argument(
        "command",
        choices=["install", "status", "demo", "uninstall", "test"],
        help="Command to run"
    )
    
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip dependency installation"
    )
    
    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip audio program compilation"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.command == "install":
        color_print("🚀 Installing Deep Learning Git Hook DJ...", Colors.GREEN, bold=True)
        print()
        
        # Check if we're in a git repo
        if not check_git_repo():
            color_print("❌ Error: Not in a git repository!", Colors.RED)
            color_print("Please run this command from the root of your git repository.", Colors.YELLOW)
            sys.exit(1)
        
        # Check dependencies
        missing = check_dependencies()
        if missing and not args.skip_deps:
            color_print(f"⚠️  Missing dependencies: {', '.join(missing)}", Colors.YELLOW)
            color_print("Installing Python dependencies...", Colors.BLUE)
            if not install_dependencies():
                sys.exit(1)
        elif missing:
            color_print(f"⚠️  Missing dependencies (skipped): {', '.join(missing)}", Colors.YELLOW)
        
        # Compile audio program
        if not args.skip_audio:
            if not compile_audio_program():
                color_print("⚠️  Audio compilation failed, but system will still work with fallbacks", Colors.YELLOW)
        
        # Install git hook
        if not install_git_hook():
            sys.exit(1)
        
        # Test system
        if not test_system():
            color_print("⚠️  Some tests failed, but basic functionality should work", Colors.YELLOW)
        
        print()
        color_print("🎉 Installation complete!", Colors.GREEN, bold=True)
        color_print("Try making a commit to hear the magic! 🎵", Colors.CYAN)
        color_print("Run 'dj_cli.py demo' to test all sounds.", Colors.BLUE)
    
    elif args.command == "status":
        show_status()
    
    elif args.command == "demo":
        demo_system()
    
    elif args.command == "uninstall":
        uninstall_system()
    
    elif args.command == "test":
        if test_system():
            color_print("✅ All tests passed!", Colors.GREEN)
        else:
            color_print("❌ Some tests failed", Colors.RED)
            sys.exit(1)

if __name__ == "__main__":
    main()
