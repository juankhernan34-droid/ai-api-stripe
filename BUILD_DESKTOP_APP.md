# Build Desktop App (.exe)

This guide shows how to convert `desktop_app.py` into a standalone Windows executable.

## Prerequisites

Make sure you have Python 3.9+ installed.

## Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

## Step 2: Build the Executable

Run this command in the repo directory:

```bash
pyinstaller --onefile --windowed --icon=rocket.ico --name="AI_API_Stripe" desktop_app.py
```

**What this does:**
- `--onefile`: Creates a single `.exe` file (not a folder)
- `--windowed`: Removes the console window (GUI only)
- `--icon=rocket.ico`: Adds an icon to the app
- `--name="AI_API_Stripe"`: Names the executable

## Step 3: Find Your .exe

After building, your executable will be in:
```
dist/AI_API_Stripe.exe
```

## Step 4: Run It! 🚀

Double-click `AI_API_Stripe.exe` and you're done!

---

## Alternative: Quick Build (No Icon)

If you don't have an icon file, use:

```bash
pyinstaller --onefile --windowed --name="AI_API_Stripe" desktop_app.py
```

---

## What the App Does

1. ✅ **Enter Credentials** - HF Token, Stripe Keys, Price IDs
2. ✅ **One Click Deploy** - Saves `.env` and prepares for HF Spaces
3. ✅ **Run Locally** - Start your API on `http://localhost:7860`

---

## Troubleshooting

**Issue: "pyinstaller not found"**
```bash
pip install --upgrade pyinstaller
```

**Issue: `.exe` is too large**
Try UPX compression:
```bash
pyinstaller --onefile --windowed -w desktop_app.py --upx-dir=/path/to/upx
```

**Issue: App won't run**
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Distribution

Once you have `AI_API_Stripe.exe`, you can:
- ✅ Share it with others
- ✅ Put it on your website for download
- ✅ Run it anywhere on Windows (no Python needed!)

Enjoy! 🎉
