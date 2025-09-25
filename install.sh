#!/bin/bash
#
# Deep Learning Git Hook DJ - Installation Script
# This script sets up the Git Hook DJ in your repository
#

set -e  # Exit on any error

echo "🎵 Deep Learning Git Hook DJ - Installation"
echo "============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository!"
    echo "Please run this script from the root of your git repository."
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x git_dj.py beep_player.py pre-commit

# Copy the pre-commit hook
echo "📋 Installing pre-commit hook..."
cp pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Install Python dependencies (optional)
echo "📦 Installing Python dependencies (optional)..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt 2>/dev/null || echo "⚠️  Warning: Could not install ML dependencies. The system will use fallback heuristics."
else
    echo "⚠️  Warning: pip3 not found. The system will use fallback heuristics."
fi

# Test the installation
echo "🧪 Testing installation..."
if python3 git_dj.py > /dev/null 2>&1; then
    echo "✅ Installation successful!"
    echo ""
    echo "🎉 Git Hook DJ is now installed!"
    echo ""
    echo "Next steps:"
    echo "1. Stage some changes: git add ."
    echo "2. Make a commit: git commit -m 'Your message'"
    echo "3. Enjoy the musical feedback! 🎵"
    echo ""
    echo "To test the sounds manually:"
    echo "  python3 beep_player.py"
    echo ""
    echo "To test the full system:"
    echo "  python3 git_dj.py"
else
    echo "❌ Installation test failed!"
    echo "Please check the error messages above and try again."
    exit 1
fi
