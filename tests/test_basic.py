import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_generator import SudokuGenerator
from localization import Localization

class TestSudokuSystem(unittest.TestCase):
    def setUp(self):
        self.generator = SudokuGenerator()
        self.localization = Localization()

    def test_puzzle_generation(self):
        """Test that puzzles are generated correctly."""
        difficulty = 'easy'
        puzzle, solution = self.generator.create_puzzle(difficulty)
        
        # Check dimensions
        self.assertEqual(len(puzzle), 9)
        self.assertEqual(len(puzzle[0]), 9)
        
        # Check that solution is valid (no zeros)
        for row in solution:
            self.assertNotIn(0, row)
            
        # Check that puzzle has zeros (empty cells)
        has_zeros = any(0 in row for row in puzzle)
        self.assertTrue(has_zeros)

    def test_localization(self):
        """Test that localization loads correctly."""
        # Test English
        text = self.localization.get_text('en', 'ui.daily_sudoku')
        self.assertIsNotNone(text)
        
        # Test Hindi (should exist)
        text_hi = self.localization.get_text('hi', 'difficulty.easy')
        self.assertIsNotNone(text_hi)

if __name__ == '__main__':
    unittest.main()
