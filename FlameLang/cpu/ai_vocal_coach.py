# ai_vocal_coach.py - AI voice gen for deep independence training
# Install: pip install TTS scipy numpy
from TTS.api import TTS
import numpy as np
from scipy.io.wavfile import write, read
import os
import math

# Config
OUTPUT_DIR = "ai_vocal_sessions"
os.makedirs(OUTPUT_DIR, exist_ok=True)
MODEL = "tts_models/en/ljspeech/tacotron2-DDC"  # Free model; swap for others
SAMPLE_RATE = 22050  # Coqui default
DURATION_SEC = 60
BPM = 140
ALPHA_HZ = 10  # Resonance target

# Load TTS
tts = TTS(model_name=MODEL, progress_bar=True)

# Gen AI voice prompt
def gen_voice(text, path):
    wav = tts.tts(text=text, speaker_wav=None, language="en")
    # Convert float32 [-1, 1] to int16 for WAV
    wav_int16 = (np.array(wav) * 32767).astype(np.int16)
    write(path, SAMPLE_RATE, wav_int16)
    return path

# Gen pedal click track
def gen_clicks(bpm=BPM, duration=DURATION_SEC):
    beat_interval = SAMPLE_RATE * (60 / bpm)
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    clicks = np.zeros_like(t)
    for i in range(int(duration * bpm / 60)):
        start = int(i * beat_interval)
        clicks[start:start+int(SAMPLE_RATE*0.01)] = 1.0
    return clicks

# Pitch shift for resonance (simple resampling approach)
def pitch_shift(wav_data, shift_semitones):
    # Calculate frequency ratio for semitone shift
    freq_ratio = 2 ** (shift_semitones / 12)
    
    # Simple time-domain resampling (crude but functional)
    # For production use, consider librosa or soundfile
    indices = np.arange(0, len(wav_data), freq_ratio)
    indices = indices[indices < len(wav_data)].astype(int)
    
    # Resample by indexing
    shifted = wav_data[indices]
    
    # Ensure output is int16
    if shifted.dtype != np.int16:
        shifted = shifted.astype(np.int16)
    
    return shifted

# Build session: AI prompt + shanty sample + clicks
def build_session(session_id=1, text_prompt="Deep chest resonance, sync to beat then desync for independence. Hoist the Colors High.", target_hz=100):
    print(f"Session {session_id}: Target {target_hz}Hz resonance")
    
    # AI voice prompt
    prompt_path = f"{OUTPUT_DIR}/prompt_{session_id}.wav"
    gen_voice(text_prompt, prompt_path)
    
    # Shanty sample (AI gen)
    shanty_text = "The king and his men stole the queen from her bed and bound her in her bones."
    shanty_path = f"{OUTPUT_DIR}/shanty_{session_id}.wav"
    gen_voice(shanty_text, shanty_path)
    
    # Pitch shift to target Hz (approx fundamental)
    shanty_sample_rate, shanty_data = read(shanty_path)
    shift_semitones = 12 * math.log2(target_hz / 100)  # Assume base ~100Hz
    shifted_shanty = pitch_shift(shanty_data, shift_semitones)
    shifted_path = f"{OUTPUT_DIR}/shifted_shanty_{session_id}.wav"
    write(shifted_path, SAMPLE_RATE, shifted_shanty)
    
    # Clicks
    clicks = gen_clicks()
    
    # Merge: Prompt + shifted shanty + clicks overlay
    max_len = max(len(shifted_shanty), len(clicks))
    merged = np.zeros(max_len)
    
    # Normalize shanty (guard against silent audio)
    shanty_max = np.max(np.abs(shifted_shanty))
    if shanty_max > 0:
        merged[:len(shifted_shanty)] += shifted_shanty / shanty_max
    
    merged[:len(clicks)] += clicks * 0.3
    
    # Final normalization (guard against all-zero audio)
    merged_max = np.max(np.abs(merged))
    if merged_max > 0:
        merged = (merged / merged_max) * 32767
    
    final_path = f"{OUTPUT_DIR}/session_{session_id}.wav"
    write(final_path, SAMPLE_RATE, merged.astype(np.int16))
    print(f"Session WAV: {final_path}")

if __name__ == "__main__":
    build_session()
