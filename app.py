"""
Flask Web Application for Sudoku Puzzle Automation
Provides web interface for API configuration and monitoring
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import yaml
import os
import json
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

CONFIG_FILE = 'config.yaml'
DEFAULT_CONFIG = {
    'scheduling': {
        'times': ['09:00', '18:00'],
        'timezone': 'Asia/Kolkata'
    },
    'localization': {
        'default_language': 'en',
        'auto_detect': True,
        'supported_languages': ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa']
    },
    'platforms': {
        'instagram': {
            'enabled': False,
            'username': '',
            'password': ''
        },
        'twitter': {
            'enabled': False,
            'api_key': '',
            'api_secret': '',
            'access_token': '',
            'access_token_secret': ''
        },
        'facebook': {
            'enabled': False,
            'page_id': '',
            'access_token': ''
        },
        'reddit': {
            'enabled': False,
            'client_id': '',
            'client_secret': '',
            'username': '',
            'password': '',
            'user_agent': 'SudokuBot by u/yourusername',
            'subreddit': 'sudoku'
        }
    },
    'demo_mode': True
}


def load_config():
    """Load configuration from file or create default."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    logger.info("Configuration saved")


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/batch')
def batch_preview():
    """Batch puzzle generation page."""
    return render_template('batch_preview.html')


@app.route('/puzzle')
def puzzle_of_the_day():
    """Interactive puzzle of the day page."""
    return render_template('puzzle.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    config = load_config()
    
    # Mask sensitive data
    masked_config = config.copy()
    for platform in masked_config.get('platforms', {}).values():
        for key in platform:
            if key in ['password', 'api_secret', 'access_token', 'access_token_secret']:
                if platform[key]:
                    platform[key] = '****' + platform[key][-4:] if len(platform[key]) > 4 else '****'
    
    return jsonify(masked_config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration."""
    try:
        new_config = request.json
        
        # Merge with existing config to preserve unmasked passwords
        current_config = load_config()
        
        # Deep merge platforms
        if 'platforms' in new_config:
            for platform, settings in new_config['platforms'].items():
                if platform not in current_config['platforms']:
                    current_config['platforms'][platform] = {}
                
                for key, value in settings.items():
                    # Only update if value is not masked
                    if not (isinstance(value, str) and value.startswith('****')):
                        current_config['platforms'][platform][key] = value
        
        # Update other settings
        if 'scheduling' in new_config:
            current_config['scheduling'] = new_config['scheduling']
        if 'localization' in new_config:
            current_config['localization'] = new_config['localization']
        if 'demo_mode' in new_config:
            current_config['demo_mode'] = new_config['demo_mode']
        
        save_config(current_config)
        
        return jsonify({'success': True, 'message': 'Configuration updated successfully'})
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/test-connection/<platform>', methods=['POST'])
def test_connection(platform):
    """Test connection to a social media platform."""
    try:
        config = load_config()
        platform_config = config.get('platforms', {}).get(platform, {})
        
        if not platform_config.get('enabled'):
            return jsonify({'success': False, 'message': f'{platform} is not enabled'})
        
        # In demo mode, always succeed
        if config.get('demo_mode', True):
            return jsonify({
                'success': True,
                'message': f'Demo mode: {platform} connection simulated successfully'
            })
        
        # TODO: Implement actual connection tests for each platform
        return jsonify({
            'success': False,
            'message': f'Connection test not implemented for {platform} in production mode'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/posting-history', methods=['GET'])
def get_posting_history():
    """Get posting history."""
    history_file = 'output/posting_history.json'
    
    if not os.path.exists(history_file):
        return jsonify([])
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # Return last 20 posts
        return jsonify(history[-20:])
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        return jsonify([])


@app.route('/api/generate-preview', methods=['POST'])
def generate_preview():
    """Generate a preview puzzle."""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        language = data.get('language', 'en')
        
        from sudoku_generator import SudokuGenerator
        from puzzle_renderer import PuzzleRenderer
        from localization import Localization
        
        # Generate puzzle
        generator = SudokuGenerator()
        puzzle, solution = generator.create_puzzle(difficulty)
        
        # Get localized text
        loc = Localization()
        title = loc.get_text(language, 'ui.daily_sudoku')
        difficulty_label = loc.get_text(language, f'difficulty.{difficulty}')
        script = loc.INDIAN_LANGUAGES.get(language, {}).get('script', 'Latin')
        
        # Render images
        renderer = PuzzleRenderer()
        
        puzzle_path = f'output/preview_puzzle_{language}_{difficulty}.png'
        solution_path = f'output/preview_solution_{language}_{difficulty}.png'
        
        renderer.render_puzzle(
            puzzle=puzzle,
            difficulty=difficulty,
            puzzle_number=0,
            title=title,
            difficulty_label=difficulty_label,
            script=script,
            output_path=puzzle_path
        )
        
        renderer.render_solution(
            solution=solution,
            puzzle=puzzle,
            difficulty=difficulty,
            puzzle_number=0,
            title=loc.get_text(language, 'ui.solution'),
            script=script,
            output_path=solution_path
        )
        
        return jsonify({
            'success': True,
            'puzzle_image': f'/output/{os.path.basename(puzzle_path)}',
            'solution_image': f'/output/{os.path.basename(solution_path)}',
            'caption': loc.format_caption(language, difficulty)
        })
    except Exception as e:
        logger.error(f"Error generating preview: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/generate-batch-preview', methods=['POST'])
def generate_batch_preview():
    """Generate preview puzzles for multiple languages at once."""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        languages = data.get('languages', ['en'])
        
        from sudoku_generator import SudokuGenerator
        from puzzle_renderer import PuzzleRenderer
        from localization import Localization
        
        # Generate one puzzle that will be used for all languages
        generator = SudokuGenerator()
        puzzle, solution = generator.create_puzzle(difficulty)
        
        loc = Localization()
        renderer = PuzzleRenderer()
        
        results = []
        
        for language in languages:
            try:
                # Get localized text
                title = loc.get_text(language, 'ui.daily_sudoku')
                difficulty_label = loc.get_text(language, f'difficulty.{difficulty}')
                script = loc.INDIAN_LANGUAGES.get(language, {}).get('script', 'Latin')
                
                # Render images
                puzzle_path = f'output/batch_preview_puzzle_{language}_{difficulty}.png'
                solution_path = f'output/batch_preview_solution_{language}_{difficulty}.png'
                
                renderer.render_puzzle(
                    puzzle=puzzle,
                    difficulty=difficulty,
                    puzzle_number=0,
                    title=title,
                    difficulty_label=difficulty_label,
                    script=script,
                    output_path=puzzle_path
                )
                
                renderer.render_solution(
                    solution=solution,
                    puzzle=puzzle,
                    difficulty=difficulty,
                    puzzle_number=0,
                    title=loc.get_text(language, 'ui.solution'),
                    script=script,
                    output_path=solution_path
                )
                
                results.append({
                    'language': language,
                    'language_name': loc.INDIAN_LANGUAGES.get(language, {}).get('name', language),
                    'success': True,
                    'puzzle_image': f'/output/{os.path.basename(puzzle_path)}',
                    'solution_image': f'/output/{os.path.basename(solution_path)}',
                    'caption': loc.format_caption(language, difficulty)
                })
            except Exception as e:
                logger.error(f"Error generating preview for {language}: {e}")
                results.append({
                    'language': language,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': sum(1 for r in results if r['success'])
        })
    except Exception as e:
        logger.error(f"Error in batch preview generation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/output/<path:filename>')
def serve_output(filename):
    """Serve output files."""
    return send_from_directory('output', filename)


@app.route('/api/puzzle-of-the-day', methods=['GET'])
def get_puzzle_of_the_day():
    """Get the current puzzle of the day."""
    puzzle_file = 'output/puzzle_of_the_day.json'

    if not os.path.exists(puzzle_file):
        # Optionally, generate one if it's missing
        return jsonify({'error': 'Puzzle of the day not found'}), 404

    try:
        with open(puzzle_file, 'r', encoding='utf-8') as f:
            puzzle_data = json.load(f)

        # Omit solution from the response
        puzzle_data.pop('solution', None)

        return jsonify(puzzle_data)
    except Exception as e:
        logger.error(f"Error loading puzzle of the day: {e}")
        return jsonify({'error': 'Could not load puzzle of the day'}), 500


@app.route('/api/check-solution', methods=['POST'])
def check_solution():
    """Check a user's Sudoku solution."""
    try:
        data = request.json
        # The user's solution grid
        user_solution = data.get('solution')

        # Load the full puzzle data, including the actual solution
        puzzle_file = 'output/puzzle_of_the_day.json'
        if not os.path.exists(puzzle_file):
            return jsonify({'success': False, 'error': 'Puzzle of the day not found'}), 404

        with open(puzzle_file, 'r', encoding='utf-8') as f:
            full_puzzle_data = json.load(f)

        actual_solution = full_puzzle_data.get('solution')

        if not actual_solution:
            return jsonify({'success': False, 'error': 'Solution not found for this puzzle'}), 500

        # Compare the user's solution to the actual solution
        is_correct = (user_solution == actual_solution)

        return jsonify({'success': is_correct})
    except Exception as e:
        logger.error(f"Error checking solution: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/leaderboard', methods=['POST'])
def update_leaderboard():
    """Update the leaderboard with a new score."""
    try:
        data = request.json
        name = data.get('name')
        time = data.get('time')  # Time in seconds

        if not name or not time:
            return jsonify({'success': False, 'error': 'Name and time are required'}), 400

        puzzle_file = 'output/puzzle_of_the_day.json'
        if not os.path.exists(puzzle_file):
            return jsonify({'success': False, 'error': 'Puzzle of the day not found'}), 404

        with open(puzzle_file, 'r', encoding='utf-8') as f:
            puzzle_data = json.load(f)

        leaderboard = puzzle_data.get('leaderboard', [])
        leaderboard.append({'name': name, 'time': time})

        # Sort leaderboard by time (lowest first) and keep top 10
        leaderboard.sort(key=lambda x: x['time'])
        puzzle_data['leaderboard'] = leaderboard[:10]

        with open(puzzle_file, 'w', encoding='utf-8') as f:
            json.dump(puzzle_data, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True, 'leaderboard': puzzle_data['leaderboard']})
    except Exception as e:
        logger.error(f"Error updating leaderboard: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/manual-post', methods=['POST'])
def manual_post():
    """Manually trigger a post."""
    try:
        data = request.json
        platform = data.get('platform')
        difficulty = data.get('difficulty', 'medium')
        language = data.get('language', 'en')
        
        from sudoku_generator import SudokuGenerator
        from puzzle_renderer import PuzzleRenderer
        from localization import Localization
        from social_media_poster import SocialMediaPoster
        
        # Generate puzzle
        generator = SudokuGenerator()
        puzzle, solution = generator.create_puzzle(difficulty)
        
        # Get localized text
        loc = Localization()
        title = loc.get_text(language, 'ui.daily_sudoku')
        difficulty_label = loc.get_text(language, f'difficulty.{difficulty}')
        script = loc.INDIAN_LANGUAGES.get(language, {}).get('script', 'Latin')
        
        # Render images
        renderer = PuzzleRenderer()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        puzzle_path = f'output/posted/puzzle_{timestamp}.png'
        solution_path = f'output/posted/solution_{timestamp}.png'
        
        renderer.render_puzzle(
            puzzle=puzzle,
            difficulty=difficulty,
            puzzle_number=0,
            title=title,
            difficulty_label=difficulty_label,
            script=script,
            output_path=puzzle_path
        )
        
        renderer.render_solution(
            solution=solution,
            puzzle=puzzle,
            difficulty=difficulty,
            puzzle_number=0,
            title=loc.get_text(language, 'ui.solution'),
            script=script,
            output_path=solution_path
        )
        
        # Post
        config = load_config()
        poster = SocialMediaPoster(config, demo_mode=config.get('demo_mode', True))
        
        caption = loc.format_caption(language, difficulty)
        hashtags = loc.get_hashtags(language, difficulty)
        
        result = poster.post_puzzle(
            platform=platform,
            image_paths=[puzzle_path, solution_path],
            caption=caption,
            hashtags=hashtags,
            metadata={
                'difficulty': difficulty,
                'language': language,
                'manual': True
            }
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in manual post: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('output', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
