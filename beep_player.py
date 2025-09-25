#!/usr/bin/env python3
"""
Beep Player Module for Git Hook DJ
Contains functions to play different beep sequences based on commit quality.
"""

import subprocess
import time
import sys
import os


def play_beep() -> None:
    """Play a single beep using system bell."""
    try:
        # Try different methods to play beep
        if sys.platform == "darwin":  # macOS
            subprocess.run(["printf", "\\a"], check=False)
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["echo", "-e", "\\a"], check=False)
        else:  # Windows or other
            subprocess.run(["echo", "\a"], check=False, shell=True)
    except Exception:
        # Fallback: just print a visual indicator
        print("🔔 BEEP!", end="", flush=True)


def clown_honk() -> None:
    """
    Play clown honk sound for bad commits.
    Two quick beeps with short delay.
    """
    print("🤡 Playing clown honk...")
    
    # First beep
    play_beep()
    time.sleep(0.1)
    
    # Second beep
    play_beep()
    time.sleep(0.1)
    
    print(" 🤡 Honk complete!")


def mario_coin() -> None:
    """
    Play Mario coin sound for good commits.
    Three evenly spaced beeps.
    """
    print("🪙 Playing Mario coin sound...")
    
    for i in range(3):
        play_beep()
        if i < 2:  # Don't sleep after the last beep
            time.sleep(0.2)
    
    print(" 🪙 Coin collected!")


def desperado() -> None:
    """
    Play Desperado theme approximation for stellar commits.
    Custom sequence with varied timing.
    """
    print("🤠 Playing Desperado theme...")
    
    # Desperado-inspired beep pattern
    # This approximates the rhythm of the classic song
    beep_pattern = [
        (0.0, 1),    # Immediate beep
        (0.3, 1),    # Short pause, beep
        (0.2, 1),    # Quick beep
        (0.4, 1),    # Longer pause, beep
        (0.1, 1),    # Quick beep
        (0.2, 1),    # Medium pause, beep
        (0.5, 1),    # Long pause, final beep
    ]
    
    for delay, beep_count in beep_pattern:
        time.sleep(delay)
        for _ in range(beep_count):
            play_beep()
            if beep_count > 1:
                time.sleep(0.05)  # Very short gap between multiple beeps
    
    print(" 🤠 Desperado complete!")


def test_all_sounds() -> None:
    """Test function to play all sounds in sequence."""
    print("🎵 Testing all Git Hook DJ sounds...")
    print("=" * 50)
    
    print("\n1. Testing clown honk (bad commit):")
    clown_honk()
    
    time.sleep(1)
    print("\n2. Testing Mario coin (good commit):")
    mario_coin()
    
    time.sleep(1)
    print("\n3. Testing Desperado (stellar commit):")
    desperado()
    
    print("\n🎵 All sounds tested!")


if __name__ == "__main__":
    # If run directly, test all sounds
    test_all_sounds()
