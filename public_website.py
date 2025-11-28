"""
Public-facing Interactive Sudoku Website
Users can solve puzzles online with timer, leaderboard, and rankings
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import secrets
from sudoku_generator import SudokuGenerator
from localization import Localization

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(32)
CORS(app)

# Data storage
LEADERBOARD_FILE = 'data/leaderboard.json'
USER_STATS_FILE = 'data/user_stats.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)


def load_leaderboard():
    """Load leaderboard from file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_leaderboard(leaderboard):
    """Save leaderboard to file."""
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)


def load_user_stats():
    """Load user statistics."""
    if os.path.exists(USER_STATS_FILE):
        with open(USER_STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_user_stats(stats):
    """Save user statistics."""
    with open(USER_STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def calculate_score(difficulty, time_seconds, hints_used):
    """
    Calculate score based on difficulty, time, and hints.
    
    Score formula:
    - Base score by difficulty (Easy: 100, Medium: 200, Hard: 300)
    - Time bonus (faster = more points)
    - Hint penalty (-20 per hint)
    """
    base_scores = {'easy': 100, 'medium': 200, 'hard': 300}
    base = base_scores.get(difficulty, 100)
    
    # Time bonus (max 100 points, decreases over time)
    time_bonus = max(0, 100 - (time_seconds / 10))
    
    # Hint penalty
    hint_penalty = hints_used * 20
    
    total = int(base + time_bonus - hint_penalty)
    return max(10, total)  # Minimum score of 10


@app.route('/')
def index():
    """Main puzzle page."""
    return render_template('puzzle.html')


@app.route('/api/new-puzzle', methods=['POST'])
def new_puzzle():
    """Generate a new puzzle."""
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        language = data.get('language', 'en')
        
        generator = SudokuGenerator()
        puzzle, solution = generator.create_puzzle(difficulty)
        
        # Store puzzle and solution in session
        session['current_puzzle'] = puzzle
        session['current_solution'] = solution
        session['difficulty'] = difficulty
        session['start_time'] = datetime.now().isoformat()
        
        # Get localized text
        loc = Localization()
        title = loc.get_text(language, 'ui.daily_sudoku')
        difficulty_label = loc.get_text(language, f'difficulty.{difficulty}')
        
        return jsonify({
            'success': True,
            'puzzle': puzzle,
            'difficulty': difficulty,
            'title': title,
            'difficulty_label': difficulty_label
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/validate-solution', methods=['POST'])
def validate_solution():
    """Validate user's solution."""
    try:
        data = request.json
        user_solution = data.get('solution')
        correct_solution = session.get('current_solution')
        
        if not correct_solution:
            return jsonify({'success': False, 'error': 'No active puzzle'}), 400
        
        # Check if solution matches
        is_correct = user_solution == correct_solution
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'solution': correct_solution if not is_correct else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    """Submit completed puzzle score."""
    try:
        data = request.json
        username = data.get('username', 'Anonymous')
        time_seconds = data.get('time', 0)
        hints_used = data.get('hints', 0)
        
        difficulty = session.get('difficulty', 'medium')
        start_time = session.get('start_time')
        
        if not start_time:
            return jsonify({'success': False, 'error': 'No active puzzle'}), 400
        
        # Calculate score
        score = calculate_score(difficulty, time_seconds, hints_used)
        
        # Create entry
        entry = {
            'username': username,
            'score': score,
            'difficulty': difficulty,
            'time': time_seconds,
            'hints_used': hints_used,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Add to leaderboard
        leaderboard = load_leaderboard()
        leaderboard.append(entry)
        
        # Sort by score (descending) and keep top 100
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:100]
        save_leaderboard(leaderboard)
        
        # Update user stats
        stats = load_user_stats()
        if username not in stats:
            stats[username] = {
                'total_puzzles': 0,
                'total_score': 0,
                'best_score': 0,
                'puzzles_by_difficulty': {'easy': 0, 'medium': 0, 'hard': 0},
                'average_time': 0,
                'total_time': 0
            }
        
        user_stat = stats[username]
        user_stat['total_puzzles'] += 1
        user_stat['total_score'] += score
        user_stat['best_score'] = max(user_stat['best_score'], score)
        user_stat['puzzles_by_difficulty'][difficulty] += 1
        user_stat['total_time'] += time_seconds
        user_stat['average_time'] = user_stat['total_time'] / user_stat['total_puzzles']
        
        save_user_stats(stats)
        
        # Find user's rank
        rank = next((i + 1 for i, e in enumerate(leaderboard) if e['timestamp'] == entry['timestamp']), None)
        
        return jsonify({
            'success': True,
            'score': score,
            'rank': rank,
            'total_entries': len(leaderboard)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard data."""
    try:
        filter_type = request.args.get('filter', 'all')  # all, today, week
        difficulty = request.args.get('difficulty', 'all')
        
        leaderboard = load_leaderboard()
        
        # Filter by time
        if filter_type == 'today':
            today = datetime.now().strftime('%Y-%m-%d')
            leaderboard = [e for e in leaderboard if e.get('date') == today]
        elif filter_type == 'week':
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            leaderboard = [e for e in leaderboard if e.get('date', '') >= week_ago]
        
        # Filter by difficulty
        if difficulty != 'all':
            leaderboard = [e for e in leaderboard if e.get('difficulty') == difficulty]
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard[:50]  # Top 50
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/user-stats/<username>', methods=['GET'])
def get_user_stats(username):
    """Get statistics for a specific user."""
    try:
        stats = load_user_stats()
        user_stat = stats.get(username, {})
        
        if not user_stat:
            return jsonify({
                'success': True,
                'stats': None,
                'message': 'User not found'
            })
        
        return jsonify({
            'success': True,
            'stats': user_stat
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/kpi', methods=['GET'])
def get_kpi():
    """Get overall KPIs."""
    try:
        stats = load_user_stats()
        leaderboard = load_leaderboard()
        
        total_users = len(stats)
        total_puzzles_solved = sum(s['total_puzzles'] for s in stats.values())
        
        # Calculate average solve time
        avg_time = sum(s['average_time'] for s in stats.values()) / total_users if total_users > 0 else 0
        
        # Puzzles by difficulty
        puzzles_by_diff = {'easy': 0, 'medium': 0, 'hard': 0}
        for user_stat in stats.values():
            for diff, count in user_stat['puzzles_by_difficulty'].items():
                puzzles_by_diff[diff] += count
        
        # Recent activity (last 24 hours)
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        recent_submissions = len([e for e in leaderboard if e.get('timestamp', '') >= yesterday])
        
        return jsonify({
            'success': True,
            'kpi': {
                'total_users': total_users,
                'total_puzzles_solved': total_puzzles_solved,
                'average_solve_time': int(avg_time),
                'puzzles_by_difficulty': puzzles_by_diff,
                'recent_submissions_24h': recent_submissions
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
