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

### Start Monitoring Clipboard
```bash
video-downloader start
```

### Options
- `--output-dir`, `-o`: Specify custom download directory
- `--manual-url`, `-u`: Download a specific URL without clipboard monitoring
- `--no-monitor`: Disable clipboard monitoring
- `--verbose`, `-v`: Enable verbose logging

### Examples

1. Start monitoring with default settings:
```bash
video-downloader start
```

2. Specify custom download directory:
```bash
video-downloader start -o ~/Videos
```

3. Download a specific URL:
```bash
video-downloader start -u https://youtube.com/watch?v=example
```

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