#!/usr/bin/env python3
"""
Example usage of ai_vocal_coach.py
Demonstrates different training session configurations
"""

# NOTE: This is an example file. To run, first install dependencies:
#   pip install -r requirements.vocal.txt

from ai_vocal_coach import build_session

def basic_session():
    """Generate a basic training session"""
    print("🎯 Generating basic session...")
    build_session(session_id=1)

def custom_prompt_session():
    """Generate session with custom coaching text"""
    print("🎯 Generating custom prompt session...")
    build_session(
        session_id=2,
        text_prompt="Focus on deep chest vibration. Feel the resonance at your sternum. Sync with the beat.",
        target_hz=110
    )

def progressive_sessions():
    """Generate progressive training sessions 1-5"""
    print("🎯 Generating progressive training series (Sessions 1-5)...")
    frequencies = {
        1: 100,   # Alpha baseline
        2: 110,   # Low chest
        3: 120,   # Mid chest
        4: 130,   # Upper chest
        5: 140    # Head voice transition
    }
    
    for session_id, hz in frequencies.items():
        print(f"\n📊 Session {session_id}: Target {hz}Hz")
        build_session(
            session_id=session_id,
            text_prompt=f"Deep resonance training. Target frequency: {hz} Hertz. Maintain steady pitch.",
            target_hz=hz
        )

def trig6_sessions():
    """Generate TRIG6 frequency mapped sessions"""
    print("🎯 Generating TRIG6 frequency sessions...")
    trig6_map = {
        10: 100,   # Alpha wave baseline
        11: 105,
        12: 110,
        13: 115,
        14: 120,
        15: 125,
    }
    
    for session_id, hz in trig6_map.items():
        build_session(
            session_id=session_id,
            text_prompt=f"TRIG6 Session {session_id}. Resonance target: {hz}Hz. Deep independence training.",
            target_hz=hz
        )

if __name__ == "__main__":
    print("🔥 AI Vocal Coach - Example Usage\n")
    print("Choose a training mode:")
    print("1. Basic session (default)")
    print("2. Custom prompt session")
    print("3. Progressive sessions (1-5)")
    print("4. TRIG6 frequency sessions\n")
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            basic_session()
        elif choice == "2":
            custom_prompt_session()
        elif choice == "3":
            progressive_sessions()
        elif choice == "4":
            trig6_sessions()
        else:
            print("Invalid choice, running basic session...")
            basic_session()
            
        print("\n✅ Training sessions generated!")
        print("📁 Check the 'ai_vocal_sessions' directory for output files")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("💡 Install dependencies first: pip install -r requirements.vocal.txt")
    except Exception as e:
        print(f"\n❌ Error generating sessions: {e}")
        print("💡 Ensure TTS is properly installed and models are available")
    except KeyboardInterrupt:
        print("\n\n👋 Session generation cancelled")
