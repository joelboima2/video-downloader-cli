import click
import os
import sys
from rich.console import Console
from .clipboard_monitor import ClipboardMonitor
from .config import Config
from .logger import setup_logger
from .ui import get_logo, clear_screen, display_status

logger = setup_logger()
console = Console()

@click.group()
@click.version_option()
def cli():
    """Video Downloader CLI - Monitor clipboard and download videos automatically"""
    pass

@cli.command()
@click.option('--output-dir', '-o', 
              type=click.Path(file_okay=False, dir_okay=True, writable=True),
              help='Directory to save downloaded videos')
@click.option('--manual-url', '-u', help='Manually provide a URL to download')
@click.option('--auto/--no-auto', default=True, 
              help='Enable/disable automatic clipboard monitoring')
@click.option('--quality', '-q', 
              type=click.Choice(['best', 'medium', '720p', '480p'], case_sensitive=False), 
              default='best',
              help='Video quality')
@click.option('--format', '-f',
              type=click.Choice(['mp4', 'webm', 'mkv'], case_sensitive=False),
              default='mp4',
              help='Output video format')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--quiet', is_flag=True, help='Suppress all output except errors')
@click.option('--progress/--no-progress', default=True, help='Show/hide progress bar')
@click.option('--download-archive', '-a',
              type=click.Path(file_okay=True, dir_okay=False),
              help='File to record all downloaded videos')
def start(output_dir, manual_url, auto, quality, format, verbose, quiet, progress, download_archive):
    """Start the video downloader with specified options"""
    try:
        if not quiet:
            clear_screen()
            console.print(get_logo())
            console.print("\nVideo Downloader CLI - Your Ultimate Video Download Assistant\n")

        config = Config()
        if output_dir:
            config.download_path = output_dir

        # Configure logging
        if verbose:
            logger.setLevel('DEBUG')
        elif quiet:
            logger.setLevel('ERROR')

        monitor_instance = ClipboardMonitor(config, {
            'quality': quality,
            'format': format,
            'show_progress': progress,
            'download_archive': download_archive
        })

        if manual_url:
            if not quiet:
                display_status("Processing manual URL...")
            monitor_instance.process_url(manual_url)
            return

        if auto:
            if not quiet:
                console.print("[cyan]Starting clipboard monitor. Press Ctrl+C to stop.")
                console.print("[green]Supported platforms: YouTube, Facebook, Twitter, Instagram\n")
            monitor_instance.start_monitoring()
        else:
            console.print("[yellow]Automatic monitoring disabled. Use --manual-url to download videos.[/]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down gracefully...[/]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        console.print(f"\n[red]Error: {str(e)}[/]")
        sys.exit(1)

def main():
    cli()

if __name__ == '__main__':
    main()