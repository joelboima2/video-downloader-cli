import yt_dlp
import os
import hashlib
from .logger import setup_logger
from .ui import create_progress_bar, display_status
from rich.progress import Progress, TaskID
from typing import Optional
import platform
import sys

logger = setup_logger()

class VideoDownloader:
    def __init__(self, config):
        self.config = config
        self.downloaded_urls = set()

    def _get_video_id(self, url):
        """Generate a unique identifier for the video URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def download(self, url):
        """Download video from URL with progress tracking"""
        video_id = self._get_video_id(url)

        if video_id in self.downloaded_urls:
            display_status(f"Video already downloaded: {url}", style="bold yellow")
            return

        progress = None
        task_id = None

        def progress_hook(d):
            """Handle download progress updates"""
            nonlocal progress, task_id
            try:
                if progress is None:
                    progress = create_progress_bar()

                if d['status'] == 'downloading':
                    if task_id is None:
                        task_id = progress.add_task(
                            description=f"[cyan]Downloading {url}",
                            total=100.0,
                            completed=0.0
                        )
                        logger.debug(f"Created progress task: {task_id}")

                    # Calculate progress percentage
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', d.get('total_bytes_estimate', 0))

                    if total > 0:
                        percentage = (downloaded / total) * 100.0
                        logger.debug(f"Download progress: {downloaded}/{total} bytes ({percentage:.1f}%)")
                        if task_id is not None:
                            progress.update(task_id, completed=min(percentage, 100.0))
                    else:
                        logger.debug("Download size unknown, showing indeterminate progress")
                        if task_id is not None:
                            progress.update(task_id, completed=0.0)

                elif d['status'] == 'finished' and task_id is not None:
                    logger.debug("Download finished, setting progress to 100%")
                    progress.update(task_id, completed=100.0)

            except Exception as e:
                logger.error(f"Progress hook error: {str(e)}")
                logger.debug(f"Progress state - task_id: {task_id}, status: {d}")

        # Configure platform-specific browser for cookies
        system = platform.system().lower()
        if system == 'linux':
            browser = 'firefox'
        elif system == 'darwin':
            browser = 'safari'
        else:
            browser = 'chrome'

        # Configure yt-dlp options with platform-specific settings
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'cookiesfrombrowser': (browser,),  # Use platform-specific browser cookies
            'ignoreerrors': True,
            'no_warnings': True,
            'extract_flat': False,
            # Facebook-specific options
            'extractor_args': {
                'facebook': {
                    'api': ['consent=1'],  # Accept cookies consent
                }
            }
        }

        try:
            display_status(f"Starting download: {url}")
            logger.info(f"Starting download: {url}")

            # Create and maintain progress bar context
            progress = create_progress_bar()
            with progress:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            display_status(f"Successfully downloaded: {url}", style="bold green")
            self.downloaded_urls.add(video_id)

        except Exception as e:
            display_status(f"Failed to download: {url}\nError: {str(e)}", style="bold red")
            logger.error(f"Download failed for {url}: {str(e)}")
            raise