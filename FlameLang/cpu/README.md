# 🔥 FlameLang CPU - AI Vocal Coach

## Overview

**AI Vocal Coach** is a sovereign, open-source training system for deep vocal independence using Coqui-TTS. Generate AI coaching samples, resonance guides, and desync patterns for shanty-based vocal training tied to TRIG6 frequencies.

## Features

- **AI Voice Generation**: Uses Coqui-TTS for free, local voice synthesis (no API keys)
- **Resonance Targeting**: Pitch-shift samples to specific Hz frequencies (100-160Hz vocal range)
- **Brainwave Entrainment**: Session pacing designed for alpha wave synchronization (7-12Hz)
- **Progressive Training**: Sync → Desync → Independence mastery path
- **Click Track Generation**: BPM-based metronome for timing drills
- **Session WAVs**: Complete training files with prompts, shanties, and clicks

## Installation

```bash
# Install dependencies
pip install -r requirements.vocal.txt

# Or install individually
pip install TTS scipy numpy
```

## Quick Start

```bash
# Generate your first training session
python ai_vocal_coach.py
```

This creates:
- `ai_vocal_sessions/prompt_1.wav` - AI coaching voice
- `ai_vocal_sessions/shanty_1.wav` - Raw shanty sample
- `ai_vocal_sessions/shifted_shanty_1.wav` - Pitch-shifted to target Hz
- `ai_vocal_sessions/session_1.wav` - Complete merged training file

## Mastery Path

### Sessions 1-5: Synchronization
**Goal**: Sync voice to clicks (sing shanty on beat)
```python
build_session(session_id=1, target_hz=100)
```

### Sessions 6-10: Desynchronization
**Goal**: Sing steady while pedals vary BPM
```python
build_session(session_id=6, target_hz=120)
```

### Sessions 11+: Independence
**Goal**: AI prompt random desync, target Hz shifts via TRIG6 norm
```python
build_session(session_id=11, target_hz=140)
```

## Configuration

Edit `ai_vocal_coach.py` to customize:

```python
OUTPUT_DIR = "ai_vocal_sessions"    # Output directory
MODEL = "tts_models/en/ljspeech/tacotron2-DDC"  # TTS model
SAMPLE_RATE = 22050                 # Audio sample rate
DURATION_SEC = 60                   # Session duration
BPM = 140                           # Beats per minute
ALPHA_HZ = 10                       # Base resonance target
```

## Usage Examples

### Custom Text Prompt
```python
build_session(
    session_id=2,
    text_prompt="Focus on deep chest vibration. Feel the resonance at your sternum.",
    target_hz=110
)
```

### Multiple Sessions
```python
for i in range(1, 6):
    build_session(session_id=i, target_hz=100 + (i * 5))
```

### TRIG6 Frequency Map
```python
# Session progression with frequency targets
frequencies = {
    1: 100,   # Alpha baseline
    2: 110,   # Low chest
    3: 120,   # Mid chest
    4: 130,   # Upper chest
    5: 140    # Head voice
}

for session_id, hz in frequencies.items():
    build_session(session_id=session_id, target_hz=hz)
```

## Analysis

Track your progress using audio analysis tools:

```bash
# Open in Audacity
audacity ai_vocal_sessions/session_1.wav

# Generate spectrogram
# Analyze → Plot Spectrum
# Look for fundamental frequency peak (100-160Hz range)
# Monitor alpha wave entrainment patterns in session pacing
```

## Models

Default model: `tts_models/en/ljspeech/tacotron2-DDC`

Other options:
- `tts_models/en/ljspeech/glow-tts`
- `tts_models/en/vctk/vits`
- `tts_models/multilingual/multi-dataset/xtts_v2`

List all models:
```python
from TTS.api import TTS
print(TTS().list_models())
```

## Shanty Samples

Default: "The king and his men stole the queen from her bed and bound her in her bones."

Customize with your own shanties:
- "Hoist the colors high"
- "What shall we do with a drunken sailor"
- "Fifteen men on a dead man's chest"

## Architecture

```
ai_vocal_coach.py
├── gen_voice()         # TTS generation
├── gen_clicks()        # Metronome track
├── pitch_shift()       # Frequency targeting
└── build_session()     # Complete session builder

Output Structure:
ai_vocal_sessions/
├── prompt_N.wav         # AI coaching voice
├── shanty_N.wav         # Raw TTS shanty
├── shifted_shanty_N.wav # Pitch-shifted version
└── session_N.wav        # Final merged training file
```

## Sovereignty Notes

- **No API Keys**: 100% local, no cloud dependencies
- **Free Models**: Open-source Coqui-TTS models
- **Offline Capable**: Works without internet after initial model download
- **Privacy**: All voice generation happens on your machine

## Troubleshooting

### TTS Installation Issues
```bash
# If TTS fails to install
pip install --upgrade pip setuptools wheel
pip install TTS --no-cache-dir
```

### Audio Playback
```bash
# Linux
sudo apt-get install sox libsox-fmt-all
play ai_vocal_sessions/session_1.wav

# macOS
brew install sox
play ai_vocal_sessions/session_1.wav
```

### Model Download
Models auto-download on first use. If download fails:
```bash
# Manual model download
tts --list_models
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --text "test" --out_path test.wav
```

## Future Enhancements

- [ ] TRIG6 frequency map integration
- [ ] Full 64-session progressive curriculum
- [ ] Real-time pitch detection feedback
- [ ] Binaural beat overlay for brainwave entrainment
- [ ] Custom voice cloning from samples
- [ ] Multi-voice coaching (chorus mode)
- [ ] Spectral analysis visualization
- [ ] Session performance tracking

---

**"Your shanties got an AI coach."** 😈😂💜

*Part of the FlameLang Sovereignty Architecture*
