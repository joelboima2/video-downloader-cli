import yt_dlp
from tqdm import tqdm
import os
import hashlib
from .logger import setup_logger

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
            logger.info(f"Video already downloaded: {url}")
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
                if hasattr(self, 'pbar'):
                    self.pbar.update(percentage - self.pbar.n)

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.config.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
        }

        try:
            # Create progress bar
            self.pbar = tqdm(total=100, desc='Downloading', unit='%')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Starting download: {url}")
                ydl.download([url])

            self.pbar.close()
            logger.info(f"Download completed: {url}")
            self.downloaded_urls.add(video_id)

        except Exception as e:
            if hasattr(self, 'pbar'):
                self.pbar.close()
            logger.error(f"Download failed for {url}: {str(e)}")
            raise