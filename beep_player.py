#!/usr/bin/env python3
"""
Beep Player Module for Git Hook DJ
Contains functions to play different beep sequences based on commit quality.
"""

import subprocess
import time
import sys
import os

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

# Try to import audio libraries for better sound
try:
    import winsound  # Windows
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Import our chiptune synthesizer
try:
    from chiptune_synth import ChiptuneSynthesizer, create_mario_theme, create_desperado_theme, create_clown_theme
    CHIPTUNE_AVAILABLE = True
except ImportError:
    CHIPTUNE_AVAILABLE = False


def play_beep() -> None:
    """Play a single beep using multiple methods."""
    beep_played = False
    
    # Method 1: C beep program (most reliable)
    beep_program = os.path.join(os.path.dirname(__file__), "beep")
    if os.path.exists(beep_program):
        try:
            subprocess.run([beep_program, "test"], check=False, timeout=2)
            beep_played = True
        except Exception:
            pass
    
    # Method 2: Windows winsound (most reliable on Windows)
    if not beep_played and WINSOUND_AVAILABLE and sys.platform == "win32":
        try:
            winsound.Beep(800, 200)  # 800Hz for 200ms
            beep_played = True
        except Exception:
            pass
    
    # Method 3: macOS say command (very audible)
    if not beep_played and sys.platform == "darwin":
        try:
            subprocess.run(["say", "-v", "Bells", "ding"], check=False, timeout=1)
            beep_played = True
        except Exception:
            pass
    
    # Method 4: Linux beep command (if available)
    if not beep_played and sys.platform.startswith("linux"):
        try:
            subprocess.run(["beep"], check=False, timeout=1)
            beep_played = True
        except Exception:
            pass
    
    # Method 5: System bell
    if not beep_played:
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["printf", "\\a"], check=False)
            elif sys.platform.startswith("linux"):  # Linux
                subprocess.run(["echo", "-e", "\\a"], check=False)
            else:  # Windows or other
                subprocess.run(["echo", "\a"], check=False, shell=True)
            beep_played = True
        except Exception:
            pass
    
    # Method 6: Visual indicator as fallback
    if not beep_played:
        print("🔔", end="", flush=True)
    else:
        print("🔊", end="", flush=True)


def clown_honk() -> None:
    """
    Play circus/clown theme for bad commits.
    """
    color_print("🤡 Playing circus theme...", Colors.RED, bold=True)
    
    # Try chiptune synthesizer first
    if CHIPTUNE_AVAILABLE and NUMPY_AVAILABLE:
        try:
            synth = ChiptuneSynthesizer()
            clown_audio = create_clown_theme(synth)
            synth.play_audio(clown_audio)
            color_print(" 🤡 Circus theme complete!", Colors.RED)
            return
        except Exception as e:
            color_print(f"Chiptune failed: {e}", Colors.YELLOW)
    
    # Try C beep program
    beep_program = os.path.join(os.path.dirname(__file__), "beep")
    if os.path.exists(beep_program):
        try:
            subprocess.run([beep_program, "clown"], check=False, timeout=3)
            color_print(" 🤡 Circus theme complete!", Colors.RED)
            return
        except Exception:
            pass
    
    # Fallback to Python implementation
    # First beep
    play_beep()
    time.sleep(0.1)
    
    # Second beep
    play_beep()
    time.sleep(0.1)
    
    color_print(" 🤡 Circus theme complete!", Colors.RED)


def mario_coin() -> None:
    """
    Play Super Mario Bros. main theme for good commits.
    """
    color_print("🪙 Playing Mario theme...", Colors.YELLOW, bold=True)
    
    # Try chiptune synthesizer first
    if CHIPTUNE_AVAILABLE and NUMPY_AVAILABLE:
        try:
            synth = ChiptuneSynthesizer()
            mario_audio = create_mario_theme(synth)
            synth.play_audio(mario_audio)
            color_print(" 🪙 Mario theme complete!", Colors.YELLOW)
            return
        except Exception as e:
            color_print(f"Chiptune failed: {e}", Colors.YELLOW)
    
    # Try C beep program
    beep_program = os.path.join(os.path.dirname(__file__), "beep")
    if os.path.exists(beep_program):
        try:
            subprocess.run([beep_program, "mario"], check=False, timeout=3)
            color_print(" 🪙 Mario theme complete!", Colors.YELLOW)
            return
        except Exception:
            pass
    
    # Fallback to Python implementation
    for i in range(3):
        play_beep()
        if i < 2:  # Don't sleep after the last beep
            time.sleep(0.2)
    
    color_print(" 🪙 Mario theme complete!", Colors.YELLOW)


def desperado() -> None:
    """
    Play Eagles 'Desperado' opening melody for stellar commits.
    """
    color_print("🤠 Playing Desperado theme...", Colors.GREEN, bold=True)
    
    # Try chiptune synthesizer first
    if CHIPTUNE_AVAILABLE and NUMPY_AVAILABLE:
        try:
            synth = ChiptuneSynthesizer()
            desperado_audio = create_desperado_theme(synth)
            synth.play_audio(desperado_audio)
            color_print(" 🤠 Desperado complete!", Colors.GREEN)
            return
        except Exception as e:
            color_print(f"Chiptune failed: {e}", Colors.YELLOW)
    
    # Try C beep program
    beep_program = os.path.join(os.path.dirname(__file__), "beep")
    if os.path.exists(beep_program):
        try:
            subprocess.run([beep_program, "desperado"], check=False, timeout=5)
            color_print(" 🤠 Desperado complete!", Colors.GREEN)
            return
        except Exception:
            pass
    
    # Fallback to Python implementation
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
    
    color_print(" 🤠 Desperado complete!", Colors.GREEN)


def test_all_sounds() -> None:
    """Test function to play all sounds in sequence."""
    color_print("🎵 Testing all Git Hook DJ sounds...", Colors.CYAN, bold=True)
    color_print("=" * 50, Colors.CYAN)
    
    color_print("\n1. Testing clown honk (bad commit):", Colors.BLUE, bold=True)
    clown_honk()
    
    time.sleep(1)
    color_print("\n2. Testing Mario coin (good commit):", Colors.BLUE, bold=True)
    mario_coin()
    
    time.sleep(1)
    color_print("\n3. Testing Desperado (stellar commit):", Colors.BLUE, bold=True)
    desperado()
    
    color_print("\n🎵 All sounds tested!", Colors.GREEN, bold=True)


if __name__ == "__main__":
    # If run directly, test all sounds
    test_all_sounds()
