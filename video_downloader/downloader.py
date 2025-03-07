import yt_dlp
import os
import hashlib
from .logger import setup_logger
from .ui import create_progress_bar, display_status

logger = setup_logger()

class VideoDownloader:
    def __init__(self, config):
        self.config = config
        self.downloaded_urls = set()
        self.progress = create_progress_bar()

    def _get_video_id(self, url):
        """Generate a unique identifier for the video URL"""
        return hashlib.md5(url.encode()).hexdigest()

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

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
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

        except Exception as e:
            display_status(f"Failed to download: {url}\nError: {str(e)}", style="bold red")
            logger.error(f"Download failed for {url}: {str(e)}")
            raise