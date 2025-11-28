# GitHub Actions & Pages Setup Guide

## What Was Set Up

✅ **GitHub Actions Workflow** (`.github/workflows/deploy.yml`)
- Runs tests on every push
- Generates a new daily puzzle 
- Deploys to GitHub Pages
- Runs automatically every day at midnight UTC (5:30 AM IST)

✅ **Test Suite** (`tests/test_basic.py`)
- Tests puzzle generation
- Tests localization system

✅ **Static Site Generator** (`scripts/generate_static.py`)
- Generates a playable daily puzzle
- Embeds puzzle data into HTML
- Rotates difficulty daily (Easy → Medium → Hard)

✅ **Static HTML Template** (`templates/static_puzzle.html`)
- Fully playable Sudoku interface
- No backend required
- Timer, number pad, solution checking

## How to Deploy

### Step 1: Push to GitHub

If you haven't already created a GitHub repository:

1. Go to https://github.com/new
2. Create a new repository (name it anything, e.g., "sudoku-automation")
3. **Don't** initialize with README (you already have files)

Then run these commands in your terminal:

```powershell
cd "c:\Users\Sreepadma Vankadara\.gemini\antigravity\playground\photonic-curiosity"

# Add all new files
git add .

# Commit the changes
git commit -m "Add GitHub Actions and Pages support"

# Connect to your GitHub repo (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under "Source", select: **Deploy from a branch**
5. Under "Branch", select: **gh-pages** → **/ (root)** → Save

### Step 3: Wait for Deployment

1. Go to the **Actions** tab in your repo
2. You'll see the workflow running
3. Wait for it to complete (takes ~1-2 minutes)
4. Once done, your site will be live at:
   ```
   https://YOUR_USERNAME.github.io/YOUR_REPO/
   ```

## What Happens Next

### Automatic Daily Updates
- Every day at midnight UTC (5:30 AM IST), GitHub Actions will:
  1. Generate a new puzzle (difficulty rotates)
  2. Deploy the updated site
  3. Your users get a fresh puzzle daily!

### On Every Code Push
- When you push code changes, it will:
  1. Run tests to ensure nothing broke
  2. Generate and deploy a new puzzle
  3. Update the live site

## Testing Locally

Before pushing, you can test the static site generator:

```powershell
python scripts/generate_static.py
```

This creates `public/index.html`. Open it in your browser to test!

## Manual Deployment

You can also trigger a deployment manually:
1. Go to **Actions** tab on GitHub
2. Click "Daily Sudoku CI/CD"
3. Click "Run workflow" → "Run workflow"

## Customization

### Change the Schedule
Edit `.github/workflows/deploy.yml`:
```yaml
schedule:
  - cron: '0 12 * * *'  # Run at noon UTC instead
```

### Change Difficulty Rotation
Edit `scripts/generate_static.py` - change the rotation logic.

## Troubleshooting

### "Page not found" error
- Make sure you selected `gh-pages` branch in Settings → Pages
- Wait 2-3 minutes after the workflow completes
- Check the Actions tab for any errors

### Workflow fails
- Check the Actions tab for error logs
- Common issue: Python dependencies not installing
- Solution: The workflow installs minimal deps (numpy, Pillow, pyyaml)

### Want to use a custom domain?
In Settings → Pages, you can add your own domain!

## What's Different from the Full App

**Static Version (GitHub Pages):**
- ✅ Play daily puzzles
- ✅ Timer and number pad
- ✅ Solution checking
- ❌ No leaderboard (no database)
- ❌ No "New Puzzle" button (updates daily)
- ❌ No multi-language support yet (can be added)

**Full App (localhost:5001):**
- ✅ Generate puzzles on-demand
- ✅ Full leaderboard with rankings
- ✅ Multi-language support
- ✅ KPI dashboard
- ✅ Social sharing

## Next Steps

1. **Push to GitHub** → Get your public link
2. **Share the link** on social media
3. **Keep the full app running locally** for the admin dashboard and social media posting schedule
4. **Update social media captions** to use your GitHub Pages URL instead of localhost

Your GitHub Pages URL will be the public-facing version where everyone can play, while you use the local app to manage posting!

---

🎉 **You're all set!** Push to GitHub and your daily Sudoku site will be live!
