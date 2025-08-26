#!/usr/bin/env python3
"""
Build script to create standalone executable for the Voice Appointment Scheduler
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['smart_scheduler.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'pyttsx3.drivers.nsss',
        'pyttsx3.drivers.espeak',
        'speech_recognition',
        'openai',
        'dotenv',
        'pyaudio',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoiceAppointmentScheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('scheduler.spec', 'w') as f:
        f.write(spec_content)
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the standalone executable"""
    print("Building standalone executable...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Build using spec file
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller", 
        "--clean", 
        "scheduler.spec"
    ])
    
    print("✓ Executable built successfully!")
    
    # Show output location
    if sys.platform.startswith('win'):
        exe_path = "dist/VoiceAppointmentScheduler.exe"
    else:
        exe_path = "dist/VoiceAppointmentScheduler"
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✓ Executable created: {exe_path} ({size_mb:.1f} MB)")
        return exe_path
    else:
        print("❌ Executable not found!")
        return None

def create_distribution_package(exe_path):
    """Create a distribution package with necessary files"""
    if not exe_path or not os.path.exists(exe_path):
        return
    
    dist_dir = "VoiceScheduler_Portable"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir)
    
    # Copy executable
    exe_name = os.path.basename(exe_path)
    shutil.copy2(exe_path, os.path.join(dist_dir, exe_name))
    
    # Create .env template
    env_template = """# Voice Appointment Scheduler Configuration
# Copy this file to .env and add your OpenAI API key

OPENAI_API_KEY=your_openai_api_key_here

# Voice Settings (optional)
VOICE_RATE=150
VOICE_VOLUME=0.9
"""
    
    with open(os.path.join(dist_dir, '.env.template'), 'w') as f:
        f.write(env_template)
    
    # Create setup instructions
    setup_instructions = """# Voice Appointment Scheduler - Portable Version

## Quick Setup:

1. Get your OpenAI API key from: https://platform.openai.com/api-keys

2. Rename '.env.template' to '.env' and add your API key:
   OPENAI_API_KEY=your_actual_api_key_here

3. Run the executable:
   - Windows: Double-click VoiceAppointmentScheduler.exe
   - Mac/Linux: ./VoiceAppointmentScheduler

## System Requirements:
- Microphone for voice input
- Speakers/headphones for voice output
- Internet connection for ChatGPT API

## Troubleshooting:
- If microphone doesn't work, check system permissions
- If voice output doesn't work, check audio settings
- Make sure your OpenAI API key is valid and has credits

## Available Doctors:
- Dr. Ali (General Medicine): Mon, Wed, Fri (9 AM - 5 PM)
- Dr. Sara (Pediatrics): Tue, Thu (10 AM - 6 PM)
- Dr. John (Cardiology): Sat, Sun (9 AM - 1 PM)

Say "exit" or "quit" to end the session.
"""
    
    with open(os.path.join(dist_dir, 'README.txt'), 'w') as f:
        f.write(setup_instructions)
    
    print(f"✓ Distribution package created: {dist_dir}/")
    print(f"  - Executable: {exe_name}")
    print(f"  - Configuration template: .env.template")
    print(f"  - Setup instructions: README.txt")

def main():
    """Main build process"""
    print("🚀 Building Voice Appointment Scheduler Executable")
    print("=" * 50)
    
    try:
        # Install PyInstaller
        install_pyinstaller()
        
        # Create spec file
        create_spec_file()
        
        # Build executable
        exe_path = build_executable()
        
        # Create distribution package
        create_distribution_package(exe_path)
        
        print("\n✅ Build completed successfully!")
        print("\nNext steps:")
        print("1. Copy the 'VoiceScheduler_Portable' folder to any device")
        print("2. Follow the README.txt instructions to set up your API key")
        print("3. Run the executable to start scheduling appointments!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()