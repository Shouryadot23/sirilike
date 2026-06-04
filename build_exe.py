#!/usr/bin/env python3
"""
Build script to create a standalone .exe using PyInstaller.

Usage:
    pip install pyinstaller
    python build_exe.py

The .exe will be created in the 'dist/' folder.
"""

import subprocess
import sys

def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                # Single .exe file
        "--name", "SiriLike",       # Name of the exe
        "--console",                # Show console window
        "--add-data", "assistant;assistant",  # Include assistant package
        "main.py"
    ]

    print("\n🔨 Building SiriLike.exe ...\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅ Build successful!")
        print("📁 Your .exe is at: dist/SiriLike.exe")
    else:
        print("\n❌ Build failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    build()
