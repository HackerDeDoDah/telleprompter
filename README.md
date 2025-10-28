# Teleprompter (Tkinter)

A small, cross-platform teleprompter written in Python using Tkinter.

Features
- Load or paste text
- Start / Pause scrolling
- Speed and font-size controls
- Fullscreen mode
- Mirror mode (reverses characters per line for reflecting setups)
- Keyboard shortcuts: Space, F11, Up/Down, +/-, M

Requirements
- Python 3.7+ (Tkinter is included with standard CPython on Windows)

Files
- `teleprompter.py` — main program
- `sample_script.txt` — example content

Pillow (optional)
------------------
For true mirror (horizontally flipped) rendering, install Pillow. On Windows:

```powershell
pip install Pillow
```

If Pillow is not installed the app will fall back to a simple character-reverse mirror mode.

Quick start (PowerShell)

```powershell
# Move to project directory
cd 'C:\Users\monke\OneDrive\Desktop\telleprompter'

# Run the teleprompter (Windows)
python teleprompter.py
```

Installer
---------
You can create a Windows installer (single EXE) using Inno Setup.

1. Build the application first (produces `dist\teleprompter.exe`). See `build.ps1`.
2. Install Inno Setup: https://jrsoftware.org/isinfo.php
3. Run the included script to compile the installer:

```powershell
cd 'C:\Users\monke\OneDrive\Desktop\telleprompter'
.\make_installer.ps1
```

This runs `ISCC.exe` on `installer.iss` and produces `teleprompter_installer.exe`.

Usage notes
- Click Open to load a .txt file, or Edit to paste text directly.
- Start with the Start button or press Space.
- Use F11 to toggle fullscreen.
- Mirror reverses characters on each line (simple method that works without extra libraries).

Next steps / improvements
- Add smooth variable-timing scrolling based on words-per-minute
- Add text-to-image rendering to support true mirror (requires Pillow)
- Persist settings between runs

If you want any of those improvements, tell me which and I can add them.