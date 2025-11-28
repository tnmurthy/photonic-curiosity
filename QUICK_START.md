# Quick Start Guide - Interactive Puzzle Website

## ✅ Font Issue Fixed!

The "junk values" issue has been **fixed**. The system now uses Windows built-in fonts (Nirmala UI) which support Indian languages. You should now see proper Hindi, Tamil, Telugu text!

## 🎮 NEW: Interactive Puzzle Website

I've created a **public-facing website** where users can:
- ✅ Solve Sudoku puzzles online with interactive grid
- ⏱️ Timer to track solve times
- 💡 Hint system (with scoring penalty)
- 🏆 **Global leaderboard** with rankings
- 📊 **Live KPI dashboard** showing stats
- 🎯 Score calculation based on difficulty, time, and hints
- 🌐 Social sharing with custom links

## Running Both Websites

### 1. Admin Dashboard (Already Running)
**Port 5000** - http://localhost:5000
```powershell
python main.py --mode web
```
- Configure social media APIs
- Generate preview puzzles
- View posting history
- Manage settings

### 2. Public Puzzle Website (NEW!)
**Port 5001** - http://localhost:5001

**Open a NEW PowerShell window** and run:
```powershell
cd "c:\Users\Sreepadma Vankadara\.gemini\antigravity\playground\photonic-curiosity"
python public_website.py
```

Then open: **http://localhost:5001**

## Features of the Public Website

### For Users:
1. **Play Puzzles**:
   - Select difficulty (Easy/Medium/Hard)
   - Click "New Game" to start
   - Use number pad or click cells to fill
   - Timer starts automatically

2. **Hint System**:
   - Select a cell
   - Click "💡 Hint" to reveal correct number
   - Each hint reduces your score by 20 points

3. **Check Solution**:
   - Click "✓ Check" when done
   - Submit your name to the leaderboard
   - Get shareable link to brag!

4. **Leaderboard**:
   - View top 10 players
   - Filter by: All Time, Today, Week
   - See rank, score, time, and difficulty
   - Gold/Silver/Bronze medals for top 3

5. **Live Statistics**:
   - Total users who played
   - Total puzzles solved
   - Average solve time
   - Recent activity (last 24h)

### Scoring System:
```
Score = Base Points + Time Bonus - Hint Penalty

Base Points:
- Easy: 100
- Medium: 200
- Hard: 300

Time Bonus: Up to 100 points (faster = more points)
Hint Penalty: -20 points per hint
```

## Social Media Integration

When you post puzzles to social media, the caption now includes:

```
🧩 Medium Sudoku Challenge!

Test your logic and problem-solving skills!

💡 Swipe to see the solution!

🎮 Play online & compete on the leaderboard:
👉 http://localhost:5001

Can you solve it? Share your time in comments! ⏱️

#Sudoku #PuzzleOfTheDay #BrainTeaser...
```

**Important**: Before posting to social media, you should:
1. Deploy the public website to a real domain (not localhost)
2. Update the website URL in the config

## Data Storage

All user data is stored in:
- `data/leaderboard.json` - Top 100 scores
- `data/user_stats.json` - Per-user statistics

## Next Steps

1. **Test the public website**: http://localhost:5001
   - Play a few puzzles
   - Submit scores with different names
   - View the leaderboard populate

2. **Test preview generation** at http://localhost:5000
   - Should now show proper Hindi/Tamil/Telugu text
   - No more junk characters!

3. **Deploy to production** (when ready):
   - Host the public website on a domain
   - Update website URL in config
   - Enable social media posting

## Troubleshooting

### If Indian text still shows incorrectly:
Windows should have Nirmala UI font by default. If not:
1. Go to Windows Settings > Time & Language > Language
2. Add Hindi/Tamil/Telugu languages
3. Windows will install the fonts automatically

### If port 5001 is busy:
Edit `public_website.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Changed port
```

## What You Have Now

✅ **Admin Dashboard** (Port 5000)
- Generate puzzles
- Configure social media
- Post to platforms
- View history

✅ **Public Website** (Port 5001)
- Interactive Sudoku solver
- Real-time timer
- Hint system
- Global leaderboard with rankings
- KPI dashboard
- Social sharing

✅ **Auto-posting** system (when configured)
- Twice daily posts
- Multiple languages
- Includes website link
- Trending hashtags

🎉 **You're ready to launch!**
