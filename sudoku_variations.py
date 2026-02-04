import random
from enum import Enum

class SudokuType(Enum):
    CLASSIC = "classic"
    EMOJI = "emoji"
    COLOR = "color"
    SYMBOL = "symbol"
    PICTURE = "picture"
    KIDS = "kids"

class SudokuVariations:
    def __init__(self):
        self.themes = {
            "emoji": {
                "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨"],
                "fruits": ["🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐"],
                "faces": ["😀", "😂", "🥰", "😎", "🤔", "😴", "🤯", "🥳", "😇"],
                # v2.1 NEW THEMES
                "space": ["🚀", "🪐", "🌟", "☄️", "🛰️", "🛸", "👨‍🚀", "🌌", "🌑"],
                "weather": ["☀️", "☁️", "⛈️", "❄️", "🌪️", "🌈", "🌊", "🔥", "🌫️"],
                "sports": ["⚽", "🏀", "🎾", "🏐", "🏈", "🎱", "🏓", "🏹", "🥊"]
            },
            "color": {
                "rainbow": ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet", "Pink", "Cyan"],
                "pastel": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D1BAFF", "#FFBAF1", "#A8E6CF", "#DCEDC1"]
            },
            "symbol": {
                "greek": ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι"],
                "shapes": ["■", "▲", "●", "★", "◆", "♠", "♣", "♥", "♦"]
            }
        }

    def get_available_variations(self):
        return {
            "classic": {"description": "Traditional numbers 1-9", "themes": [], "target_audience": "All", "difficulty_modifier": 1.0},
            "emoji": {"description": "Fun emoji sets", "themes": list(self.themes["emoji"].keys()), "target_audience": "Kids & Casual", "difficulty_modifier": 0.9},
            "color": {"description": "Color-based logic", "themes": list(self.themes["color"].keys()), "target_audience": "Visual Learners", "difficulty_modifier": 1.1},
            "symbol": {"description": "Mathematical & Shape symbols", "themes": list(self.themes["symbol"].keys()), "target_audience": "Advanced", "difficulty_modifier": 1.2}
        }

    def convert_puzzle(self, grid, variation_type="classic", theme=None, custom_symbols=None):
        """
        Converts a numeric grid (1-9) to the selected variation symbols.
        v2.1: Added custom_symbols support for Custom Theme Creator.
        """
        if custom_symbols and len(custom_symbols) == 9:
            symbols = custom_symbols
        elif variation_type == "classic" or variation_type not in self.themes:
            symbols = [str(i) for i in range(1, 10)]
        else:
            available_themes = self.themes.get(variation_type, {})
            selected_theme = theme if theme in available_themes else list(available_themes.keys())[0]
            symbols = available_themes[selected_theme]

        # Mapping: 1 -> symbols[0], 2 -> symbols[1], ... 0 stays 0
        converted_grid = []
        for row in grid:
            new_row = []
            for cell in row:
                if cell == 0:
                    new_row.append(0)
                else:
                    new_row.append(symbols[cell - 1])
            converted_grid.append(new_row)
        
        return converted_grid, symbols

    def get_daily_challenge_seed(self):
        """v2.1: Generates a stable seed for the day's challenge"""
        return int(datetime.datetime.now().strftime("%Y%m%d"))

# Simple placeholder for grid generation (to be replaced by a real generator)
def generate_base_grid(difficulty="easy"):
    # Just a static valid solved grid for demo
    base = [[5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]]
    
    # Randomly remove cells based on difficulty
    cells_to_remove = {"easy": 30, "medium": 45, "hard": 55}.get(difficulty, 30)
    puzzle = [row[:] for row in base]
    count = 0
    while count < cells_to_remove:
        r, c = random.randint(0,8), random.randint(0,8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            count += 1
    return puzzle
