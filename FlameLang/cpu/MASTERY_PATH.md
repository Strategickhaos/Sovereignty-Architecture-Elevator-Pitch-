# 🎯 AI Vocal Coach - Mastery Path Quick Reference

## Overview
Progressive vocal independence training using AI-generated coaching and shanty samples.

## Training Phases

### Phase 1: Synchronization (Sessions 1-5)
**Goal**: Sync voice to clicks (sing shanty on beat)

**Technique**:
- Listen to the click track
- Sing shanty lyrics precisely on beat
- Match pitch to target Hz
- Focus on timing accuracy

**Progress Metric**: Can maintain steady rhythm without drift

```bash
python ai_vocal_coach.py  # Session 1, 100Hz baseline
```

---

### Phase 2: Desynchronization (Sessions 6-10)
**Goal**: Sing steady while pedals vary BPM

**Technique**:
- Maintain your vocal rhythm
- Let click track vary (change BPM mid-session)
- Resist following the metronome
- Keep internal tempo steady

**Progress Metric**: Can hold pitch/rhythm independent of external cues

```python
# Modify BPM mid-training to practice desync
build_session(session_id=6, target_hz=120)
```

---

### Phase 3: Independence (Sessions 11+)
**Goal**: AI prompt random desync, target Hz shifts via TRIG6 norm

**Technique**:
- Random BPM changes from AI
- Frequency shifts during session
- Maintain vocal control through changes
- Deep chest rumble at 7-12Hz target

**Progress Metric**: Complete independence from external rhythm

```python
# Advanced sessions with frequency progression
for i in range(11, 16):
    build_session(session_id=i, target_hz=100 + (i * 3))
```

---

## Tracking Progress

### Spectral Analysis in Audacity
1. Open session WAV file
2. Select audio region
3. `Analyze → Plot Spectrum`
4. Look for fundamental frequency peak (100-160Hz vocal range)
5. Monitor harmonic overtones and resonance patterns
6. Compare across sessions to track improvement

**Note**: The 7-12Hz alpha wave range refers to brainwave entrainment through session pacing, not vocal frequency. Actual vocal targets are 100-160Hz.

### Session Recording
- Record your live performance during training
- Compare to generated shanty sample
- Analyze pitch stability
- Track resonance frequency achievement

---

## TRIG6 Frequency Map

| Session | Target Hz | Focus Area |
|---------|-----------|------------|
| 1-3     | 100-110   | Alpha baseline, low chest |
| 4-6     | 115-125   | Mid chest resonance |
| 7-9     | 130-140   | Upper chest, head voice |
| 10-12   | 145-155   | Voice transition zone |
| 13+     | 160+      | Full range mastery |

---

## Quick Commands

```bash
# Basic session
python ai_vocal_coach.py

# Custom session
python example_usage.py

# Progressive series
python -c "from ai_vocal_coach import build_session; [build_session(i, 100+(i*5)) for i in range(1,6)]"

# Install dependencies
pip install -r requirements.vocal.txt
```

---

## Success Indicators

### Beginner (Sessions 1-5)
- ✅ Can follow click track
- ✅ Pitch matches target Hz ±10Hz
- ✅ Complete full session without breaks

### Intermediate (Sessions 6-10)
- ✅ Maintain rhythm without clicks
- ✅ Pitch stable during BPM changes
- ✅ Chest resonance detectable in spectrogram

### Advanced (Sessions 11+)
- ✅ Complete independence from metronome
- ✅ Fundamental frequency stable at target Hz (100-160Hz range)
- ✅ Can vary frequency on command
- ✅ Control maintained through random changes
- ✅ Strong harmonic overtones visible in spectrogram

---

## Tips for Maximum Results

1. **Hydration**: Drink water before training
2. **Posture**: Sit upright, feet flat
3. **Breathing**: Deep diaphragmatic breaths
4. **Focus**: Close eyes, feel the vibration
5. **Consistency**: Daily 15-minute sessions
6. **Recording**: Track every session for analysis
7. **Rest**: Allow vocal recovery between sessions

---

## Troubleshooting

**Can't hit target Hz?**
- Lower initial target (90-95Hz)
- Focus on chest resonance
- Try humming first

**Losing tempo?**
- Slow BPM (100-120)
- Increase click volume
- Practice with tapping

**Voice fatigue?**
- Reduce session duration (30 sec)
- More water breaks
- Lower volume/intensity

---

**"Your shanties got an AI coach."** 😈😂💜
