# 🎵 Deep Learning Git Hook DJ

A fun Git pre-commit hook that analyzes your staged code changes using machine learning and plays appropriate audio feedback based on commit quality!

## 🎯 Features

- **ML-Powered Analysis**: Uses Hugging Face transformers to analyze commit diffs
- **High-Quality Audio**: Plays authentic chiptune versions of iconic songs:
  - 🤡 **Bad commits** → Circus/Clown theme ("Entry of the Gladiators" opening)
  - 🪙 **Good commits** → Super Mario Bros. main theme (iconic opening melody)  
  - 🤠 **Stellar commits** → Eagles "Desperado" opening melody
- **NES-Style Synthesis**: Uses academic research in procedural music generation
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
# Quick installation (recommended)
./install.sh

# Or test manually:
# Test the beep sounds
python3 beep_player.py

# Test the full system
python3 git_dj.py

# Run the complete demo
python3 demo.py
```

## 🎮 Usage

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
├── git_dj.py          # Main analysis script with colorful output
├── beep_player.py     # Audio feedback functions with colors
├── chiptune_synth.py  # NES-style chiptune synthesizer
├── beep.c             # C program for high-quality audio
├── beep               # Compiled C beep program
├── pre-commit         # Git hook script
├── requirements.txt   # Python dependencies
├── install.sh         # Installation script
├── demo.py           # Demo script
├── .gitignore        # Git ignore file
├── LICENSE           # MIT License
├── QUICKSTART.md     # Quick start guide
└── README.md         # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed!

## 🎵 Enjoy Your Musical Commits!

Happy coding and may your commits always be stellar! 🚀
