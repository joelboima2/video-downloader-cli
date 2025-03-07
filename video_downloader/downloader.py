import yt_dlp
import os
import hashlib
from .logger import setup_logger
from .ui import create_progress_bar, display_status
from rich.progress import Progress, TaskID

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

        # Create progress bar with spinner and time remaining
        progress = create_progress_bar()
        download_task = None

        def progress_hook(d):
            """Handle download progress updates"""
            nonlocal download_task
            try:
                if d['status'] == 'downloading':
                    # Initialize download task if needed
                    if download_task is None:
                        download_task = progress.add_task(
                            description=f"[cyan]Downloading {url}",
                            total=100.0,
                            completed=0.0
                        )
                        logger.debug("Created download task")

                    # Calculate and update progress
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes', d.get('total_bytes_estimate', 0))

                    if total > 0:
                        percentage = min((downloaded / total) * 100, 100.0)
                        logger.debug(f"Download progress: {percentage:.1f}%")
                        progress.update(
                            task_id=download_task,
                            completed=percentage
                        )

                elif d['status'] == 'finished' and download_task is not None:
                    logger.debug("Download finished, setting progress to 100%")
                    progress.update(download_task, completed=100.0)

            except Exception as e:
                logger.error(f"Progress hook error: {str(e)}")
                logger.debug(f"Progress state: {d}")

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,  # Let us handle the output
        }

        try:
            display_status(f"Starting download: {url}")

            # Ensure progress bar is visible during download
            with progress:
                logger.debug("Starting download with yt-dlp")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            display_status(f"Successfully downloaded: {url}", style="bold green")
            self.downloaded_urls.add(video_id)

        except Exception as e:
            display_status(f"Failed to download: {url}\nError: {str(e)}", style="bold red")
            logger.error(f"Download failed for {url}: {str(e)}")
            raise