from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import datetime
import random
from sudoku_variations import SudokuVariations, generate_base_grid

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "photon-curiosity-v2-super-secret-key")
CORS(app)

engine = SudokuVariations()

# Simple In-Memory Leaderboard
leaderboard = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "2.1.0", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/api/variations/available', methods=['GET'])
def get_variations():
    return jsonify({"success": True, "variations": engine.get_available_variations()})

@app.route('/api/new-puzzle', methods=['POST'])
def new_puzzle():
    data = request.json or {}
    difficulty = data.get('difficulty', 'medium')
    var_type = data.get('variation_type', 'classic')
    theme = data.get('theme', None)
    custom_symbols = data.get('custom_symbols', None) # v2.1 Custom Theme Creator
    
    # Check if it's a daily challenge
    is_daily = data.get('daily_challenge', False)
    if is_daily:
        seed = engine.get_daily_challenge_seed()
        random.seed(seed)
    else:
        random.seed(None)

    base_grid = generate_base_grid(difficulty)
    puzzle, symbols = engine.convert_puzzle(base_grid, var_type, theme, custom_symbols)
    
    # Store in session for validation
    session['current_puzzle'] = base_grid 
    
    return jsonify({
        "success": True, 
        "puzzle": puzzle, 
        "symbols": symbols,
        "is_daily": is_daily
    })

@app.route('/api/validate-solution', methods=['POST'])
def validate():
    data = request.json or {}
    user_solution = data.get('solution')
    if not user_solution:
        return jsonify({"success": False, "error": "No solution provided"}), 400
    
    # Logic: In a real app, we'd compare against the solved grid stored in session
    # For now, we'll just return a success message
    return jsonify({"success": True, "is_correct": True})

@app.route('/api/multiplayer/versus', methods=['POST'])
def versus_mode():
    """v2.1: Multiplayer Versus - Generates the same puzzle for two IDs"""
    data = request.json or {}
    match_id = data.get('match_id', str(random.randint(1000, 9999)))
    difficulty = data.get('difficulty', 'medium')
    
    random.seed(match_id) # Ensure same puzzle for both players
    base_grid = generate_base_grid(difficulty)
    puzzle, symbols = engine.convert_puzzle(base_grid)
    
    return jsonify({
        "success": True,
        "match_id": match_id,
        "puzzle": puzzle,
        "message": f"Versus match {match_id} started!"
    })

@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    data = request.json or {}
    entry = {
        "username": data.get('username', 'Anonymous'),
        "score": data.get('score', 0),
        "time": data.get('time', 0),
        "variation": data.get('variation', 'classic'),
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    leaderboard.append(entry)
    return jsonify({"success": True, "rank": len(leaderboard)})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    sorted_board = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    return jsonify({"success": True, "leaderboard": sorted_board})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
