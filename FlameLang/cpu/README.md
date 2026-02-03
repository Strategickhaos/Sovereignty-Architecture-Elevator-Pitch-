# FlameLang CPU Module

## Vocal Independence Trainer

### Overview
The vocal independence trainer (`vocal_independence_trainer.py`) is a Python-based tool for deep independence vocal training. It generates BWE (Brainwave Entrainment) backed audio guides for vocal exercises with progressive independence drills.

### Features
- **BWE Layer**: Generates binaural/isochronic audio for 7-12Hz alpha entrainment (vagal/resonance)
- **Drill Layer**: Click track for pedal independence (sync voice to beats, then desync for bilateral mastery)
- **TRIG6 Integration**: Maps Norm² to target Hz (e.g., 7=~100Hz deep chest)
- **Progressive Sessions**: Start synced, progress to independent (voice steady, pedals vary)

### Dependencies
```bash
pip install numpy scipy
```

Optional for MIDI support:
```bash
pip install mido
```

### Usage
```bash
cd FlameLang/cpu
python3 vocal_independence_trainer.py
```

### Output
The script generates three files in the `vocal_sessions/` directory:
- `bwe_{session_id}.wav`: Binaural/isochronic audio for resonance entrainment
- `drill_{session_id}.wav`: Click track for pedal independence
- `session_{session_id}.wav`: Merged audio combining BWE and drill tracks

### How It Works
1. **BWE Generation**: Creates binaural beats with a base frequency and alpha delta (7-12Hz) for chest resonance entrainment
2. **Drill Creation**: Generates click tracks at specified BPM (default 140) for rhythmic training
3. **Session Building**: Merges BWE and drill layers with proper attenuation for optimal training

### Training Progression
1. Run 10 sessions per day
2. Gradually increase BPM and desync complexity
3. Track progress with spectrogram analysis (e.g., using Audacity)

### Customization
Edit the configuration variables at the top of the script:
- `SAMPLE_RATE`: Audio sample rate (default: 44100 Hz)
- `DURATION_SEC`: Exercise duration (default: 60 seconds)
- `BASE_FREQ`: Binaural base frequency (default: 200 Hz)
- `ALPHA_DELTA`: Target alpha range for chest resonance (default: 10 Hz for 7-12Hz range)

### Future Enhancements
- MIDI note generation for vocal guidance
- Full TRIG6 table integration for 64 progressive sessions
- Variable BPM progression
- Automated session scheduling
