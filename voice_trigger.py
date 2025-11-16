#!/usr/bin/env python3
# voice_trigger.py  
# REFLEXSHELL BRAIN v1 — Voice-Activated Cognitive Environment
# Strategickhaos DAO LLC — "Hey Baby, show me the empire" → Full Neural Activation

import speech_recognition as sr
import subprocess
import os
import time
from pathlib import Path

class VoiceCognitiveTrigger:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.trigger_phrases = {
            'show me the empire': self.activate_full_empire,
            'cognitive bootstrap': self.bootstrap_brain,
            'thread status': self.show_thread_status,
            'sovereignty mode': self.activate_sovereignty_mode,
            'neural map': self.render_cognitive_map,
            'sleep mode': self.enter_sleep_mode
        }
        
    def listen_for_trigger(self):
        """Continuously listen for voice triggers"""
        print("🎤 Voice trigger active - Say: 'Hey Baby, show me the empire'")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
        while True:
            try:
                with self.microphone as source:
                    print("🔊 Listening...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"🎯 Heard: {command}")
                    
                    # Check for trigger phrases
                    for phrase, action in self.trigger_phrases.items():
                        if phrase in command:
                            print(f"✅ Trigger detected: {phrase}")
                            action()
                            break
                            
                except sr.UnknownValueError:
                    pass  # Ignore unrecognized speech
                    
            except sr.WaitTimeoutError:
                pass  # Continue listening
            except KeyboardInterrupt:
                print("\n👋 Voice trigger deactivated")
                break
                
    def activate_full_empire(self):
        """Full empire visualization activation"""
        print("🏛️ ACTIVATING FULL EMPIRE VIEW")
        
        # Launch cognitive environment
        subprocess.Popen(['python3', 'reflexshell_layout.py'])
        time.sleep(2)
        
        # Render cognitive map
        self.render_cognitive_map()
        
        # Launch thread manager
        subprocess.Popen(['bash', 'thread_manager.sh'])
        
        # Open strategic overview
        if os.path.exists('dao_record_v1.0.yaml'):
            subprocess.Popen(['code', 'dao_record_v1.0.yaml'])
            
        print("🎯 FULL EMPIRE: ONLINE")
        
    def bootstrap_brain(self):
        """Bootstrap cognitive environment"""
        print("🧠 COGNITIVE BOOTSTRAP INITIATED")
        subprocess.Popen(['python3', 'reflexshell_layout.py'])
        
    def show_thread_status(self):
        """Display current thread status"""
        print("📊 THREAD STATUS:")
        if os.path.exists('cognitive_thread_status.json'):
            subprocess.Popen(['cat', 'cognitive_thread_status.json'])
        else:
            print("❌ No active threads detected")
            
    def activate_sovereignty_mode(self):
        """Activate full sovereignty mode"""
        print("👑 SOVEREIGNTY MODE: ACTIVATED")
        
        # Launch all sovereignty components
        commands = [
            ['docker', 'compose', 'up', '-d'],
            ['python3', 'reflexshell_layout.py'],
            ['bash', 'thread_manager.sh']
        ]
        
        for cmd in commands:
            subprocess.Popen(cmd)
            time.sleep(1)
            
    def render_cognitive_map(self):
        """Render and display cognitive architecture map"""
        print("🗺️ RENDERING COGNITIVE MAP")
        
        if os.path.exists('cognitive_map.dot'):
            # Render SVG
            subprocess.run(['dot', '-Tsvg', 'cognitive_map.dot', '-o', 'cognitive_architecture.svg'])
            print("✅ Cognitive map rendered: cognitive_architecture.svg")
            
            # Try to open with default viewer
            try:
                subprocess.Popen(['xdg-open', 'cognitive_architecture.svg'])  # Linux
            except FileNotFoundError:
                try:
                    subprocess.Popen(['open', 'cognitive_architecture.svg'])  # Mac
                except FileNotFoundError:
                    print("💡 Manual open required: cognitive_architecture.svg")
        else:
            print("❌ cognitive_map.dot not found")
            
    def enter_sleep_mode(self):
        """Enter sleep mode - shut down non-essential processes"""
        print("💤 ENTERING SLEEP MODE")
        
        # Log sleep mode activation
        with open('sleep_mode.log', 'w') as f:
            f.write(f"Sleep mode activated: {time.ctime()}\n")
            
        print("😴 Sleep mode activated - Voice trigger remains active")
        
if __name__ == '__main__':
    try:
        trigger = VoiceCognitiveTrigger()
        trigger.listen_for_trigger()
    except ImportError:
        print("❌ speech_recognition not installed")
        print("💡 Install with: pip install SpeechRecognition pyaudio")