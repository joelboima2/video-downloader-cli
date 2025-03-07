import re
from urllib.parse import urlparse
from .logger import setup_logger

logger = setup_logger()

class URLValidator:
    def __init__(self):
        # Regex for URL extraction
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        
        # Supported video platforms
        self.supported_domains = {
            'youtube.com',
            'youtu.be',
            'facebook.com',
            'fb.watch',
            'twitter.com',
            'instagram.com',
        }
    
    def extract_urls(self, text):
        """Extract all URLs from text"""
        return self.url_pattern.findall(text)
    
    def is_supported_video_url(self, url):
        """Check if URL is from a supported video platform"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove 'www.' if present
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Check if domain or any subdomain is supported
            return any(domain.endswith(supported) for supported in self.supported_domains)
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {str(e)}")
            return False
