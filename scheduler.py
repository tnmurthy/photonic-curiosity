"""
Scheduler for automated Sudoku posting
Handles twice-daily posting schedule
"""

import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import yaml
import logging
from datetime import datetime
from sudoku_generator import SudokuGenerator
from puzzle_renderer import PuzzleRenderer
from localization import Localization
from social_media_poster import SocialMediaPoster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SudokuScheduler:
    """Schedule and manage automated Sudoku puzzle posting."""
    
    # Difficulty rotation pattern
    DIFFICULTY_ROTATION = ['easy', 'medium', 'hard', 'medium', 'easy', 'hard']
    
    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize the scheduler.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.scheduler = BackgroundScheduler()
        self.post_counter = 0
        
        # Initialize components
        self.generator = SudokuGenerator()
        self.renderer = PuzzleRenderer()
        self.localization = Localization()
        self.poster = SocialMediaPoster(
            self.config,
            demo_mode=self.config.get('demo_mode', True)
        )
    
    def _load_config(self):
        """Load configuration from file and override with environment variables."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found, using defaults")
            config = {
                'scheduling': {'times': ['09:00', '18:00'], 'timezone': 'Asia/Kolkata'},
                'localization': {'default_language': 'en'},
                'platforms': {
                    'instagram': {'enabled': False},
                    'twitter': {'enabled': False},
                    'facebook': {'enabled': False},
                    'reddit': {'enabled': False},
                },
                'demo_mode': True
            }

        # Override with environment variables if they exist
        platforms = config.get('platforms', {})

        # Instagram
        if 'instagram' in platforms and os.getenv('INSTAGRAM_USERNAME'):
            platforms['instagram']['username'] = os.getenv('INSTAGRAM_USERNAME')
            platforms['instagram']['password'] = os.getenv('INSTAGRAM_PASSWORD')
            logger.info("Loaded Instagram credentials from environment variables.")

        # Twitter
        if 'twitter' in platforms and os.getenv('TWITTER_API_KEY'):
            platforms['twitter']['api_key'] = os.getenv('TWITTER_API_KEY')
            platforms['twitter']['api_secret'] = os.getenv('TWITTER_API_SECRET')
            platforms['twitter']['access_token'] = os.getenv('TWITTER_ACCESS_TOKEN')
            platforms['twitter']['access_token_secret'] = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            logger.info("Loaded Twitter credentials from environment variables.")

        # Reddit
        if 'reddit' in platforms and os.getenv('REDDIT_CLIENT_ID'):
            platforms['reddit']['client_id'] = os.getenv('REDDIT_CLIENT_ID')
            platforms['reddit']['client_secret'] = os.getenv('REDDIT_CLIENT_SECRET')
            platforms['reddit']['username'] = os.getenv('REDDIT_USERNAME')
            platforms['reddit']['password'] = os.getenv('REDDIT_PASSWORD')
            logger.info("Loaded Reddit credentials from environment variables.")

        # Facebook
        if 'facebook' in platforms and os.getenv('FACEBOOK_PAGE_ID'):
            platforms['facebook']['page_id'] = os.getenv('FACEBOOK_PAGE_ID')
            platforms['facebook']['access_token'] = os.getenv('FACEBOOK_ACCESS_TOKEN')
            logger.info("Loaded Facebook credentials from environment variables.")

        config['platforms'] = platforms

        # If any credentials are loaded, assume production mode
        if any(os.getenv(key) for key in [
            'INSTAGRAM_USERNAME', 'TWITTER_API_KEY',
            'REDDIT_CLIENT_ID', 'FACEBOOK_PAGE_ID'
        ]):
            config['demo_mode'] = False
            logger.info("Credentials found, setting demo_mode to False.")

        return config
    
    def setup_schedule(self):
        """Set up the posting schedule based on configuration."""
        times = self.config.get('scheduling', {}).get('times', ['09:00', '18:00'])
        timezone = self.config.get('scheduling', {}).get('timezone', 'Asia/Kolkata')
        
        for time_str in times:
            hour, minute = map(int, time_str.split(':'))
            
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                timezone=timezone
            )
            
            self.scheduler.add_job(
                self.generate_and_post,
                trigger=trigger,
                id=f'sudoku_post_{time_str}',
                replace_existing=True
            )
            
            logger.info(f"Scheduled post at {time_str} ({timezone})")
    
    def generate_and_post(self):
        """Generate a puzzle and post to all enabled platforms."""
        try:
            # Get difficulty for this post (rotate through pattern)
            difficulty = self.DIFFICULTY_ROTATION[self.post_counter % len(self.DIFFICULTY_ROTATION)]
            self.post_counter += 1
            
            # Get enabled platforms
            enabled_platforms = [
                name for name, config in self.config.get('platforms', {}).items()
                if config.get('enabled', False)
            ]
            
            if not enabled_platforms:
                logger.warning("No platforms enabled, skipping post")
                return
            
            # Get language settings
            default_language = self.config.get('localization', {}).get('default_language', 'en')
            
            # Generate puzzle
            puzzle, solution = self.generator.create_puzzle(difficulty)
            logger.info(f"Generated {difficulty} puzzle #{self.post_counter}")
            
            # Get localized text
            title = self.localization.get_text(default_language, 'ui.daily_sudoku')
            difficulty_label = self.localization.get_text(default_language, f'difficulty.{difficulty}')
            script = self.localization.INDIAN_LANGUAGES.get(default_language, {}).get('script', 'Latin')
            
            # Render images
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            puzzle_path = f'output/posted/puzzle_{timestamp}.png'
            solution_path = f'output/posted/solution_{timestamp}.png'
            
            self.renderer.render_puzzle(
                puzzle=puzzle,
                difficulty=difficulty,
                puzzle_number=self.post_counter,
                title=title,
                difficulty_label=difficulty_label,
                script=script,
                output_path=puzzle_path
            )
            
            self.renderer.render_solution(
                solution=solution,
                puzzle=puzzle,
                difficulty=difficulty,
                puzzle_number=self.post_counter,
                title=self.localization.get_text(default_language, 'ui.solution'),
                script=script,
                output_path=solution_path
            )
            
            # Prepare caption and hashtags
            website_url = self.config.get('website_url', 'http://localhost:5001')
            caption = self.localization.format_caption(default_language, difficulty, website_url)
            hashtags = self.localization.get_hashtags(default_language, difficulty)
            
            # Post to all enabled platforms
            for platform in enabled_platforms:
                result = self.poster.post_puzzle(
                    platform=platform,
                    image_paths=[puzzle_path, solution_path],
                    caption=caption,
                    hashtags=hashtags,
                    metadata={
                        'difficulty': difficulty,
                        'language': default_language,
                        'puzzle_number': self.post_counter,
                        'scheduled': True
                    }
                )
                
                if result['success']:
                    logger.info(f"Posted to {platform}: {result.get('post_id', 'N/A')}")
                else:
                    logger.error(f"Failed to post to {platform}: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Error in generate_and_post: {e}", exc_info=True)
    
    def start(self):
        """Start the scheduler."""
        self.setup_schedule()
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
    
    def post_now(self):
        """Manually trigger a post immediately."""
        logger.info("Manual post triggered")
        self.generate_and_post()


if __name__ == "__main__":
    # Run the scheduler
    scheduler = SudokuScheduler()
    scheduler.start()
    
    logger.info("Sudoku scheduler is running. Press Ctrl+C to stop.")
    
    try:
        # Keep the script running
        import time
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        logger.info("Scheduler stopped gracefully")
