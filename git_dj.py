#!/usr/bin/env python3
"""
Deep Learning Git Hook DJ
Analyzes staged git diffs and plays appropriate audio feedback based on commit quality.
"""

import subprocess
import sys
import time
import json
import os
from typing import Tuple, Optional
import random

# Suppress tokenizers parallelism warnings
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

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
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'

def color_print(text: str, color: str = Colors.WHITE, bold: bool = False) -> None:
    """Print colored text to terminal."""
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.END}")
    else:
        print(f"{color}{text}{Colors.END}")

def print_header() -> None:
    """Print the colorful header."""
    color_print("🎵 Deep Learning Git Hook DJ 🎵", Colors.CYAN, bold=True)
    color_print("=" * 40, Colors.CYAN)

# Import our ML predictor and config
try:
    from ml_predictor import CodeQualityPredictor
    from ml_config import MLConfig
    ML_PREDICTOR_AVAILABLE = True
except ImportError:
    ML_PREDICTOR_AVAILABLE = False
    print("Warning: ML predictor not available, using fallback heuristics")

# Fallback imports
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from beep_player import clown_honk, mario_coin, desperado


def get_staged_diff() -> str:
    """Extract staged diff from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            print(f"Git diff failed: {result.stderr}")
            return ""
        return result.stdout
    except subprocess.TimeoutExpired:
        print("Git diff timed out")
        return ""
    except Exception as e:
        print(f"Error getting staged diff: {e}")
        return ""


def analyze_diff_heuristic(diff: str) -> Tuple[str, float]:
    """
    Fallback heuristic analysis when ML model is not available.
    Returns (classification, confidence)
    """
    if not diff.strip():
        return "bad", 0.8
    
    lines = diff.split('\n')
    diff_lines = [line for line in lines if line.startswith(('+', '-')) and not line.startswith('+++') and not line.startswith('---')]
    
    # Count actual changes (excluding context lines)
    actual_changes = len(diff_lines)
    
    # Heuristic rules
    if actual_changes < 10:
        return "bad", 0.7
    
    # Check for test modifications or new functions
    has_tests = any('test' in line.lower() for line in diff_lines)
    has_functions = any(line.strip().startswith('+def ') or line.strip().startswith('+function ') for line in diff_lines)
    
    if has_tests or has_functions:
        return "stellar", 0.8
    
    return "good", 0.6


def classify_with_ml(diff: str) -> Tuple[str, float]:
    """
    Classify commit quality using our ML predictor.
    Falls back to heuristics if model fails or is unavailable.
    """
    if ML_PREDICTOR_AVAILABLE:
        try:
            # Load configuration
            config = MLConfig()
            use_transformer = config.get_effective_model_choice()
            
            # Initialize predictor with model selection
            predictor = CodeQualityPredictor(use_transformer=use_transformer)
            return predictor.predict(diff)
        except Exception as e:
            color_print(f"ML prediction failed: {e}, falling back to heuristics", Colors.YELLOW)
            return analyze_diff_heuristic(diff)
    else:
        return analyze_diff_heuristic(diff)


def update_karma(classification: str) -> None:
    """Update karma score in .git/karma.json"""
    karma_file = ".git/karma.json"
    
    # Load existing karma
    karma = {"bad": 0, "good": 0, "stellar": 0, "total": 0}
    if os.path.exists(karma_file):
        try:
            with open(karma_file, 'r') as f:
                karma = json.load(f)
        except:
            pass
    
    # Update karma
    karma[classification] += 1
    karma["total"] += 1
    
    # Save karma
    try:
        with open(karma_file, 'w') as f:
            json.dump(karma, f, indent=2)
    except Exception as e:
        print(f"Could not save karma: {e}")


def display_ascii_art(classification: str) -> None:
    """Display ASCII art based on classification"""
    if classification == "bad":
        print("""
    🤡 CLOWN HONK 🤡
    ╭─────────────────╮
    │   BAD COMMIT    │
    │   (._.)         │
    │  <)   )>        │
    │   /   \\         │
    ╰─────────────────╯
        """)
    elif classification == "good":
        print("""
    🪙 MARIO COIN 🪙
    ╭─────────────────╮
    │   GOOD COMMIT   │
    │      💰         │
    │    ╭─────╮      │
    │   ╱       ╲     │
    │  ╱  ★★★  ╲    │
    │ ╱           ╲   │
    │╱_____________╲  │
    ╰─────────────────╯
        """)
    elif classification == "stellar":
        print("""
    🤠 DESPERADO 🤠
    ╭─────────────────╮
    │  STELLAR COMMIT │
    │    ╭─────╮      │
    │   ╱  🤠  ╲     │
    │  ╱   ╭─╮  ╲    │
    │ ╱   ╱   ╲  ╲   │
    │╱___╱     ╲__╲  │
    ╰─────────────────╯
        """)


def main():
    """Main function to analyze commit and play appropriate sound."""
    print_header()
    
    # Get staged diff
    color_print("📊 Analyzing staged changes...", Colors.BLUE)
    diff = get_staged_diff()
    
    if not diff.strip():
        color_print("No staged changes found.", Colors.YELLOW)
        return 0
    
    # Classify commit quality
    start_time = time.time()
    classification, confidence = classify_with_ml(diff)
    analysis_time = time.time() - start_time
    
    color_print(f"🔍 Analysis complete in {analysis_time:.2f}s", Colors.GREEN)
    
    # Color-code the classification
    if classification == "bad":
        color_print(f"📈 Classification: {classification.upper()} (confidence: {confidence:.2f})", Colors.RED, bold=True)
    elif classification == "good":
        color_print(f"📈 Classification: {classification.upper()} (confidence: {confidence:.2f})", Colors.YELLOW, bold=True)
    elif classification == "stellar":
        color_print(f"📈 Classification: {classification.upper()} (confidence: {confidence:.2f})", Colors.GREEN, bold=True)
    
    # Display ASCII art
    display_ascii_art(classification)
    
    # Update karma
    update_karma(classification)
    
    # Play appropriate sound
    color_print(f"🔊 Playing {classification} commit sound...", Colors.MAGENTA)
    if classification == "bad":
        clown_honk()
    elif classification == "good":
        mario_coin()
    elif classification == "stellar":
        desperado()
    
    color_print("✅ Git Hook DJ complete!", Colors.GREEN, bold=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
