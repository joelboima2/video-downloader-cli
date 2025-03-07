import yt_dlp
import os
import hashlib
from .logger import setup_logger
from .ui import create_progress_bar, display_status
from rich.progress import Progress

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

        # Create progress bar with default configuration
        progress = create_progress_bar()
        task_id = None

        def progress_hook(d):
            """Handle download progress updates"""
            nonlocal task_id

            try:
                if d['status'] == 'downloading':
                    # Initialize task if not exists
                    if task_id is None:
                        logger.debug("Initializing new progress task")
                        task_id = progress.add_task(
                            f"[cyan]Downloading {url}",
                            total=100.0
                        )
                        logger.debug(f"Created task ID: {task_id}")

                    # Calculate progress percentage
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', d.get('total_bytes_estimate', 0))

                    if total > 0:
                        percentage = (downloaded / total) * 100
                        logger.debug(f"Download progress: {downloaded}/{total} bytes ({percentage:.1f}%)")
                        progress.update(task_id, completed=min(percentage, 100.0))
                    else:
                        logger.debug("Download size unknown, showing indeterminate progress")

                elif d['status'] == 'finished' and task_id is not None:
                    logger.debug("Download finished, updating progress to 100%")
                    progress.update(task_id, completed=100.0)

            except Exception as e:
                logger.error(f"Progress update error: {str(e)}")
                logger.debug(f"Debug info - task_id: {task_id}, status: {d.get('status')}")

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
        }

        try:
            with progress:  # Ensure progress bar context is maintained
                display_status(f"Starting download: {url}")
                logger.debug("Initialized progress bar, starting download")

                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    logger.info(f"Starting download: {url}")
                    ydl.download([url])

            display_status(f"Successfully downloaded: {url}", style="bold green")
            self.downloaded_urls.add(video_id)

        except Exception as e:
            display_status(f"Failed to download: {url}\nError: {str(e)}", style="bold red")
            logger.error(f"Download failed for {url}: {str(e)}")
            raise