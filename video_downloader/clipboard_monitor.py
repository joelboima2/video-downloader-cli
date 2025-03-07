import pyperclip
import time
from .url_validator import URLValidator
from .downloader import VideoDownloader
from .logger import setup_logger

logger = setup_logger()

class ClipboardMonitor:
    def __init__(self, config):
        self.config = config
        self.url_validator = URLValidator()
        self.downloader = VideoDownloader(config)
        self.last_clipboard = ''
        self.verify_clipboard_access()

    def verify_clipboard_access(self):
        """Verify clipboard access is working"""
        try:
            pyperclip.paste()
            logger.debug("Clipboard access verified successfully")
        except Exception as e:
            logger.error(f"Clipboard access error: {str(e)}")
            logger.info("Please ensure xclip is installed on Linux systems")
            raise

    def start_monitoring(self):
        """Start monitoring the clipboard for video URLs"""
        logger.info("Started clipboard monitoring")
        logger.info("Waiting for video URLs to be copied...")

        while True:
            try:
                current_clipboard = pyperclip.paste()

                if current_clipboard and current_clipboard != self.last_clipboard:
                    logger.debug(f"New clipboard content detected")
                    self.last_clipboard = current_clipboard
                    self.process_clipboard_content(current_clipboard)

                time.sleep(1)  # Prevent high CPU usage

            except KeyboardInterrupt:
                logger.info("Stopping clipboard monitor...")
                break
            except Exception as e:
                logger.error(f"Error monitoring clipboard: {str(e)}")
                time.sleep(5)  # Longer delay on error

    def process_clipboard_content(self, content):
        """Process clipboard content for video URLs"""
        urls = self.url_validator.extract_urls(content)

        if not urls:
            logger.debug("No URLs found in clipboard content")
            return

        for url in urls:
            if self.url_validator.is_supported_video_url(url):
                logger.info(f"Found video URL: {url}")
                self.process_url(url)
            else:
                logger.debug(f"Unsupported URL format: {url}")

    def process_url(self, url):
        """Process a single video URL"""
        try:
            logger.info(f"Starting download for: {url}")
            self.downloader.download(url)
            logger.info(f"Successfully processed URL: {url}")
        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")