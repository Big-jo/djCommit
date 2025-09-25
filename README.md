# 🎵 Deep Learning Git Hook DJ

A fun Git pre-commit hook that analyzes your staged code changes using machine learning and plays appropriate audio feedback based on commit quality!

## 🎯 Features

- **ML-Powered Analysis**: Uses Hugging Face transformers to analyze commit diffs
- **High-Quality Audio**: Plays authentic chiptune versions of iconic songs:
  - 🤡 **Bad commits** → Circus/Clown theme ("Entry of the Gladiators" opening)
  - 🪙 **Good commits** → Super Mario Bros. main theme (iconic opening melody)  
  - 🤠 **Stellar commits** → Eagles "Desperado" opening melody
- **NES-Style Synthesis**: Based on academic research in chiptune synthesis and NES APU emulation
- **Multiple Audio Methods**: Chiptune synthesizer, C beep program, and fallback options
- **Colorful Terminal Output**: Beautiful colored logs for better user experience
- **Fallback Heuristics**: Works even without ML dependencies
- **Karma Tracking**: Saves your commit quality history
- **ASCII Art**: Visual feedback alongside audio
- **Fast Performance**: Runs in under 2 seconds

## 📋 Requirements

- Python 3.7+
- Git repository
- Terminal with bell support (most modern terminals)

## 🚀 Installation

### 1. Clone or Download

```bash
git clone <your-repo-url>
cd dj_commit
```

### 2. Install Dependencies (Optional)

For full ML functionality:
```bash
pip install -r requirements.txt
```

**Note**: The script works without ML dependencies using fallback heuristics!

### 3. Install the Git Hook

```bash
# Make the pre-commit hook executable
chmod +x pre-commit

# Copy it to your git hooks directory
cp pre-commit .git/hooks/pre-commit
```

### 4. Test the Installation

```bash
# Super easy installation (recommended)
python3 setup.py

# Or use the CLI for more control
python3 dj_cli.py install

# Or use the original install script
./install.sh

# Test the system
python3 dj_cli.py status
python3 dj_cli.py demo
```

## 🎮 Usage

### CLI Commands

The new CLI makes everything super easy:

```bash
# Install everything (recommended for new users)
python3 setup.py

# Or use the CLI for more control
python3 dj_cli.py install     # Install everything
python3 dj_cli.py status      # Check system status
python3 dj_cli.py demo        # Run interactive demo
python3 dj_cli.py test        # Test all components
python3 dj_cli.py uninstall   # Remove git hook
```

### Automatic Usage
The hook runs automatically on every commit:

```bash
git add .
git commit -m "Your commit message"
# 🎵 Git Hook DJ will analyze and play sounds!
```

### Manual Testing
You can test the system manually:

```bash
# Stage some changes
git add .

# Run the DJ manually
python3 git_dj.py
```

### Demo Mode
Run the complete demo to see all features:

```bash
# Run the interactive demo
python3 demo.py
```

This will:
- Create test files for different commit types
- Demonstrate all sound effects
- Show commit analysis in action
- Display karma tracking
- Clean up test files automatically

### Testing Different Commit Types

**Bad Commit** (small changes):
```bash
echo "// TODO" >> test.js
git add test.js
git commit -m "Add todo"
# 🤡 Clown honk!
```

**Good Commit** (moderate changes):
```bash
# Make some substantial changes
git add .
git commit -m "Refactor user service"
# 🪙 Mario coin!
```

**Stellar Commit** (tests or new functions):
```bash
# Add a new function or test
echo "def new_feature(): pass" >> main.py
git add main.py
git commit -m "Add new feature"
# 🤠 Desperado theme!
```

## 🔧 Configuration

### Classification Heuristics

The system uses these fallback rules when ML is unavailable:

- **Bad**: < 10 lines of changes
- **Good**: 10+ lines of changes  
- **Stellar**: Changes include tests or new functions

### Karma Tracking

Your commit quality is tracked in `.git/karma.json`:

```json
{
  "bad": 5,
  "good": 12,
  "stellar": 3,
  "total": 20
}
```

### Customizing Sounds

The system uses multiple audio methods for maximum compatibility:

1. **Chiptune Synthesizer** (`chiptune_synth.py`) - Primary method:
   - NES-style square waves, triangle waves, and noise
   - Based on academic research in procedural music generation
   - Generates authentic 8-bit style audio
   - Customize melodies by editing the note arrays

2. **C Beep Program** (`beep.c`) - Secondary method:
   - Edit frequency arrays and durations
   - Add new sound types
   - Recompile with `gcc -o beep beep.c -framework AudioToolbox` (macOS)

3. **Python Fallback** - Edit `beep_player.py` for simple beep patterns:
   ```python
   def custom_sound():
       # Your custom beep pattern
       play_beep()
       time.sleep(0.5)
       play_beep()
   ```

### Testing Audio Generation

Generate test audio files to verify the synthesizer:
```bash
python3 test_audio.py
# Creates: mario_theme.wav, desperado_theme.wav, clown_theme.wav
```

## 🛠️ Troubleshooting

### No Sound Playing
- Ensure your terminal supports bell characters
- Try running `printf "\a"` to test system bell
- Check that your terminal volume is up

### ML Model Issues
- Install dependencies: `pip install -r requirements.txt`
- The system falls back to heuristics if ML fails
- Check console output for error messages

### Git Hook Not Running
- Ensure the hook is executable: `chmod +x .git/hooks/pre-commit`
- Check that the hook file is in the correct location
- Verify the Python script path in the hook

### Performance Issues
- The system has a 2-second timeout for ML analysis
- Falls back to heuristics if too slow
- Consider using a smaller model for faster performance

## 🎨 Customization

### Adding New Commit Types

1. Edit `git_dj.py` to add new classification logic
2. Add corresponding beep function in `beep_player.py`
3. Update the main function to call your new sound

### Using Different ML Models

Replace the model in `git_dj.py`:

```python
# Use a different model
model_name = "microsoft/codebert-base"  # or your custom model
```

### Custom ASCII Art

Edit the `display_ascii_art()` function in `git_dj.py` to add your own art.

## 📁 Project Structure

```
dj_commit/
├── dj_cli.py          # Command-line interface (main entry point)
├── setup.py           # Super simple setup script
├── git_dj.py          # Main analysis script with colorful output
├── beep_player.py     # Audio feedback functions with colors
├── chiptune_synth.py  # NES-style chiptune synthesizer
├── beep.c             # C program for high-quality audio
├── beep               # Compiled C beep program
├── pre-commit         # Git hook script
├── requirements.txt   # Python dependencies
├── install.sh         # Original installation script
├── demo.py           # Demo script
├── .gitignore        # Git ignore file
├── LICENSE           # MIT License
├── QUICKSTART.md     # Quick start guide
└── README.md         # This file
```

## 📚 Research Foundation

This project is built on academic research in chiptune synthesis and procedural music generation:

### Key Papers
- **"Endless Loop: A Brief History of Chiptunes"** by Kevin Driscoll and Joshua Diaz (Transformative Works and Cultures, 2009)
- **"Chiptune: The Ludomusical Shaping of Identity"** (ResearchGate, 2018)
- **"Signal Processing for Sound Synthesis: Computer-Generated Sounds and Music for All"** (ResearchGate, 2006)
- **"Automatic Sound Synthesizer Programming: Techniques and Applications"** (ResearchGate, 2016)

### Technical Implementation
- NES 2A03 APU (Audio Processing Unit) emulation
- Square wave synthesis with configurable duty cycles
- Triangle wave generation for bass and melody
- White noise generation for percussion effects
- ADSR envelope implementation for realistic sound shaping

### References
- [NES Technical Documentation](https://wiki.nesdev.com/w/index.php/APU)
- [Chiptune Synthesis Papers](https://www.semanticscholar.org/topic/Chiptune/1707298)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed!

## 🚀 Future Roadmap

Exciting features coming soon:
- **Tree-sitter AST integration** for language-specific code analysis
- **Advanced ML models** combining AST structure with deep learning
- **Procedural music generation** based on code complexity and structure
- **Multi-language support** with framework-aware analysis
- **Real-time audio feedback** during coding sessions

## 🎵 Enjoy Your Musical Commits!

Happy coding and may your commits always be stellar! 🚀
