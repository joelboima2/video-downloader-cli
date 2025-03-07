# Video Downloader CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A command-line interface (CLI) tool that monitors your clipboard for video links and automatically downloads them. Supports YouTube, Facebook, Twitter, and Instagram videos.

## Features

- Automatic clipboard monitoring for video links
- Progress bar for download tracking
- Support for multiple video platforms
- Configurable download directory
- Cross-platform support (Windows, macOS, Linux)
- Multiple video quality options
- Custom output format selection
- Download history tracking

## Installation

### Prerequisites

#### Windows
No additional prerequisites required.

#### macOS
No additional prerequisites required.

#### Linux
Install xclip (required for clipboard functionality):
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora
sudo dnf install xclip

# Arch Linux
sudo pacman -S xclip
```

### Installing from Source

1. Clone the repository:
```bash
git clone https://github.com/joelboima2/video-downloader-cli.git
cd video-downloader-cli
```

2. Install the package:
```bash
pip install .
```

### Installing from PyPI
```bash
pip install video-downloader-cli
```

## Usage

### Basic Usage
```bash
video-downloader start
```

### Advanced Options
- `--output-dir`, `-o`: Specify custom download directory
- `--manual-url`, `-u`: Download a specific URL without clipboard monitoring
- `--auto/--no-auto`: Enable/disable automatic clipboard monitoring
- `--quality`, `-q`: Set video quality (best, medium, 720p, 480p)
- `--format`, `-f`: Choose output format (mp4, webm, mkv)
- `--verbose`, `-v`: Enable verbose logging
- `--quiet`, `-q`: Suppress all output except errors
- `--progress/--no-progress`: Show/hide progress bar
- `--download-archive`, `-a`: File to record downloaded videos

### Examples

1. Start monitoring with default settings:
```bash
video-downloader start
```

2. Download high-quality MP4:
```bash
video-downloader start -q best -f mp4
```

3. Manual download with specific quality:
```bash
video-downloader start -u https://youtube.com/watch?v=example -q 720p
```

4. Disable automatic monitoring:
```bash
video-downloader start --no-auto -u https://youtube.com/watch?v=example
```

5. Custom download directory with progress tracking:
```bash
video-downloader start -o ~/Videos --progress
```

### Handling YouTube Authentication

Some YouTube videos may require authentication. If you encounter a "Sign in to confirm you're not a bot" error, try these solutions:

1. Use Browser Cookies:
   - Install the yt-dlp browser extension
   - Export cookies from your browser (Chrome, Firefox, Safari, or Edge)
   - The tool will automatically try to use cookies from installed browsers
   - Make sure you're logged into YouTube in your browser

2. Alternative Solutions:
   - Try a different video URL
   - Use non-age-restricted videos
   - If using auto-monitoring, copy a different video URL

3. Troubleshooting Tips:
   - Clear browser cookies and log in to YouTube again
   - Try using a different browser
   - Ensure you have the latest version of yt-dlp installed


## Configuration

The application uses a `config.yaml` file for configuration. Default location is in the current directory.

Example configuration:
```yaml
download_path: ~/Downloads
supported_platforms:
  - youtube.com
  - youtu.be
  - facebook.com
  - fb.watch
  - twitter.com
  - instagram.com
```

## Development

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Troubleshooting

### Linux
If you encounter clipboard errors, ensure xclip is installed.

### Windows
No common issues reported.

### macOS
No common issues reported.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/joelboima2/video-downloader-cli/issues) on GitHub.