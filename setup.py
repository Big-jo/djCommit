#!/usr/bin/env python3
"""
Super simple setup script for Deep Learning Git Hook DJ
Just run: python3 setup.py
"""

import subprocess
import sys
import os

def main():
    print("🎵 Deep Learning Git Hook DJ - Quick Setup")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("dj_cli.py"):
        print("❌ Error: dj_cli.py not found!")
        print("Please run this script from the dj_commit directory.")
        sys.exit(1)
    
    # Run the CLI install command
    try:
        subprocess.run([sys.executable, "dj_cli.py", "install"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Installation failed!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Installation cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
