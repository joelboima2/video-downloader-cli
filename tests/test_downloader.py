import unittest
from unittest.mock import MagicMock, patch
from video_downloader.downloader import VideoDownloader
from video_downloader.clipboard_monitor import ClipboardMonitor
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

    def test_duplicate_download_prevention(self):
        """Test that the same URL is not downloaded twice"""
        test_url = "https://youtube.com/watch?v=abc123"

        # First download should process normally
        with patch('yt_dlp.YoutubeDL') as mock_ytdl:
            mock_ytdl_instance = MagicMock()
            mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
            self.downloader.download(test_url)
            mock_ytdl_instance.download.assert_called_once()

        # Second download should be skipped
        with patch('yt_dlp.YoutubeDL') as mock_ytdl:
            mock_ytdl_instance = MagicMock()
            mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
            self.downloader.download(test_url)
            mock_ytdl_instance.download.assert_not_called()

class TestClipboardMonitor(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.monitor = ClipboardMonitor(self.config)

    def test_duplicate_url_handling(self):
        """Test that duplicate URLs are not processed twice"""
        test_content = "Check out https://youtube.com/watch?v=abc123"

        # Mock the downloader to track calls
        self.monitor.downloader.download = MagicMock()

        # First processing should trigger download
        self.monitor.process_clipboard_content(test_content)
        self.monitor.downloader.download.assert_called_once()

        # Reset mock to verify second call
        self.monitor.downloader.download.reset_mock()

        # Second processing should not trigger download
        self.monitor.process_clipboard_content(test_content)
        self.monitor.downloader.download.assert_not_called()

    def test_multiple_urls_duplicate_handling(self):
        """Test handling multiple URLs with duplicates"""
        test_content = """
        First video: https://youtube.com/watch?v=abc123
        Second video: https://youtube.com/watch?v=def456
        Same as first: https://youtube.com/watch?v=abc123
        """

        # Mock the downloader
        self.monitor.downloader.download = MagicMock()

        # Process content
        self.monitor.process_clipboard_content(test_content)

        # Should only download unique URLs
        self.assertEqual(self.monitor.downloader.download.call_count, 2)

if __name__ == '__main__':
    unittest.main()