import pyperclip
import time
import subprocess
import platform
from .url_validator import URLValidator
from .downloader import VideoDownloader
from .logger import setup_logger
from .ui import display_status

logger = setup_logger()

class ClipboardMonitor:
    def __init__(self, config):
        self.config = config
        self.url_validator = URLValidator()
        self.downloader = VideoDownloader(config)
        self.last_clipboard = ''
        self.processed_urls = set()
        self.setup_clipboard()
        self.verify_clipboard_access()
        logger.debug("ClipboardMonitor initialized with config")

    def setup_clipboard(self):
        """Configure clipboard based on platform"""
        try:
            # Check if running in Termux
            subprocess.run(["termux-clipboard-get"], capture_output=True, check=False)
            self.setup_termux_clipboard()
            logger.info("Termux clipboard support enabled")
        except (FileNotFoundError, subprocess.SubprocessError):
            logger.debug("Using default clipboard implementation")

    def setup_termux_clipboard(self):
        """Configure Pyperclip to use Termux clipboard"""
        def termux_paste():
            try:
                result = subprocess.run(
                    ["termux-clipboard-get"], 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                logger.error(f"Termux clipboard paste error: {str(e)}")
                return ''

        def termux_copy(text):
            try:
                subprocess.run(
                    ["termux-clipboard-set"], 
                    input=text.encode(), 
                    check=True
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Termux clipboard copy error: {str(e)}")

        pyperclip.copy = termux_copy
        pyperclip.paste = termux_paste

    def verify_clipboard_access(self):
        """Verify clipboard access is working"""
        try:
            pyperclip.paste()
            logger.debug("Clipboard access verified successfully")
        except Exception as e:
            logger.error(f"Clipboard access error: {str(e)}")
            if platform.system() == "Linux":
                logger.info("Please ensure xclip is installed on Linux systems")
            else:
                logger.info("Ensure Termux API is installed and accessible")
            raise

    def start_monitoring(self):
        """Start monitoring the clipboard for video URLs"""
        display_status("Started clipboard monitoring")
        display_status("Waiting for video URLs to be copied...", style="bold green")
        logger.debug("Supported platforms: YouTube, Facebook, Twitter, Instagram")

        while True:
            try:
                current_clipboard = pyperclip.paste()

                if current_clipboard and current_clipboard != self.last_clipboard:
                    logger.debug("New clipboard content detected")
                    self.last_clipboard = current_clipboard
                    self.process_clipboard_content(current_clipboard)

                time.sleep(1)  # Prevent high CPU usage

            except KeyboardInterrupt:
                display_status("Stopping clipboard monitor...", style="bold yellow")
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
            if url in self.processed_urls:
                logger.info(f"Skipping already processed URL: {url}")
                continue

            if self.url_validator.is_supported_video_url(url):
                logger.info(f"Found supported video URL: {url}")
                self.process_url(url)
                self.processed_urls.add(url)
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