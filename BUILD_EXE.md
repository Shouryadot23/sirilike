# 🔨 Building the .exe

Follow these steps to create a standalone `SiriLike.exe`:

## 1. Install dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

## 2. Build the exe
```bash
python build_exe.py
```

## 3. Run it
```bash
cd dist
SiriLike.exe
```

The `.exe` will be in the `dist/` folder. You can share it with anyone — no Python installation needed on their machine!

> **Note:** The exe runs in **text mode** by default. For voice mode, just double-click it — it will use your microphone.

> **Note (Windows):** If you get antivirus warnings, it's a false positive common with PyInstaller. You can whitelist the file.
