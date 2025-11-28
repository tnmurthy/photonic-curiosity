"""
Static Site Generator for GitHub Pages
Generates a daily puzzle and embeds it into index.html
"""

import sys
import os
import json
import datetime

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_generator import SudokuGenerator

def generate_static_site():
    print("Generating daily puzzle...")
    
    # 1. Generate Puzzle
    generator = SudokuGenerator()
    # Rotate difficulty based on day of year
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    difficulties = ['easy', 'medium', 'hard']
    difficulty = difficulties[day_of_year % 3]
    
    puzzle, solution = generator.create_puzzle(difficulty)
    
    meta = {
        'difficulty': difficulty,
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'generated_at': datetime.datetime.now().isoformat()
    }
    
    # 2. Read Template
    template_path = os.path.join('templates', 'static_puzzle.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 3. Inject Data
    # We use simple string replacement to avoid needing Jinja2 in the CI environment if possible,
    # though we likely have it installed.
    html = template.replace('{{ puzzle_json }}', json.dumps(puzzle))
    html = html.replace('{{ solution_json }}', json.dumps(solution))
    html = html.replace('{{ meta_json }}', json.dumps(meta))
    
    # 4. Output
    output_dir = 'public'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Generated {output_path} with {difficulty} puzzle.")

if __name__ == '__main__':
    generate_static_site()
