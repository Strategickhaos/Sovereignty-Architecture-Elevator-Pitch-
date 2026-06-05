import numpy as np
from scipy.io.wavfile import write, read
import math
import os

# Config
SAMPLE_RATE = 44100
DURATION_SEC = 60  # Per exercise
BASE_FREQ = 200    # Binaural base
ALPHA_DELTA = 10   # 7-12Hz target (chest resonance)
OUTPUT_DIR = "vocal_sessions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# TRIG6 freq map (demo: norm to Hz)
def trig6_to_hz(norm_sq, min_hz=80, max_hz=150):
    if norm_sq == 'inf':
        return max_hz
    return min_hz + (max_hz - min_hz) * (norm_sq / 200.0)  # Cap norm

# Generate BWE WAV (binaural + isochronic for resonance)
def generate_bwe(session_id, delta=ALPHA_DELTA, duration=DURATION_SEC):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    left = np.sin(2 * np.pi * BASE_FREQ * t)
    right = np.sin(2 * np.pi * (BASE_FREQ + delta) * t)
    pulse = (np.sin(2 * np.pi * delta * t) > 0).astype(float)  # Isochronic
    audio = np.vstack((left * pulse, right * pulse)).T
    max_val = np.abs(audio).max()
    if max_val > 0:
        audio = (audio / max_val) * 32767
    path = f"{OUTPUT_DIR}/bwe_{session_id}.wav"
    write(path, SAMPLE_RATE, audio.astype(np.int16))
    return path

# Vocal drill: Progressive independence (voice + "pedal" beat)
def vocal_drill(session_id, bpm=140, duration=DURATION_SEC):
    # Placeholder: Generate "pedal" click track (MIDI or WAV)
    beat_interval = SAMPLE_RATE * (60 / bpm)
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    clicks = np.zeros_like(t)
    for i in range(int(duration * bpm / 60)):
        start = int(i * beat_interval)
        clicks[start:start+int(SAMPLE_RATE*0.01)] = 1.0  # Short click
    audio = np.vstack((clicks, clicks)).T  # Stereo
    max_val = np.abs(audio).max()
    if max_val > 0:
        audio = (audio / max_val) * 32767
    path = f"{OUTPUT_DIR}/drill_{session_id}.wav"
    write(path, SAMPLE_RATE, audio.astype(np.int16))
    return path

# Master session: BWE + drill + trig freq guide
def build_session(trig_entry, session_id=1):
    # Trig-tied Hz for voice target
    norm_sq = trig_entry.get('Norm_Sq', 7.0)
    target_hz = trig6_to_hz(norm_sq)
    print(f"Session {session_id}: Target resonance ~{target_hz:.0f}Hz (from TRIG6 norm {norm_sq})")
    print("Exercise: Sing 'Hoist the Colors' deep chest, sync/desync to pedal clicks.")

    bwe_path = generate_bwe(session_id)
    drill_path = vocal_drill(session_id)
    # Merge: Overlay BWE + clicks (simple add, normalize)
    _, bwe_data = read(bwe_path)
    _, drill_data = read(drill_path)
    # Convert to float for safe arithmetic, then clip and convert back to int16
    merged = bwe_data.astype(np.float32) + drill_data.astype(np.float32) * 0.3
    merged = np.clip(merged, -32768, 32767).astype(np.int16)
    merged_path = f"{OUTPUT_DIR}/session_{session_id}.wav"
    write(merged_path, SAMPLE_RATE, merged)
    print(f"Session WAV: {merged_path}")
    # TODO: MIDI for notes if mido installed

if __name__ == "__main__":
    # Demo trig entry (from your table, Atomic 9)
    demo_trig = {"Norm_Sq": 7.0}
    build_session(demo_trig)
