# Quick Setup Guide - Getting Started

## The Issue

You're seeing `ERR_CONNECTION_REFUSED` because **Python is not installed** on your system. The web server can't start without Python.

## Solution: Install Python

### Option 1: Install from Python.org (Recommended)

1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.12.x" (latest version)
   - **Important**: During installation, CHECK ✅ "Add Python to PATH"

2. **Verify Installation**:
   Open a new PowerShell window and run:
   ```powershell
   python --version
   ```
   You should see: `Python 3.12.x`

### Option 2: Install from Microsoft Store (Easier)

1. Open Microsoft Store
2. Search for "Python 3.12"
3. Click "Get" or "Install"
4. Wait for installation to complete

## After Installing Python

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
cd "c:\Users\Sreepadma Vankadara\.gemini\antigravity\playground\photonic-curiosity"
pip install -r requirements.txt
```

### Step 2: Start the Web Application

```powershell
python main.py --mode web
```

You should see:
```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Go to: **http://localhost:5000**

---

## Quick Test Without Installation

If you want to test immediately without setting up the full environment, you can use the **standalone version** I can create that doesn't require dependencies.

Would you like me to:
1. Wait for you to install Python (recommended for full features)
2. Create a simplified standalone version that works immediately

---

## Troubleshooting

### If `pip install` fails:

Try:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### If port 5000 is busy:

Change the port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changed to 8080
```

Then access at: http://localhost:8080

### If you see "Module not found" errors:

Make sure you're in the correct directory:
```powershell
cd "c:\Users\Sreepadma Vankadara\.gemini\antigravity\playground\photonic-curiosity"
```

---

## What Happens After It Starts

Once the server is running:
1. **Dashboard** shows system status
2. **Configuration** tab lets you add social media API credentials
3. **Preview & Test** generates sample puzzles
4. **History** shows all posts (demo mode saves locally)

**Demo mode is enabled by default** - it won't post to social media until you configure APIs and disable demo mode.

---

## Next Steps After Installation

1. Install Python (5 minutes)
2. Install dependencies (2 minutes)
3. Start the server (instant)
4. Configure your settings in the web UI
5. Test with preview generation
6. When ready, add social media credentials and start posting!

Let me know if you need help with any of these steps!
