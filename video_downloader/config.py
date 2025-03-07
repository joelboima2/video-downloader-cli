import os
import yaml
from .logger import setup_logger

logger = setup_logger()

class Config:
    def __init__(self):
        self.config_file = 'config.yaml'
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file or use defaults"""
        defaults = {
            'download_path': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'supported_platforms': [
                'youtube.com',
                'youtu.be',
                'facebook.com',
                'fb.watch',
                'twitter.com',
                'instagram.com'
            ]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    self.download_path = config.get('download_path', defaults['download_path'])
                    self.supported_platforms = config.get('supported_platforms', 
                                                        defaults['supported_platforms'])
            else:
                self.download_path = defaults['download_path']
                self.supported_platforms = defaults['supported_platforms']
                
            # Ensure download directory exists
            os.makedirs(self.download_path, exist_ok=True)
            
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            logger.info("Using default configuration")
            self.download_path = defaults['download_path']
            self.supported_platforms = defaults['supported_platforms']
