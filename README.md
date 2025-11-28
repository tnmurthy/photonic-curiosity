# Sudoku Automation System 🧩

[![Daily Sudoku CI/CD](https://github.com/tnmurthy/photonic-curiosity/actions/workflows/deploy.yml/badge.svg)](https://github.com/tnmurthy/photonic-curiosity/actions/workflows/deploy.yml)


Automated system to generate 9x9 Sudoku puzzles in three difficulty levels and post them twice daily to social media platforms with trending hashtags in Indian languages.

## Features

- **Sudoku Generation**: Production-grade puzzle generator with 3 difficulty levels (Easy, Medium, Hard)
- **Multi-Language Support**: Full support for 10 Indian languages:
  - English, Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Bengali (বাংলা)
  - Marathi (मराठी), Gujarati (ગુજરાતી), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ)
- **Beautiful Image Rendering**: Modern dark-themed puzzle images optimized for social media
- **Automated Scheduling**: Post twice daily with difficulty rotation
- **Multi-Platform Support**: Instagram, Twitter/X, Facebook, Reddit
- **Web Dashboard**: Beautiful configuration interface and monitoring
- **Demo Mode**: Test the system without posting to social media

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Dashboard

```bash
python main.py --mode web
```

Then open your browser to `http://localhost:5000`

### 3. Configure Your Social Media APIs

1. Go to the **Configuration** tab in the web dashboard
2. Enable the platforms you want to use
3. Enter your API credentials for each platform
4. Save your configuration

### 4. Test the System

Generate preview puzzles to see how they look:

```bash
python main.py --mode test
```

This will generate sample puzzles in multiple languages and difficulties in the `output/` directory.

## Usage Modes

### Web Dashboard (Recommended)

The web dashboard provides a beautiful interface for:
- Configuring social media API credentials
- Previewing generated puzzles
- Manually posting puzzles
- Viewing posting history
- Managing settings

```bash
python main.py --mode web
```

### Automated Scheduler

Run the automated scheduler for hands-free operation:

```bash
python main.py --mode scheduler
```

To post immediately:

```bash
python main.py --mode scheduler --post-now
```

### Test Mode

Generate sample puzzles for testing:

```bash
python main.py --mode test
```

## Configuration

### Demo Mode vs Production Mode

**Demo Mode** (default):
- Posts are simulated and saved locally to `output/scheduled_posts/`
- Perfect for testing without actually posting to social media
- No API credentials required

**Production Mode**:
- Requires valid API credentials for each platform
- Actually posts to social media
- Toggle in the web dashboard or edit `config.yaml`

### Setting Up Social Media APIs

#### Instagram
- Requires username and password
- OR use Meta Graph API (more reliable)

#### Twitter/X
- Create a developer account at https://developer.twitter.com
- Create an app and get API keys
- Required: API Key, API Secret, Access Token, Access Token Secret

#### Reddit
- Create an app at https://www.reddit.com/prefs/apps
- Required: Client ID, Client Secret, Username, Password
- Specify target subreddit (default: r/sudoku)

#### Facebook
- Use Facebook Graph API
- Required: Page ID, Access Token

## Project Structure

```
photonic-curiosity/
├── main.py                 # Main entry point
├── app.py                  # Flask web application
├── sudoku_generator.py     # Puzzle generation engine
├── puzzle_renderer.py      # Image rendering
├── localization.py         # Multi-language support
├── social_media_poster.py  # Social media posting
├── scheduler.py            # Automated scheduling
├── requirements.txt        # Python dependencies
├── config.yaml            # Configuration file
├── templates/
│   └── index.html         # Web dashboard UI
├── locales/               # Translation files
│   ├── en.json
│   ├── hi.json
│   ├── ta.json
│   └── ...
├── fonts/                 # Font files for rendering
└── output/                # Generated images and logs
    ├── posted/
    ├── scheduled_posts/
    └── posting_history.json
```

## Customization

### Adding More Languages

1. Add translations to `localization.py`
2. Download appropriate fonts and place in `fonts/` directory
3. Update the language configuration in web dashboard

### Changing Posting Schedule

Edit `config.yaml` or use the web dashboard:

```yaml
scheduling:
  times: ["09:00", "18:00", "15:00"]  # Add/remove times
  timezone: "Asia/Kolkata"
```

### Customizing Puzzle Appearance

Edit colors and styling in `puzzle_renderer.py`:

```python
COLORS = {
    'background': '#0F172A',
    'accent': '#3B82F6',
    # ... customize colors
}
```

## Troubleshooting

### Fonts Not Rendering

Download Google Noto fonts for Indian scripts:
- [Noto Sans Devanagari](https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari)
- [Noto Sans Tamil](https://fonts.google.com/noto/specimen/Noto+Sans+Tamil)
- [Noto Sans Telugu](https://fonts.google.com/noto/specimen/Noto+Sans+Telugu)
- etc.

Place the `.ttf` files in the `fonts/` directory.

### API Connection Errors

1. Verify your API credentials are correct
2. Check if your API access is not rate-limited
3. Use the "Test Connection" button in the web dashboard
4. Check logs for detailed error messages

### Scheduler Not Running

1. Make sure config.yaml exists and is valid
2. Check timezone settings
3. Verify Python timezone library is installed: `pip install pytz`

## License

MIT License - feel free to use and modify for your needs!

## Support

For issues or questions, please check the logs in the output directory or enable debug logging.

---

**Made with ❤️ for puzzle lovers around the world**
