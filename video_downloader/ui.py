from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
import shutil

def get_logo():
    """Return ASCII art logo with dynamic width scaling"""
    terminal_width = shutil.get_terminal_size().columns
    logo = """
    ╦  ╦╦╔═╗╔═╗╔═╗  ╔╦╗╔═╗╦ ╦╔╗╔╦  ╔═╗╔═╗╔╦╗╔═╗╦═╗
    ╚╗╔╝║╠╣ ║╣ ║ ║   ║║║ ║║║║║║║║  ║ ║╠═╣ ║║║╣ ╠╦╝
     ╚╝ ╩╚  ╚═╝╚═╝  ═╩╝╚═╝╚╩╝╝╚╝╩═╝╚═╝╩ ╩═╩╝╚═╝╩╚═
    """
    # Center the logo based on terminal width
    centered_logo = '\n'.join(line.center(terminal_width) for line in logo.split('\n'))
    return Panel(Text(centered_logo, style="bold cyan"))

def create_progress_bar():
    """Create a rich progress bar with enhanced visuals"""
    console = Console()
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        transient=False,  # Keep the progress bar visible
        expand=True,      # Use full width
    )
    return progress

def display_status(message, style="bold cyan"):
    """Display a status message in a panel"""
    console = Console()
    console.print(Panel(Text(message, style=style)))

def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")