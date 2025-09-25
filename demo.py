#!/usr/bin/env python3
"""
Deep Learning Git Hook DJ - Demo Script
This script demonstrates all the features of the Git Hook DJ
"""

import subprocess
import os
import time
from beep_player import clown_honk, mario_coin, desperado


def run_command(cmd, description):
    """Run a command and display the result."""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    print("-" * 50)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def create_test_files():
    """Create test files for demonstration."""
    print("📝 Creating test files for demonstration...")
    
    # Bad commit - small change
    with open("bad_commit.txt", "w") as f:
        f.write("// TODO: fix this\n")
    
    # Good commit - medium change
    with open("good_commit.py", "w") as f:
        f.write("""# Configuration updates
CONFIG = {
    'api_key': 'new-key',
    'timeout': 30,
    'retry_attempts': 3,
    'cache_ttl': 3600,
    'rate_limit': 1000,
    'debug_mode': True,
    'log_level': 'INFO'
}

# Environment setup
import os
os.environ['API_KEY'] = CONFIG['api_key']
os.environ['DEBUG'] = str(CONFIG['debug_mode'])
""")
    
    # Stellar commit - new function
    with open("stellar_commit.py", "w") as f:
        f.write("""def new_awesome_feature():
    \"\"\"This is a new function that should trigger stellar classification.\"\"\"
    print("Awesome feature activated!")
    return "success"

def another_function():
    \"\"\"Another function for good measure.\"\"\"
    return True

# Main execution
if __name__ == "__main__":
    result = new_awesome_feature()
    print(f"Result: {result}")
""")


def demo_commit_types():
    """Demonstrate different commit types."""
    print("\n🎵 DEMONSTRATING DIFFERENT COMMIT TYPES")
    print("=" * 50)
    
    # Bad commit
    print("\n1️⃣  BAD COMMIT (small change)")
    run_command("git add bad_commit.txt", "Staging bad commit file")
    run_command("python3 git_dj.py", "Analyzing bad commit")
    
    time.sleep(2)
    
    # Good commit  
    print("\n2️⃣  GOOD COMMIT (medium change)")
    run_command("git add good_commit.py", "Staging good commit file")
    run_command("python3 git_dj.py", "Analyzing good commit")
    
    time.sleep(2)
    
    # Stellar commit
    print("\n3️⃣  STELLAR COMMIT (new functions)")
    run_command("git add stellar_commit.py", "Staging stellar commit file")
    run_command("python3 git_dj.py", "Analyzing stellar commit")


def demo_sounds():
    """Demonstrate all the sounds."""
    print("\n🔊 DEMONSTRATING ALL SOUNDS")
    print("=" * 30)
    
    print("\n🤡 Clown Honk (Bad Commit):")
    clown_honk()
    
    time.sleep(1)
    
    print("\n🪙 Mario Coin (Good Commit):")
    mario_coin()
    
    time.sleep(1)
    
    print("\n🤠 Desperado (Stellar Commit):")
    desperado()


def show_karma():
    """Show the karma tracking."""
    print("\n📊 KARMA TRACKING")
    print("=" * 20)
    
    karma_file = ".git/karma.json"
    if os.path.exists(karma_file):
        with open(karma_file, 'r') as f:
            import json
            karma = json.load(f)
        
        print(f"Bad commits: {karma.get('bad', 0)}")
        print(f"Good commits: {karma.get('good', 0)}")
        print(f"Stellar commits: {karma.get('stellar', 0)}")
        print(f"Total commits: {karma.get('total', 0)}")
        
        if karma.get('total', 0) > 0:
            bad_pct = (karma.get('bad', 0) / karma.get('total', 1)) * 100
            good_pct = (karma.get('good', 0) / karma.get('total', 1)) * 100
            stellar_pct = (karma.get('stellar', 0) / karma.get('total', 1)) * 100
            
            print(f"\nCommit Quality Distribution:")
            print(f"  Bad: {bad_pct:.1f}%")
            print(f"  Good: {good_pct:.1f}%")
            print(f"  Stellar: {stellar_pct:.1f}%")
    else:
        print("No karma data found yet.")


def main():
    """Main demo function."""
    print("🎵 Deep Learning Git Hook DJ - DEMO")
    print("=" * 40)
    
    # Check if we're in a git repo
    if not os.path.exists(".git"):
        print("❌ Not in a git repository!")
        print("Please run this demo from a git repository.")
        return
    
    # Create test files
    create_test_files()
    
    # Demo sounds
    demo_sounds()
    
    # Demo commit analysis
    demo_commit_types()
    
    # Show karma
    show_karma()
    
    # Cleanup
    print("\n🧹 Cleaning up demo files...")
    for file in ["bad_commit.txt", "good_commit.py", "stellar_commit.py"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✅ Demo complete!")
    print("\nTo use the Git Hook DJ:")
    print("1. Stage changes: git add .")
    print("2. Commit: git commit -m 'Your message'")
    print("3. Enjoy the musical feedback! 🎵")


if __name__ == "__main__":
    main()
