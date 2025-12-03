"""
Social Media Poster
Handles posting to various social media platforms
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaPoster:
    """Handle posting to multiple social media platforms."""
    
    SUPPORTED_PLATFORMS = ['instagram', 'twitter', 'facebook', 'reddit']
    
    def __init__(self, config: Dict, demo_mode: bool = True):
        """
        Initialize social media poster.
        
        Args:
            config: Configuration dictionary with API credentials
            demo_mode: If True, simulate posting without actual API calls
        """
        self.config = config
        self.demo_mode = demo_mode
        self.history_file = 'output/posting_history.json'
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists."""
        os.makedirs('output/scheduled_posts', exist_ok=True)
        os.makedirs('output/posted', exist_ok=True)
    
    def post_puzzle(
        self,
        platform: str,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Post a puzzle to a social media platform.
        
        Args:
            platform: Platform name ('instagram', 'twitter', etc.)
            image_paths: List of image file paths
            caption: Post caption
            hashtags: List of hashtags
            metadata: Additional metadata
            
        Returns:
            Dictionary with posting result
        """
        if platform not in self.SUPPORTED_PLATFORMS:
            logger.error(f"Unsupported platform: {platform}")
            return {'success': False, 'error': 'Unsupported platform'}
        
        if self.demo_mode:
            return self._simulate_post(platform, image_paths, caption, hashtags, metadata)
        
        # Check if platform is enabled
        platform_config = self.config.get('platforms', {}).get(platform, {})
        if not platform_config.get('enabled', False):
            logger.warning(f"Platform {platform} is not enabled")
            return {'success': False, 'error': 'Platform not enabled'}
        
        # Route to appropriate platform handler
        result = {}
        try:
            if platform == 'instagram':
                result = self._post_to_instagram(image_paths, caption, hashtags, platform_config)
            elif platform == 'twitter':
                result = self._post_to_twitter(image_paths, caption, hashtags, platform_config)
            elif platform == 'facebook':
                result = self._post_to_facebook(image_paths, caption, hashtags, platform_config)
            elif platform == 'reddit':
                result = self._post_to_reddit(image_paths, caption, hashtags, platform_config)
            else:
                result = {'success': False, 'error': 'Platform handler not implemented'}
        except Exception as e:
            logger.error(f"Error posting to {platform}: {e}")
            result = {'success': False, 'error': str(e)}

        # Add metadata to result and save to history
        result.update({
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
        self._add_to_history(result)

        return result
    
    def _simulate_post(
        self,
        platform: str,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Simulate a post in demo mode.
        
        Args:
            platform: Platform name
            image_paths: Image paths
            caption: Caption text
            hashtags: Hashtags list
            metadata: Additional metadata
            
        Returns:
            Simulated result dictionary
        """
        timestamp = datetime.now().isoformat()
        post_id = f"DEMO_{platform}_{timestamp.replace(':', '-')}"
        
        # Save post data
        post_data = {
            'post_id': post_id,
            'platform': platform,
            'timestamp': timestamp,
            'image_paths': image_paths,
            'caption': caption,
            'hashtags': hashtags,
            'metadata': metadata or {},
            'demo_mode': True
        }
        
        # Save to JSON file
        output_file = f"output/scheduled_posts/{post_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, ensure_ascii=False, indent=2)

        logger.info(f"[DEMO MODE] Simulated post to {platform}: {output_file}")
        
        # Add to history
        self._add_to_history(post_data)
        
        return post_data
    
    def _post_to_instagram(
        self,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        config: Dict
    ) -> Dict:
        """Post to Instagram using Graph API or instagrapi."""
        # This is a placeholder - actual implementation would use instagrapi or Graph API
        logger.info("Posting to Instagram (production mode)")
        
        try:
            # Example using instagrapi (uncomment when library is installed)
            # from instagrapi import Client
            # cl = Client()
            # cl.login(config['username'], config['password'])
            # 
            # full_caption = f"{caption}\n\n{' '.join(['#' + tag for tag in hashtags])}"
            # 
            # if len(image_paths) == 1:
            #     result = cl.photo_upload(image_paths[0], full_caption)
            # else:
            #     result = cl.album_upload(image_paths, full_caption)
            # 
            # return {
            #     'success': True,
            #     'post_id': result.pk,
            #     'platform': 'instagram',
            #     'url': f"https://instagram.com/p/{result.code}/"
            # }
            
            return {'success': False, 'error': 'Instagram posting not configured. Please install instagrapi and configure credentials.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _post_to_twitter(
        self,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        config: Dict
    ) -> Dict:
        """Post to Twitter/X using tweepy."""
        logger.info("Posting to Twitter (production mode)")
        
        try:
            # Example using tweepy (uncomment when configured)
            # import tweepy
            # 
            # auth = tweepy.OAuthHandler(config['api_key'], config['api_secret'])
            # auth.set_access_token(config['access_token'], config['access_token_secret'])
            # api = tweepy.API(auth)
            # 
            # full_text = f"{caption}\n\n{' '.join(['#' + tag for tag in hashtags[:4]])}"  # Twitter hashtag limit
            # 
            # # Upload media
            # media_ids = []
            # for img_path in image_paths[:4]:  # Twitter allows max 4 images
            #     media = api.media_upload(img_path)
            #     media_ids.append(media.media_id)
            # 
            # # Post tweet
            # tweet = api.update_status(status=full_text, media_ids=media_ids)
            # 
            # return {
            #     'success': True,
            #     'post_id': tweet.id_str,
            #     'platform': 'twitter',
            #     'url': f"https://twitter.com/user/status/{tweet.id_str}"
            # }
            
            return {'success': False, 'error': 'Twitter posting not configured. Please install tweepy and configure credentials.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _post_to_facebook(
        self,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        config: Dict
    ) -> Dict:
        """Post to Facebook using Graph API."""
        logger.info("Posting to Facebook (production mode)")
        
        # Placeholder - would use Facebook Graph API
        return {'success': False, 'error': 'Facebook posting not configured'}
    
    def _post_to_reddit(
        self,
        image_paths: List[str],
        caption: str,
        hashtags: List[str],
        config: Dict
    ) -> Dict:
        """Post to Reddit using PRAW."""
        logger.info("Posting to Reddit (production mode)")
        
        try:
            # Example using PRAW (uncomment when configured)
            # import praw
            # 
            # reddit = praw.Reddit(
            #     client_id=config['client_id'],
            #     client_secret=config['client_secret'],
            #     user_agent=config['user_agent'],
            #     username=config['username'],
            #     password=config['password']
            # )
            # 
            # subreddit = reddit.subreddit(config.get('subreddit', 'sudoku'))
            # 
            # # Post as image
            # submission = subreddit.submit_image(
            #     title=caption,
            #     image_path=image_paths[0]
            # )
            # 
            # return {
            #     'success': True,
            #     'post_id': submission.id,
            #     'platform': 'reddit',
            #     'url': submission.url
            # }
            
            return {'success': False, 'error': 'Reddit posting not configured. Please install praw and configure credentials.'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _add_to_history(self, post_data: Dict) -> None:
        """Add post to history file."""
        history = []
        
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append(post_data)
        
        # Keep only last 100 posts
        history = history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get posting history.
        
        Args:
            limit: Number of recent posts to return
            
        Returns:
            List of post dictionaries
        """
        if not os.path.exists(self.history_file):
            return []
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        return history[-limit:]


if __name__ == "__main__":
    # Test demo mode
    config = {'platforms': {}}
    poster = SocialMediaPoster(config, demo_mode=True)
    
    result = poster.post_puzzle(
        platform='instagram',
        image_paths=['output/test_puzzle.png', 'output/test_solution.png'],
        caption='🧩 Medium Sudoku Challenge!\n\nTest your skills!',
        hashtags=['Sudoku', 'PuzzleOfTheDay', 'BrainTeaser'],
        metadata={'difficulty': 'medium', 'puzzle_number': 1}
    )
    
    print(json.dumps(result, indent=2))
