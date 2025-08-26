#!/usr/bin/env python3
"""
Cross-platform build script for Voice Appointment Scheduler
Creates executables for Windows, macOS, and Linux
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def get_platform_info():
    """Get current platform information"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        return "windows", "exe"
    elif system == "darwin":
        return "macos", ""
    elif system == "linux":
        return "linux", ""
    else:
        return "unknown", ""

def create_platform_spec(platform_name, exe_extension):
    """Create platform-specific PyInstaller spec file"""
    
    # Platform-specific hidden imports
    hidden_imports = [
        'pyttsx3.drivers',
        'speech_recognition',
        'openai',
        'dotenv',
        'pyaudio',
    ]
    
    if platform_name == "windows":
        hidden_imports.extend([
            'pyttsx3.drivers.sapi5',
            'win32api',
            'win32com.client',
        ])
    elif platform_name == "macos":
        hidden_imports.extend([
            'pyttsx3.drivers.nsss',
            'AppKit',
        ])
    elif platform_name == "linux":
        hidden_imports.extend([
            'pyttsx3.drivers.espeak',
            'pyttsx3.drivers.festival',
        ])
    
    exe_name = f'VoiceScheduler_{platform_name}'
    if exe_extension:
        exe_name += f'.{exe_extension}'
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['smart_scheduler_standalone.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
    ],
    hiddenimports={hidden_imports},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
    ],
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
    name='{exe_name}',
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
)
'''
    
    spec_filename = f'scheduler_{platform_name}.spec'
    with open(spec_filename, 'w') as f:
        f.write(spec_content)
    
    return spec_filename, exe_name

def build_for_platform():
    """Build executable for current platform"""
    platform_name, exe_ext = get_platform_info()
    
    print(f"🔨 Building for {platform_name}...")
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create platform-specific spec
    spec_file, exe_name = create_platform_spec(platform_name, exe_ext)
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Build executable
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        spec_file
    ])
    
    # Check if build was successful
    exe_path = os.path.join('dist', exe_name)
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✅ Built successfully: {exe_path} ({size_mb:.1f} MB)")
        return exe_path, platform_name
    else:
        print("❌ Build failed!")
        return None, platform_name

def create_release_package(exe_path, platform_name):
    """Create release package with documentation"""
    if not exe_path:
        return
    
    package_name = f"VoiceScheduler_{platform_name}_portable"
    
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    
    os.makedirs(package_name)
    
    # Copy executable
    exe_name = os.path.basename(exe_path)
    shutil.copy2(exe_path, os.path.join(package_name, exe_name))
    
    # Make executable on Unix systems
    if platform_name in ['linux', 'macos']:
        os.chmod(os.path.join(package_name, exe_name), 0o755)
    
    # Create configuration template
    env_content = """# Voice Appointment Scheduler Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional voice settings
VOICE_RATE=150
VOICE_VOLUME=0.9
"""
    
    with open(os.path.join(package_name, '.env.template'), 'w') as f:
        f.write(env_content)
    
    # Create platform-specific instructions
    if platform_name == "windows":
        instructions = """# Voice Appointment Scheduler - Windows

## Setup:
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Rename '.env.template' to '.env'
3. Edit .env and add your API key
4. Double-click VoiceScheduler_windows.exe to run

## Troubleshooting:
- If Windows Defender blocks it, click "More info" → "Run anyway"
- Make sure microphone permissions are enabled
- Check that speakers/headphones are working
"""
    elif platform_name == "macos":
        instructions = """# Voice Appointment Scheduler - macOS

## Setup:
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Rename '.env.template' to '.env'
3. Edit .env and add your API key
4. Right-click the executable → Open (first time only)
5. Grant microphone permissions when prompted

## Troubleshooting:
- If macOS blocks it, go to System Preferences → Security & Privacy
- Enable microphone access for the application
- Make sure audio output is working
"""
    else:  # Linux
        instructions = """# Voice Appointment Scheduler - Linux

## Setup:
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Rename '.env.template' to '.env'
3. Edit .env and add your API key
4. Run: ./VoiceScheduler_linux

## Dependencies:
You may need to install audio libraries:
- Ubuntu/Debian: sudo apt install espeak espeak-data libespeak1 libespeak-dev
- Fedora: sudo dnf install espeak espeak-devel
- Arch: sudo pacman -S espeak

## Troubleshooting:
- Make sure microphone permissions are granted
- Check audio system (PulseAudio/ALSA) is working
- Install missing audio libraries if needed
"""
    
    with open(os.path.join(package_name, 'README.txt'), 'w') as f:
        f.write(instructions)
    
    print(f"📦 Package created: {package_name}/")
    return package_name

def main():
    """Main build process"""
    print("🚀 Voice Appointment Scheduler - Cross-Platform Builder")
    print("=" * 60)
    
    try:
        exe_path, platform_name = build_for_platform()
        
        if exe_path:
            package_name = create_release_package(exe_path, platform_name)
            
            print(f"\n✅ Build completed for {platform_name}!")
            print(f"📁 Portable package: {package_name}")
            print("\n📋 Next steps:")
            print("1. Copy the package folder to any compatible device")
            print("2. Follow the README.txt instructions")
            print("3. Run the executable to start the voice scheduler!")
        else:
            print(f"\n❌ Build failed for {platform_name}")
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()