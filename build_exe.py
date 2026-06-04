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
        "--windowed",               # No console window (clean GUI)
        "--add-data", "assistant;assistant",  # Include assistant package
        # Exclude heavy/unnecessary packages that cause build errors
        "--exclude-module", "tensorflow",
        "--exclude-module", "torch",
        "--exclude-module", "keras",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "matplotlib",
        "--exclude-module", "scipy",
        "--exclude-module", "sklearn",
        "--exclude-module", "PIL",
        "--exclude-module", "cv2",
        "--exclude-module", "IPython",
        "--exclude-module", "jupyter",
        "--exclude-module", "notebook",
        "--exclude-module", "pytest",
        "--exclude-module", "setuptools",
        "--exclude-module", "pkg_resources",
        "main_gui.py"
    ]

    print("\n\U0001f528 Building SiriLike.exe (GUI Edition) ...\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n\u2705 Build successful!")
        print("\U0001f4c1 Your .exe is at: dist/SiriLike.exe")
    else:
        print("\n\u274c Build failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    build()
