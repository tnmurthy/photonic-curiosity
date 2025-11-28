"""
Main entry point for Sudoku Automation System
"""

import argparse
import logging
import sys
from scheduler import SudokuScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Sudoku Automation System')
    parser.add_argument(
        '--mode',
        choices=['web', 'scheduler', 'test'],
        default='web',
        help='Run mode: web (dashboard), scheduler (automated posting), or test (generate sample)'
    )
    parser.add_argument(
        '--post-now',
        action='store_true',
        help='Post immediately (works with scheduler mode)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        # Run web dashboard
        logger.info("Starting web dashboard...")
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.mode == 'scheduler':
        # Run automated scheduler
        logger.info("Starting automated scheduler...")
        scheduler = SudokuScheduler()
        
        if args.post_now:
            logger.info("Posting immediately...")
            scheduler.post_now()
        
        scheduler.start()
        
        try:
            import time
            logger.info("Scheduler running. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.stop()
            logger.info("Scheduler stopped")
    
    elif args.mode == 'test':
        # Generate test puzzle
        logger.info("Generating test puzzle...")
        from sudoku_generator import SudokuGenerator
        from puzzle_renderer import PuzzleRenderer
        from localization import Localization
        
        generator = SudokuGenerator()
        renderer = PuzzleRenderer()
        loc = Localization()
        
        # Test each difficulty
        for difficulty in ['easy', 'medium', 'hard']:
            for language in ['en', 'hi', 'ta']:
                logger.info(f"Generating {difficulty} puzzle in {language}...")
                
                puzzle, solution = generator.create_puzzle(difficulty)
                
                title = loc.get_text(language, 'ui.daily_sudoku')
                difficulty_label = loc.get_text(language, f'difficulty.{difficulty}')
                script = loc.INDIAN_LANGUAGES.get(language, {}).get('script', 'Latin')
                
                puzzle_path = f'output/test_{language}_{difficulty}_puzzle.png'
                solution_path = f'output/test_{language}_{difficulty}_solution.png'
                
                renderer.render_puzzle(
                    puzzle=puzzle,
                    difficulty=difficulty,
                    puzzle_number=1,
                    title=title,
                    difficulty_label=difficulty_label,
                    script=script,
                    output_path=puzzle_path
                )
                
                renderer.render_solution(
                    solution=solution,
                    puzzle=puzzle,
                    difficulty=difficulty,
                    puzzle_number=1,
                    title=loc.get_text(language, 'ui.solution'),
                    script=script,
                    output_path=solution_path
                )
                
                logger.info(f"  Saved: {puzzle_path}, {solution_path}")
        
        logger.info("\nTest complete! Check the output/ directory for generated images.")
        logger.info("To start the web dashboard, run: python main.py --mode web")


if __name__ == '__main__':
    main()
