import unittest
from video_downloader.url_validator import URLValidator

class TestURLValidator(unittest.TestCase):
    def setUp(self):
        self.validator = URLValidator()
    
    def test_extract_urls(self):
        text = "Check out this video https://youtube.com/watch?v=123 and this one https://fb.watch/abc"
        urls = self.validator.extract_urls(text)
        self.assertEqual(len(urls), 2)
        self.assertIn("https://youtube.com/watch?v=123", urls)
        self.assertIn("https://fb.watch/abc", urls)
    
    def test_supported_video_url(self):
        valid_urls = [
            "https://www.youtube.com/watch?v=123",
            "https://youtu.be/123",
            "https://facebook.com/videos/123",
            "https://fb.watch/abc",
        ]
        
        invalid_urls = [
            "https://example.com/video",
            "not_a_url",
            "http://invalid url.com",
        ]
        
        for url in valid_urls:
            self.assertTrue(self.validator.is_supported_video_url(url))
            
        for url in invalid_urls:
            self.assertFalse(self.validator.is_supported_video_url(url))

if __name__ == '__main__':
    unittest.main()
