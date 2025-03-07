import yt_dlp
import os
import hashlib
from .logger import setup_logger
from .ui import create_progress_bar, display_status

logger = setup_logger()

class VideoDownloader:
    def __init__(self, config, options=None):
        self.config = config
        self.options = options or {}
        self.downloaded_urls = set()
        self.progress = create_progress_bar()

        # Load download archive if specified
        self.archive_file = self.options.get('download_archive')
        if self.archive_file and os.path.exists(self.archive_file):
            with open(self.archive_file, 'r') as f:
                self.downloaded_urls.update(line.strip() for line in f)

    def _get_video_id(self, url):
        """Generate a unique identifier for the video URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def _update_archive(self, video_id):
        """Update download archive with new video ID"""
        if self.archive_file:
            with open(self.archive_file, 'a') as f:
                f.write(f"{video_id}\n")

    def download(self, url):
        """Download video from URL with progress tracking"""
        video_id = self._get_video_id(url)

        if video_id in self.downloaded_urls:
            display_status(f"Video already downloaded: {url}", style="bold yellow")
            return

        def progress_hook(d):
            if d['status'] == 'downloading':
                # Calculate progress percentage
                if 'total_bytes' in d:
                    percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d:
                    percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    percentage = 0

                # Update progress bar
                if hasattr(self, 'task'):
                    self.task.update(completed=percentage)

        # Configure format based on quality setting
        quality_format = {
            'best': 'bestvideo+bestaudio/best',
            'medium': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        }.get(self.options.get('quality', 'best'), 'best')

        # Configure output format
        output_format = self.options.get('format', 'mp4')

        # Setup yt-dlp options with multi-browser cookies support
        ydl_opts = {
            'format': quality_format,
            'merge_output_format': output_format,
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if self.options.get('show_progress', True) else [],
            'quiet': True,
            'cookiesfrombrowser': ('chrome', 'firefox', 'safari', 'edge'),  # Try multiple browsers
        }

        try:
            display_status(f"Starting download: {url}")

            with self.progress:
                self.task = self.progress.add_task(
                    f"[cyan]Downloading: {url}",
                    total=100
                )

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    logger.info(f"Starting download: {url}")
                    ydl.download([url])

            display_status(f"Successfully downloaded: {url}", style="bold green")
            self.downloaded_urls.add(video_id)
            self._update_archive(video_id)

        except Exception as e:
            error_msg = str(e)
            if "Sign in to confirm you're not a bot" in error_msg:
                helpful_msg = (
                    f"Failed to download: {url}\n"
                    "YouTube requires authentication for this video.\n"
                    "Try one of these solutions:\n"
                    "1. Export cookies from your browser using yt-dlp's browser extension\n"
                    "2. Use a different video URL\n"
                    "3. Try downloading a non-age-restricted video"
                )
                display_status(helpful_msg, style="bold red")
            else:
                display_status(f"Failed to download: {url}\nError: {error_msg}", style="bold red")
            logger.error(f"Download failed for {url}: {error_msg}")
            raise