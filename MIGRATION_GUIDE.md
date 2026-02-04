# Migration Guide: Upgrading to Sudoku v2.0

## 🎯 Overview

This guide helps you migrate from the original Sudoku system to v2.0 with variations support and production-ready features.

---

## 📋 Pre-Migration Checklist

- [ ] **Backup your data**
  ```bash
  cp -r data data_backup_$(date +%Y%m%d)
  cp config.yaml config.yaml.backup
  ```

- [ ] **Test current system**
  - Verify current functionality works
  - Export any important data
  - Document custom configurations

- [ ] **Review new features**
  - Read IMPLEMENTATION_SUMMARY.md
  - Review QUICK_START.md
  - Check PRODUCTION_DEPLOYMENT.md

---

## 🔄 Migration Steps

### Step 1: Install New Dependencies

```bash
# Backup old requirements
cp requirements.txt requirements.txt.old

# Install new production requirements
pip install -r requirements_production.txt
```

### Step 2: Add New Files

Copy these new files to your project:

```bash
# Core modules
sudoku_variations.py       # NEW: Variation engine
variation_renderer.py      # NEW: Enhanced renderer
production_config.py       # NEW: Production config manager
enhanced_api.py           # REPLACES: public_website.py

# Frontend
templates/puzzle_variations.html  # NEW: Enhanced UI

# Documentation
PRODUCTION_DEPLOYMENT.md
IMPLEMENTATION_SUMMARY.md
QUICK_START.md
```

### Step 3: Update Existing Files

#### **Option A: Fresh Start (Recommended)**
```bash
# Rename old files
mv public_website.py public_website.py.old
mv puzzle_renderer.py puzzle_renderer.py.old

# Use new files
cp enhanced_api.py public_website.py  # Or keep as enhanced_api.py
```

#### **Option B: Gradual Migration**
Keep both systems running:
```bash
# Old system on port 5001
python public_website.py

# New system on port 5002
PORT=5002 python enhanced_api.py
```

### Step 4: Update Configuration

Create or update `.env` file:
```bash
# Required for new system
SECRET_KEY=generate-a-random-32-char-key-here
FLASK_DEBUG=False
WEBSITE_URL=http://localhost:5001

# Optional: Keep existing credentials
# (They'll be loaded automatically)
```

Validate configuration:
```python
from production_config import ProductionConfigManager

config = ProductionConfigManager()
is_valid, errors = config.validate()

if not is_valid:
    print("Configuration errors:", errors)
else:
    print("Configuration is valid!")
```

### Step 5: Migrate Data

The new system is backward compatible with existing data:

```python
# Optional: Add variation fields to existing leaderboard entries
import json

with open('data/leaderboard.json', 'r') as f:
    leaderboard = json.load(f)

for entry in leaderboard:
    if 'variation_type' not in entry:
        entry['variation_type'] = 'classic'
    if 'theme' not in entry:
        entry['theme'] = 'default'

with open('data/leaderboard.json', 'w') as f:
    json.dump(leaderboard, f, indent=2)
```

### Step 6: Test New System

```bash
# Start enhanced API
python enhanced_api.py

# In another terminal, run tests
python test_suite.py
```

Expected output:
```
✅ PASS | Health endpoint responds
✅ PASS | Variations endpoint responds
✅ PASS | Classic easy puzzle
...
🎉 ALL TESTS PASSED! 🎉
```

### Step 7: Update Frontend

Replace or update your `puzzle.html`:

```html
<!-- Add variation selector before difficulty selector -->
<div class="variation-selector">
    <h3>Choose Your Puzzle Style</h3>
    <select id="variationType" onchange="updateVariationUI()">
        <option value="classic">Classic</option>
        <option value="emoji">Emoji</option>
        <option value="color">Color</option>
        <option value="symbol">Symbol</option>
    </select>
</div>
```

Or use the complete new template:
```bash
cp templates/puzzle_variations.html templates/puzzle.html
```

---

## 🔍 What Changed?

### API Endpoints (Backward Compatible)

**Existing endpoints still work:**
- ✅ `POST /api/new-puzzle` - Now supports `variation_type` and `theme` parameters
- ✅ `POST /api/validate-solution` - Works with both numbers and symbols
- ✅ `POST /api/submit-score` - Now tracks variation type
- ✅ `GET /api/leaderboard` - Shows variation badges
- ✅ `GET /api/kpi` - Includes variation statistics

**New endpoints:**
- 🆕 `GET /api/variations/available` - List all variations
- 🆕 `POST /api/get-hint` - Dedicated hint endpoint
- 🆕 `GET /health` - Health check endpoint

### Request/Response Changes

**Old Request:**
```json
POST /api/new-puzzle
{
  "difficulty": "medium",
  "language": "en"
}
```

**New Request (Backward Compatible):**
```json
POST /api/new-puzzle
{
  "difficulty": "medium",
  "variation_type": "emoji",  // OPTIONAL (defaults to "classic")
  "theme": "animals",         // OPTIONAL (random if not specified)
  "language": "en"
}
```

**Enhanced Response:**
```json
{
  "success": true,
  "puzzle": [[...]],
  "symbols": ["🐶", "🐱", ...],  // NEW
  "variation_info": {            // NEW
    "description": "...",
    "target_audience": "...",
    "difficulty_modifier": 0.9
  }
}
```

### Data Structure Changes

**Leaderboard entries now include:**
```json
{
  "username": "Player1",
  "score": 285,
  "difficulty": "medium",
  "variation_type": "emoji",  // NEW (defaults to "classic")
  "theme": "animals",         // NEW
  "time": 245,
  "hints_used": 2,
  "timestamp": "2025-02-04T10:30:00",
  "date": "2025-02-04"
}
```

**User stats now include:**
```json
{
  "Player1": {
    "total_puzzles": 15,
    "total_score": 3500,
    "best_score": 385,
    "puzzles_by_difficulty": {...},
    "puzzles_by_variation": {   // NEW
      "classic": 10,
      "emoji": 3,
      "color": 2
    },
    "average_time": 280
  }
}
```

---

## ⚠️ Breaking Changes

### Minimal Breaking Changes
Most changes are **additive**, not breaking. However:

1. **Configuration System**
   - Old: Direct YAML loading
   - New: ProductionConfigManager with validation
   - **Fix**: Update config loading code or use legacy mode

2. **Error Responses**
   - Old: Inconsistent error formats
   - New: Standardized `{success: false, error: "message"}`
   - **Fix**: Update error handling in frontend

3. **Session Management**
   - Old: Basic session
   - New: Secure session with SECRET_KEY
   - **Fix**: Set SECRET_KEY in environment

---

## 🧪 Testing Migration

### 1. Verify Old Functionality
```bash
# Test classic puzzles still work
curl -X POST http://localhost:5001/api/new-puzzle \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"medium"}'
```

### 2. Test New Features
```bash
# Test variations
curl -X POST http://localhost:5001/api/new-puzzle \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"easy","variation_type":"emoji","theme":"animals"}'
```

### 3. Verify Data Integrity
```python
import json

# Check leaderboard loads
with open('data/leaderboard.json') as f:
    leaderboard = json.load(f)
    print(f"Leaderboard entries: {len(leaderboard)}")

# Check user stats loads
with open('data/user_stats.json') as f:
    stats = json.load(f)
    print(f"User count: {len(stats)}")
```

---

## 🚀 Post-Migration Steps

### 1. Enable New Features

Update your frontend to show variations:
```html
<button onclick="selectVariation('emoji')">
  Try Emoji Sudoku! 🎮
</button>
```

### 2. Announce to Users

Example announcement:
```
🎉 NEW! Sudoku Variations!

We've added 6 exciting puzzle types:
• 🎮 Emoji Sudoku (8 fun themes!)
• 🌈 Color Sudoku
• ⚡ Symbol Sudoku
• 🎨 Picture Sudoku
• 👶 Kids Sudoku
• 🔢 Classic Sudoku

Try them now at [your-url]!
```

### 3. Monitor Performance

```bash
# Watch logs
tail -f logs/sudoku.log

# Check for errors
grep ERROR logs/sudoku.log

# Monitor health
watch -n 5 'curl -s http://localhost:5001/health | jq'
```

### 4. Gradual Rollout

Week 1: Enable Classic + Emoji
Week 2: Add Color + Symbol
Week 3: Add Picture + Kids
Week 4: Full launch with all variations

---

## 🔧 Rollback Plan

If issues occur, rollback quickly:

```bash
# Stop new system
pkill -f enhanced_api.py

# Restore old files
mv public_website.py.old public_website.py
mv puzzle_renderer.py.old puzzle_renderer.py

# Restore old data (if needed)
cp -r data_backup_YYYYMMDD/* data/

# Restart old system
python public_website.py
```

---

## 📊 Migration Checklist

- [ ] Old system backed up
- [ ] New dependencies installed
- [ ] New files added to project
- [ ] Configuration validated
- [ ] Data migration completed (if needed)
- [ ] Tests passing
- [ ] Frontend updated
- [ ] Production deployment planned
- [ ] Monitoring configured
- [ ] Rollback plan documented
- [ ] Team trained on new features

---

## 🆘 Troubleshooting

### Issue: Import errors
```
ModuleNotFoundError: No module named 'sudoku_variations'
```
**Fix**: Ensure `sudoku_variations.py` is in the same directory as `enhanced_api.py`

### Issue: Configuration validation fails
```
Configuration validation failed: Invalid timezone
```
**Fix**: Install pytz: `pip install pytz`

### Issue: Emoji not displaying
```
Emojis show as boxes or question marks
```
**Fix**: Ensure your terminal/browser supports UTF-8 encoding

### Issue: Session errors
```
KeyError: 'current_puzzle'
```
**Fix**: Set SECRET_KEY in environment variables

---

## 📞 Support

If you encounter issues:

1. Check logs: `logs/sudoku.log`
2. Review documentation: `PRODUCTION_DEPLOYMENT.md`
3. Run test suite: `python test_suite.py`
4. Verify configuration: Check `.env` file

---

## ✅ Success Criteria

Migration is successful when:
- [ ] All existing features work
- [ ] At least 1 new variation works
- [ ] All tests pass
- [ ] No data loss
- [ ] Performance is maintained or improved
- [ ] Users can access the system

---

**Estimated Migration Time**: 30-60 minutes for basic setup, 2-4 hours for full production deployment.

**Good luck with your migration! 🚀**
