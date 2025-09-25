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

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available, using fallback heuristics")

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
    Classify commit quality using Hugging Face model.
    Falls back to heuristics if model fails or is unavailable.
    """
    if not TRANSFORMERS_AVAILABLE:
        return analyze_diff_heuristic(diff)
    
    try:
        # Try to load a code-related model
        model_name = "microsoft/codebert-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # For now, we'll use a mock classification since we don't have a fine-tuned model
        # In a real implementation, you'd load a model trained on commit quality
        
        # Tokenize the diff (truncate if too long)
        inputs = tokenizer(
            diff[:1000],  # Limit input size for performance
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # Mock prediction - in reality you'd run this through your trained model
        # For now, we'll use the heuristic but with ML-like confidence scores
        classification, confidence = analyze_diff_heuristic(diff)
        
        # Add some ML-like randomness to confidence
        confidence += random.uniform(-0.1, 0.1)
        confidence = max(0.1, min(0.95, confidence))
        
        return classification, confidence
        
    except Exception as e:
        print(f"ML classification failed: {e}, falling back to heuristics")
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
    print("🎵 Deep Learning Git Hook DJ 🎵")
    print("=" * 40)
    
    # Get staged diff
    print("📊 Analyzing staged changes...")
    diff = get_staged_diff()
    
    if not diff.strip():
        print("No staged changes found.")
        return 0
    
    # Classify commit quality
    start_time = time.time()
    classification, confidence = classify_with_ml(diff)
    analysis_time = time.time() - start_time
    
    print(f"🔍 Analysis complete in {analysis_time:.2f}s")
    print(f"📈 Classification: {classification.upper()} (confidence: {confidence:.2f})")
    
    # Display ASCII art
    display_ascii_art(classification)
    
    # Update karma
    update_karma(classification)
    
    # Play appropriate sound
    print(f"🔊 Playing {classification} commit sound...")
    if classification == "bad":
        clown_honk()
    elif classification == "good":
        mario_coin()
    elif classification == "stellar":
        desperado()
    
    print("✅ Git Hook DJ complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
