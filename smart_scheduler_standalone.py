#!/usr/bin/env python3
"""
Standalone version of the Voice Appointment Scheduler
Optimized for PyInstaller compilation
"""
import sys
import os
import traceback
from pathlib import Path

# Add the current directory to Python path for imports
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import pyttsx3
    except ImportError:
        missing_deps.append("pyttsx3 (text-to-speech)")
    
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("speech_recognition")
    
    try:
        import openai
    except ImportError:
        missing_deps.append("openai")
    
    try:
        import dotenv
    except ImportError:
        missing_deps.append("python-dotenv")
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nThis shouldn't happen in the standalone version.")
        print("Please contact support or rebuild the executable.")
        return False
    
    return True

def check_environment():
    """Check environment setup"""
    env_file = os.path.join(application_path, '.env')
    env_template = os.path.join(application_path, '.env.template')
    
    if not os.path.exists(env_file):
        if os.path.exists(env_template):
            print("⚠️  Configuration needed!")
            print(f"Please rename '.env.template' to '.env' and add your OpenAI API key.")
            print(f"Location: {application_path}")
        else:
            print("⚠️  Missing configuration file!")
            print("Please create a '.env' file with your OpenAI API key:")
            print("OPENAI_API_KEY=your_api_key_here")
        
        input("Press Enter after setting up the configuration file...")
        
        if not os.path.exists(env_file):
            print("❌ Configuration file still not found. Exiting.")
            return False
    
    return True

def main():
    """Main application entry point"""
    print("🎤 Voice Appointment Scheduler")
    print("=" * 40)
    
    try:
        # Check dependencies
        if not check_dependencies():
            input("Press Enter to exit...")
            return
        
        # Check environment
        if not check_environment():
            input("Press Enter to exit...")
            return
        
        # Import and run the scheduler
        from smart_scheduler import SmartAppointmentScheduler
        
        print("✅ All systems ready!")
        print("Starting voice appointment scheduler...\n")
        
        scheduler = SmartAppointmentScheduler()
        scheduler.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        print("\nIf this error persists, please check:")
        print("1. Your microphone is working and permissions are granted")
        print("2. Your speakers/headphones are working")
        print("3. Your internet connection is stable")
        print("4. Your OpenAI API key is valid and has credits")
        
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()