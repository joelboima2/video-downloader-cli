import click
import os
import sys
from .clipboard_monitor import ClipboardMonitor
from .config import Config
from .logger import setup_logger

logger = setup_logger()

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
        config = Config()
        if output_dir:
            config.download_path = output_dir
        
        if verbose:
            logger.setLevel('DEBUG')
        
        monitor_instance = ClipboardMonitor(config)
        
        if manual_url:
            monitor_instance.process_url(manual_url)
            return
            
        if monitor:
            click.echo("Starting clipboard monitor. Press Ctrl+C to stop.")
            monitor_instance.start_monitoring()
        
    except KeyboardInterrupt:
        click.echo("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

def main():
    cli()

if __name__ == '__main__':
    main()
