#!/usr/bin/env python3
"""
Vocal Independence Trainer
BWE (Brainwave Entrainment) + Click Tracks for vocal training
"""

import math
from typing import List, Tuple


class VocalIndependenceTrainer:
    """
    Generates binaural beats and click tracks for vocal independence training
    BWE = Brainwave Entrainment using binaural beats
    """
    
    def __init__(self, base_frequency: float = 432.0):
        """
        Initialize trainer
        
        Args:
            base_frequency: Base frequency in Hz (default 432 Hz - universal resonance)
        """
        self.base_frequency = base_frequency
        self.sample_rate = 44100  # Standard audio sample rate
        
        # Brainwave frequency ranges (Hz)
        self.brainwave_ranges = {
            'delta': (0.5, 4.0),    # Deep sleep
            'theta': (4.0, 8.0),    # Meditation, creativity
            'alpha': (8.0, 13.0),   # Relaxed awareness
            'beta': (13.0, 30.0),   # Active thinking
            'gamma': (30.0, 100.0)  # Peak performance
        }
    
    def generate_binaural_beat(self, target_frequency: float, 
                              duration: float = 10.0,
                              brainwave_type: str = 'alpha') -> Tuple[List[float], List[float]]:
        """
        Generate binaural beat for BWE
        
        Binaural beats work by playing slightly different frequencies in each ear.
        The brain perceives the difference as a "beat" frequency.
        
        Args:
            target_frequency: Base carrier frequency (Hz)
            duration: Length in seconds
            brainwave_type: Type of brainwave to entrain (delta, theta, alpha, beta, gamma)
        
        Returns:
            (left_channel, right_channel) audio samples
        """
        # Get brainwave frequency range
        bw_min, bw_max = self.brainwave_ranges.get(brainwave_type, (8.0, 13.0))
        beat_frequency = (bw_min + bw_max) / 2  # Use middle of range
        
        # Left ear: base frequency
        # Right ear: base frequency + beat frequency
        freq_left = target_frequency
        freq_right = target_frequency + beat_frequency
        
        num_samples = int(duration * self.sample_rate)
        
        left_channel = []
        right_channel = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            
            # Generate sine waves
            left_sample = math.sin(2 * math.pi * freq_left * t)
            right_sample = math.sin(2 * math.pi * freq_right * t)
            
            left_channel.append(left_sample)
            right_channel.append(right_sample)
        
        return left_channel, right_channel
    
    def generate_click_track(self, bpm: int = 120, duration: float = 10.0,
                            subdivision: int = 4) -> List[float]:
        """
        Generate click track for rhythm training
        
        Args:
            bpm: Beats per minute
            duration: Length in seconds
            subdivision: Subdivisions per beat (4 = sixteenth notes)
        
        Returns:
            Audio samples for click track
        """
        num_samples = int(duration * self.sample_rate)
        samples = [0.0] * num_samples
        
        # Calculate click interval
        seconds_per_beat = 60.0 / bpm
        seconds_per_click = seconds_per_beat / subdivision
        samples_per_click = int(seconds_per_click * self.sample_rate)
        
        # Generate clicks (short 1kHz tone bursts)
        click_frequency = 1000.0
        click_duration_samples = int(0.01 * self.sample_rate)  # 10ms clicks
        
        for click_num in range(int(duration / seconds_per_click)):
            start_sample = click_num * samples_per_click
            
            # Determine click strength (stronger on beat)
            if click_num % subdivision == 0:
                amplitude = 0.8  # Strong beat
            else:
                amplitude = 0.3  # Subdivision
            
            # Generate click
            for i in range(click_duration_samples):
                if start_sample + i < num_samples:
                    t = i / self.sample_rate
                    # Exponential decay envelope
                    envelope = math.exp(-10 * t / 0.01)
                    samples[start_sample + i] = (
                        amplitude * envelope * math.sin(2 * math.pi * click_frequency * t)
                    )
        
        return samples
    
    def generate_vocal_exercise(self, exercise_type: str = 'scale',
                               duration: float = 30.0) -> dict:
        """
        Generate complete vocal exercise with BWE and click track
        
        Args:
            exercise_type: Type of exercise ('scale', 'arpeggio', 'sustained')
            duration: Exercise duration in seconds
        
        Returns:
            Dictionary with exercise data
        """
        # Generate BWE background (theta for creative flow)
        left_bwe, right_bwe = self.generate_binaural_beat(
            self.base_frequency,
            duration,
            'theta'
        )
        
        # Generate click track (moderate tempo)
        click_track = self.generate_click_track(
            bpm=100,
            duration=duration,
            subdivision=4
        )
        
        # Generate pitch sequence for exercise
        if exercise_type == 'scale':
            # Major scale pattern
            intervals = [1.0, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2.0]
            pitches = [self.base_frequency * interval for interval in intervals]
            
        elif exercise_type == 'arpeggio':
            # Major arpeggio
            intervals = [1.0, 5/4, 3/2, 2.0]
            pitches = [self.base_frequency * interval for interval in intervals]
            
        else:  # sustained
            # Single sustained pitch
            pitches = [self.base_frequency]
        
        return {
            'type': exercise_type,
            'duration': duration,
            'base_frequency': self.base_frequency,
            'pitches': pitches,
            'bwe_left': left_bwe,
            'bwe_right': right_bwe,
            'click_track': click_track,
            'instructions': self._get_exercise_instructions(exercise_type)
        }
    
    def _get_exercise_instructions(self, exercise_type: str) -> str:
        """Get instructions for exercise type"""
        instructions = {
            'scale': (
                "Sing ascending and descending major scale.\n"
                "Focus on smooth transitions between notes.\n"
                "Maintain consistent vowel shape."
            ),
            'arpeggio': (
                "Sing major arpeggio (1-3-5-8).\n"
                "Emphasize clear pitch centers.\n"
                "Use sustained breath support."
            ),
            'sustained': (
                "Sustain single pitch for entire duration.\n"
                "Focus on steady tone and breath control.\n"
                "Experiment with dynamics (soft to loud)."
            )
        }
        return instructions.get(exercise_type, "Follow the pitch sequence.")
    
    def generate_polyrhythm_exercise(self, ratio: Tuple[int, int] = (3, 4),
                                    duration: float = 20.0) -> dict:
        """
        Generate polyrhythmic vocal independence exercise
        
        Args:
            ratio: Polyrhythm ratio (e.g., 3:4 means 3 beats against 4)
            duration: Exercise duration in seconds
        
        Returns:
            Dictionary with polyrhythm exercise data
        """
        # Generate two click tracks at different subdivisions
        click_track_a = self.generate_click_track(
            bpm=60,
            duration=duration,
            subdivision=ratio[0]
        )
        
        click_track_b = self.generate_click_track(
            bpm=60,
            duration=duration,
            subdivision=ratio[1]
        )
        
        return {
            'type': 'polyrhythm',
            'ratio': ratio,
            'duration': duration,
            'click_a': click_track_a,
            'click_b': click_track_b,
            'instructions': (
                f"Practice singing in {ratio[0]}:{ratio[1]} polyrhythm.\n"
                f"Left ear: {ratio[0]} beats per measure.\n"
                f"Right ear: {ratio[1]} beats per measure.\n"
                "This develops vocal independence and rhythmic precision."
            )
        }


def demo():
    """Demonstrate Vocal Independence Trainer"""
    print("="*60)
    print("VOCAL INDEPENDENCE TRAINER")
    print("BWE + Click Tracks")
    print("="*60)
    
    trainer = VocalIndependenceTrainer(base_frequency=432.0)
    
    # Display brainwave ranges
    print("\nBrainwave Frequency Ranges:")
    for wave_type, (min_freq, max_freq) in trainer.brainwave_ranges.items():
        print(f"  {wave_type.capitalize():6s}: {min_freq:5.1f} - {max_freq:6.1f} Hz")
    
    # Generate scale exercise
    print("\n" + "="*60)
    print("EXERCISE 1: Major Scale with BWE")
    print("="*60)
    
    exercise1 = trainer.generate_vocal_exercise('scale', duration=30.0)
    print(f"\nExercise Type: {exercise1['type']}")
    print(f"Duration: {exercise1['duration']} seconds")
    print(f"Base Frequency: {exercise1['base_frequency']} Hz")
    print(f"\nPitch Sequence:")
    for i, pitch in enumerate(exercise1['pitches']):
        print(f"  Step {i+1}: {pitch:.2f} Hz")
    print(f"\nInstructions:\n{exercise1['instructions']}")
    
    # Generate arpeggio exercise
    print("\n" + "="*60)
    print("EXERCISE 2: Arpeggio with Click Track")
    print("="*60)
    
    exercise2 = trainer.generate_vocal_exercise('arpeggio', duration=20.0)
    print(f"\nExercise Type: {exercise2['type']}")
    print(f"Pitch Sequence:")
    for i, pitch in enumerate(exercise2['pitches']):
        print(f"  Degree {i+1}: {pitch:.2f} Hz")
    print(f"\nInstructions:\n{exercise2['instructions']}")
    
    # Generate polyrhythm exercise
    print("\n" + "="*60)
    print("EXERCISE 3: Polyrhythmic Independence (3:4)")
    print("="*60)
    
    exercise3 = trainer.generate_polyrhythm_exercise((3, 4), duration=20.0)
    print(f"\nPolyrhythm Ratio: {exercise3['ratio'][0]}:{exercise3['ratio'][1]}")
    print(f"Duration: {exercise3['duration']} seconds")
    print(f"\nInstructions:\n{exercise3['instructions']}")
    
    print("\n" + "="*60)
    print("VOCAL INDEPENDENCE TRAINING COMPLETE ✅")
    print("="*60)
    print("\nNote: Audio generation code included but not rendered here.")
    print("To create actual audio files, integrate with audio library (e.g., scipy.io.wavfile)")


if __name__ == "__main__":
    demo()
