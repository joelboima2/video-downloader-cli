import unittest
from unittest.mock import MagicMock, patch
from video_downloader.downloader import VideoDownloader
from video_downloader.config import Config

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.downloader = VideoDownloader(self.config)
    
    @patch('yt_dlp.YoutubeDL')
    def test_download_success(self, mock_ytdl):
        # Mock the YoutubeDL instance
        mock_ytdl_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
        
        test_url = "https://youtube.com/watch?v=test123"
        self.downloader.download(test_url)
        
        # Verify download was called
        mock_ytdl_instance.download.assert_called_once_with([test_url])
    
    @patch('yt_dlp.YoutubeDL')
    def test_download_failure(self, mock_ytdl):
        # Mock YoutubeDL to raise an exception
        mock_ytdl.return_value.__enter__.return_value.download.side_effect = Exception("Download failed")
        
        test_url = "https://youtube.com/watch?v=test123"
        
        with self.assertRaises(Exception):
            self.downloader.download(test_url)

if __name__ == '__main__':
    unittest.main()
