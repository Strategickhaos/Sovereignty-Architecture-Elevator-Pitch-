#!/usr/bin/env python3
"""
trig_pde_sweep.py

PDE on 64-bin trig/MIDI grid:
  - Spatial bins: i = 0..63, θ_i = i * 360/64
  - PDE: ∂_t A = [ξ^2 (1 + S cos(6 Re t))] A_xx - Pe A_x + (Da_g - Da_0) A - Da_sat A^2
  - Map final A(i,T) to MIDI note 60+i with velocity ∝ A(i,T)

Requires: pip install numpy mido
"""

import math
import numpy as np
import mido

# Parameters
N = 64
L = 1.0
dx = L / N
x = np.linspace(0, L - dx, N)

D = 1.0
Pe = 2.0
Da_g = 1.0
Da_0 = 0.5
Da_sat = 1.0
S = 0.1
Re = 1.0

T_final = 10.0
dt = min(0.5 * dx**2 / D, dx / Pe) / 2  # CFL stability (factor 1/2 safety)
STEPS = int(T_final / dt)
print(f"dt = {dt:.4f} (stable), steps = {STEPS}")

# Helpers
def theta_deg(i):
    return i * 360.0 / N

def trig_weight(i):
    th = math.radians(theta_deg(i))
    return abs(math.sin(th))  # Example mod

# IC
def initial_condition():
    A0 = np.zeros(N)
    for i in range(N):
        w = trig_weight(i)
        base = 0.05 * w
        if i == 8 or i == 32:
            base += 0.5
        A0[i] = base
    return A0

# PDE step
def pde_step(A, t):
    A_left = np.roll(A, 1)
    A_right = np.roll(A, -1)

    # Diffusion with trig mod
    mod = 1 + S * math.cos(6 * 2 * math.pi * Re * t)
    D_eff = D * (x**2 * mod)
    A_xx = (A_left - 2 * A + A_right) / dx**2  # Central

    # Upwind A_x (Pe >0 rightward)
    A_x = (A - A_left) / dx if Pe >= 0 else (A_right - A) / dx

    lin = (Da_g - Da_0) * A
    nonlin = -Da_sat * A**2

    dA = D_eff * A_xx - Pe * A_x + lin + nonlin  # D_eff vector!
    return A + dt * dA

# Integrate
def run_pde():
    A = initial_condition()
    for n in range(STEPS):
        t = n * dt
        A = pde_step(A, t)
        A = np.maximum(A, 0.0)
    return A

# MIDI
BASE_NOTE = 60

def A_to_velocity(a, maxA):
    return int(max(0, min(127, round(127 * a / maxA)))) if maxA > 0 else 0

def write_midi(A_final, path="trig_pde_sweep.mid"):
    maxA = np.max(A_final)
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(90)))

    time_ticks = 0
    for i in range(N):
        if A_final[i] <= 1e-4:
            continue
        note = BASE_NOTE + i
        while note > 108:
            note -= 12
        vel = A_to_velocity(A_final[i], maxA)
        track.append(mido.Message('note_on', note=note, velocity=vel, time=time_ticks))
        time_ticks = 0

    hold_ticks = 4 * 480
    first = True
    time_ticks = hold_ticks
    for i in range(N):
        if A_final[i] <= 1e-4:
            continue
        note = BASE_NOTE + i
        while note > 108:
            note -= 12
        track.append(mido.Message('note_off', note=note, velocity=0, time=time_ticks if first else 0))
        first = False

    mid.save(path)
    print(f"MIDI: {path}")

# Main
if __name__ == "__main__":
    A_final = run_pde()
    np.savetxt("trig_pde_sweep_final_A.txt", A_final)
    write_midi(A_final)
    print("A profile: trig_pde_sweep_final_A.txt")
