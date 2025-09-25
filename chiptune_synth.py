#!/usr/bin/env python3
"""
Chiptune Synthesizer for Git Hook DJ
Implements NES-style sound chip emulation with square waves, triangle waves, and noise.

Research Foundation:
- "Endless Loop: A Brief History of Chiptunes" by Kevin Driscoll and Joshua Diaz
  (Transformative Works and Cultures, 2009)
- "Chiptune: The Ludomusical Shaping of Identity" 
  (ResearchGate, 2018)
- "Signal Processing for Sound Synthesis: Computer-Generated Sounds and Music for All"
  (ResearchGate, 2006)
- "Automatic Sound Synthesizer Programming: Techniques and Applications"
  (ResearchGate, 2016)

Technical Implementation:
- NES 2A03 APU (Audio Processing Unit) emulation
- Square wave synthesis with configurable duty cycles
- Triangle wave generation for bass and melody
- White noise generation for percussion effects
- ADSR envelope implementation for realistic sound shaping
- Multi-channel mixing with proper normalization

References:
- NES Technical Documentation: https://wiki.nesdev.com/w/index.php/APU
- Chiptune Synthesis Papers: https://www.semanticscholar.org/topic/Chiptune/1707298
"""

import numpy as np
import wave
import struct
import os
import tempfile
import subprocess
import sys
from typing import List, Tuple, Optional


class ChiptuneSynthesizer:
    """NES-style chiptune synthesizer with multiple channels."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.channels = {
            'square1': {'frequency': 0, 'volume': 0, 'duty_cycle': 0.5, 'envelope': 0},
            'square2': {'frequency': 0, 'volume': 0, 'duty_cycle': 0.5, 'envelope': 0},
            'triangle': {'frequency': 0, 'volume': 0, 'phase': 0},
            'noise': {'volume': 0, 'period': 0, 'seed': 1}
        }
    
    def generate_square_wave(self, frequency: float, duration: float, 
                           volume: float = 0.5, duty_cycle: float = 0.5) -> np.ndarray:
        """Generate a square wave with specified duty cycle."""
        if frequency <= 0:
            return np.zeros(int(self.sample_rate * duration))
        
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Generate square wave
        wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
        
        # Apply duty cycle
        period = 1.0 / frequency
        duty_samples = int(period * self.sample_rate * duty_cycle)
        for i in range(samples):
            phase = (i % int(period * self.sample_rate)) / (period * self.sample_rate)
            if phase > duty_cycle:
                wave_data[i] = -1
        
        return wave_data * volume
    
    def generate_triangle_wave(self, frequency: float, duration: float, 
                             volume: float = 0.5) -> np.ndarray:
        """Generate a triangle wave."""
        if frequency <= 0:
            return np.zeros(int(self.sample_rate * duration))
        
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Generate triangle wave using sawtooth
        triangle = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        
        return triangle * volume
    
    def generate_noise(self, duration: float, volume: float = 0.5, 
                      period: int = 1) -> np.ndarray:
        """Generate white noise."""
        samples = int(self.sample_rate * duration)
        noise = np.random.uniform(-1, 1, samples)
        
        # Apply period for different noise types
        if period > 1:
            for i in range(period, samples):
                noise[i] = noise[i - period]
        
        return noise * volume
    
    def generate_envelope(self, duration: float, attack: float = 0.1, 
                         decay: float = 0.2, sustain: float = 0.7, 
                         release: float = 0.3) -> np.ndarray:
        """Generate ADSR envelope."""
        samples = int(self.sample_rate * duration)
        envelope = np.zeros(samples)
        
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        sustain_samples = samples - attack_samples - decay_samples - release_samples
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        if decay_samples > 0:
            start_idx = attack_samples
            end_idx = start_idx + decay_samples
            envelope[start_idx:end_idx] = np.linspace(1, sustain, decay_samples)
        
        # Sustain
        if sustain_samples > 0:
            start_idx = attack_samples + decay_samples
            end_idx = start_idx + sustain_samples
            envelope[start_idx:end_idx] = sustain
        
        # Release
        if release_samples > 0:
            start_idx = attack_samples + decay_samples + sustain_samples
            envelope[start_idx:] = np.linspace(sustain, 0, release_samples)
        
        return envelope
    
    def mix_channels(self, *channels) -> np.ndarray:
        """Mix multiple audio channels."""
        if not channels:
            return np.array([])
        
        max_length = max(len(ch) for ch in channels)
        mixed = np.zeros(max_length)
        
        for channel in channels:
            if len(channel) < max_length:
                padded = np.pad(channel, (0, max_length - len(channel)), 'constant')
            else:
                padded = channel
            mixed += padded
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.8
        
        return mixed
    
    def save_wav(self, audio_data: np.ndarray, filename: str) -> None:
        """Save audio data as WAV file."""
        # Convert to 16-bit integers
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
    
    def play_audio(self, audio_data: np.ndarray) -> None:
        """Play audio data using system audio."""
        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            self.save_wav(audio_data, tmp_file.name)
            
            try:
                # Try different audio players
                if sys.platform == "darwin":  # macOS
                    subprocess.run(["afplay", tmp_file.name], check=False, timeout=10)
                elif sys.platform.startswith("linux"):  # Linux
                    subprocess.run(["aplay", tmp_file.name], check=False, timeout=10)
                elif sys.platform == "win32":  # Windows
                    subprocess.run(["start", tmp_file.name], check=False, timeout=10, shell=True)
                else:
                    # Fallback to system bell
                    print("🔔", end="", flush=True)
            except Exception:
                print("🔔", end="", flush=True)
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass


def create_mario_theme(synth: ChiptuneSynthesizer) -> np.ndarray:
    """Create the iconic Super Mario Bros. main theme."""
    # Mario theme notes (in Hz)
    notes = [
        (659, 0.2), (659, 0.2), (0, 0.1), (659, 0.2), (0, 0.1), (523, 0.2), (659, 0.2), (0, 0.1),  # Opening
        (784, 0.2), (0, 0.1), (0, 0.1), (0, 0.1), (392, 0.2), (0, 0.1), (0, 0.1), (0, 0.1),  # First phrase
        (523, 0.2), (0, 0.1), (392, 0.2), (0, 0.1), (330, 0.2), (0, 0.1), (440, 0.2), (0, 0.1),  # Second phrase
        (494, 0.2), (0, 0.1), (466, 0.2), (440, 0.2), (0, 0.1), (392, 0.2), (659, 0.2), (784, 0.2),  # Third phrase
        (880, 0.2), (0, 0.1), (659, 0.2), (523, 0.2), (440, 0.2), (0, 0.1), (392, 0.2), (0, 0.1),  # Fourth phrase
        (330, 0.2), (0, 0.1), (440, 0.2), (0, 0.1), (494, 0.2), (0, 0.1), (466, 0.2), (440, 0.2),  # Fifth phrase
        (392, 0.2), (0, 0.1), (659, 0.2), (523, 0.2), (440, 0.2), (0, 0.1), (392, 0.2), (0, 0.1),  # Sixth phrase
        (330, 0.2), (0, 0.1), (440, 0.2), (0, 0.1), (494, 0.2), (0, 0.1), (466, 0.2), (440, 0.2)   # Final phrase
    ]
    
    channels = []
    
    for freq, duration in notes:
        if freq == 0:  # Rest
            channels.append(np.zeros(int(synth.sample_rate * duration)))
        else:
            # Main melody (square wave)
            melody = synth.generate_square_wave(freq, duration, 0.6, 0.5)
            # Add some triangle wave for bass
            bass_freq = freq * 0.5 if freq > 200 else freq
            bass = synth.generate_triangle_wave(bass_freq, duration, 0.3)
            
            # Mix melody and bass
            note = synth.mix_channels(melody, bass)
            channels.append(note)
    
    return np.concatenate(channels)


def create_desperado_theme(synth: ChiptuneSynthesizer) -> np.ndarray:
    """Create the Eagles 'Desperado' opening melody."""
    # Desperado melody (in Hz)
    notes = [
        (523, 0.4), (0, 0.1), (659, 0.4), (0, 0.1), (784, 0.4), (0, 0.1), (659, 0.4), (0, 0.1),  # "Desperado, why don't you come to your senses"
        (523, 0.4), (0, 0.1), (440, 0.4), (0, 0.1), (392, 0.4), (0, 0.1), (440, 0.4), (0, 0.1),  # "You've been out ridin' fences"
        (523, 0.4), (0, 0.1), (659, 0.4), (0, 0.1), (784, 0.4), (0, 0.1), (880, 0.4), (0, 0.1),  # "for so long now"
        (784, 0.4), (0, 0.1), (659, 0.4), (0, 0.1), (523, 0.4), (0, 0.1), (440, 0.4), (0, 0.1),  # "Oh, you're a hard one"
        (392, 0.4), (0, 0.1), (440, 0.4), (0, 0.1), (523, 0.4), (0, 0.1), (659, 0.4), (0, 0.1),  # "But I know that you have"
        (523, 0.4), (0, 0.1), (440, 0.4), (0, 0.1), (392, 0.4), (0, 0.1), (330, 0.4), (0, 0.1),  # "your reasons"
        (440, 0.4), (0, 0.1), (523, 0.4), (0, 0.1), (659, 0.4), (0, 0.1), (784, 0.4), (0, 0.1),  # "These things that are pleasin' you"
        (659, 0.4), (0, 0.1), (523, 0.4), (0, 0.1), (440, 0.4), (0, 0.1), (392, 0.4), (0, 0.1)   # "Can hurt you somehow"
    ]
    
    channels = []
    
    for freq, duration in notes:
        if freq == 0:  # Rest
            channels.append(np.zeros(int(synth.sample_rate * duration)))
        else:
            # Main melody (triangle wave for softer sound)
            melody = synth.generate_triangle_wave(freq, duration, 0.7)
            # Add some square wave for harmonics
            harmonic = synth.generate_square_wave(freq * 2, duration, 0.2, 0.25)
            
            # Mix melody and harmonic
            note = synth.mix_channels(melody, harmonic)
            channels.append(note)
    
    return np.concatenate(channels)


def create_clown_theme(synth: ChiptuneSynthesizer) -> np.ndarray:
    """Create a circus/clown theme based on 'Entry of the Gladiators'."""
    # Circus theme notes (in Hz)
    notes = [
        (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2),  # C5 repeated
        (659, 0.2), (659, 0.2), (659, 0.2), (659, 0.2), (659, 0.2), (659, 0.2), (659, 0.2), (659, 0.2),  # E5 repeated
        (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2), (523, 0.2),  # C5 repeated
        (440, 0.2), (440, 0.2), (440, 0.2), (440, 0.2), (440, 0.2), (440, 0.2), (440, 0.2), (440, 0.2),  # A4 repeated
        (523, 0.3), (659, 0.3), (784, 0.3), (880, 0.4), (784, 0.3), (659, 0.3), (523, 0.3), (440, 0.4)   # C-E-G-A-G-E-C-A
    ]
    
    channels = []
    
    for freq, duration in notes:
        # Main melody (square wave)
        melody = synth.generate_square_wave(freq, duration, 0.6, 0.5)
        # Add some noise for circus effect
        noise = synth.generate_noise(duration, 0.1, 4)
        
        # Mix melody and noise
        note = synth.mix_channels(melody, noise)
        channels.append(note)
    
    return np.concatenate(channels)


def main():
    """Test the chiptune synthesizer."""
    print("🎵 Chiptune Synthesizer Test")
    print("=" * 30)
    
    synth = ChiptuneSynthesizer()
    
    print("🎮 Generating Mario theme...")
    mario_audio = create_mario_theme(synth)
    print("🔊 Playing Mario theme...")
    synth.play_audio(mario_audio)
    
    print("\n🤠 Generating Desperado theme...")
    desperado_audio = create_desperado_theme(synth)
    print("🔊 Playing Desperado theme...")
    synth.play_audio(desperado_audio)
    
    print("\n🤡 Generating Clown theme...")
    clown_audio = create_clown_theme(synth)
    print("🔊 Playing Clown theme...")
    synth.play_audio(clown_audio)
    
    print("\n✅ Chiptune synthesizer test complete!")


if __name__ == "__main__":
    main()
