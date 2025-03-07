# Video Downloader CLI

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

### Installing the Package

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

## Troubleshooting

### Linux
If you encounter clipboard errors, ensure xclip is installed.

### Windows
No common issues reported.

### macOS
No common issues reported.

## License

MIT License
