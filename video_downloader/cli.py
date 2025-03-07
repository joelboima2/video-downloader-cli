import click
import os
import sys
from rich.console import Console
from .clipboard_monitor import ClipboardMonitor
from .config import Config
from .logger import setup_logger
from .ui import get_logo, clear_screen

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
@click.option('--monitor/--no-monitor', default=True, 
              help='Enable/disable clipboard monitoring')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def start(output_dir, manual_url, monitor, verbose):
    """Start the video downloader"""
    try:
        clear_screen()
        console.print(get_logo())
        console.print("\nVideo Downloader CLI - Your Ultimate Video Download Assistant\n")

        config = Config()
        if output_dir:
            config.download_path = output_dir

        if verbose:
            logger.setLevel('DEBUG')

        monitor_instance = ClipboardMonitor(config)

        if manual_url:
            console.print("\nProcessing manual URL...")
            monitor_instance.process_url(manual_url)
            return

        if monitor:
            console.print("[cyan]Starting clipboard monitor. Press Ctrl+C to stop.")
            console.print("[green]Supported platforms: YouTube, Facebook, Twitter, Instagram\n")
            monitor_instance.start_monitoring()

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