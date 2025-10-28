# Teleprompter (Tkinter)

A lightweight teleprompter application written in Python and Tkinter. It's designed to be simple to run on Windows and Linux and easy to customize.

What this repo contains
- `teleprompter.py` — main program (Tkinter GUI)
- `sample_script.txt` — example text to try
- `requirements.txt` — external package list (empty by default)

Features
- Load or paste text via the Edit window
- Start / Pause scrolling (Start button or Space)
- Speed and font-size controls (sliders + keyboard shortcuts)
- Fullscreen mode (F11)
- Styling controls: choose text color, choose background color, optional drop-shadow
- Per-line rendering with a bottom progress bar
- Keyboard shortcuts: Space (start/pause), Up/Down (speed), +/- (font size), F11 (fullscreen)

Requirements
- Python 3.7+ (Tkinter is included with standard CPython on Windows)

Quick start (PowerShell)

```powershell
cd 'C:\Users\Path_to_your_folder\telleprompter'
python teleprompter.py
```

Usage notes
- Click Open to load a `.txt` file, or Edit to paste/modify the text directly.
- Use the Speed and Font sliders to tune scrolling and readability.
- Use Text Color / BG Color to style the display for your lighting and camera.

Notes & next steps
- The project intentionally avoids optional image-based mirroring; the current mirror feature was removed to keep the app simple and dependency-free.
- If you want advanced features (WPM-based scrolling, persistent settings, installer, or a true mirrored output using Pillow), I can add them on request.

If you'd like an installer or a packaged exe, tell me whether you want an Inno Setup installer or a simpler portable ZIP and I will prepare it.