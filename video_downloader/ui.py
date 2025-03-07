from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
import shutil

def get_logo():
    """Return ASCII art logo with dynamic width scaling and enhanced styling"""
    terminal_width = shutil.get_terminal_size().columns
    # Enhanced ASCII art logo with more detail
    logo = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃   ╦  ╦╦╔═╗╔═╗╔═╗  ╔╦╗╔═╗╦ ╦╔╗╔╦  ╔═╗╔═╗╔╦╗╔═╗╦═╗ ┃
    ┃   ╚╗╔╝║╠╣ ║╣ ║ ║   ║║║ ║║║║║║║║  ║ ║╠═╣ ║║║╣ ╠╦╝ ┃
    ┃    ╚╝ ╩╚  ╚═╝╚═╝  ═╩╝╚═╝╚╩╝╝╚╝╩═╝╚═╝╩ ╩═╩╝╚═╝╩╚═ ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """

    # Sub-title with gradient effect
    subtitle = """
         🎥 Download Any Video with Style and Ease 🎥
    """

    # Center both logo and subtitle
    centered_logo = '\n'.join(line.center(terminal_width) for line in logo.split('\n'))
    centered_subtitle = subtitle.center(terminal_width)

    # Create a panel with gradient border
    return Panel(
        Text.assemble(
            Text(centered_logo, style="bold cyan"),
            Text("\n"),
            Text(centered_subtitle, style="bold magenta"),
        ),
        border_style="blue",
        title="[bold yellow]Video Downloader CLI[/]",
        subtitle="[bold green]v1.0.0[/]"
    )

def create_progress_bar():
    """Create a rich progress bar with enhanced visuals"""
    console = Console()
    progress = Progress(
        SpinnerColumn(style="green"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(
            complete_style="green",
            finished_style="bold green",
            pulse_style="yellow"
        ),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        transient=False,  # Keep the progress bar visible
        expand=True,      # Use full width
    )
    return progress

def display_status(message, style="bold cyan"):
    """Display a status message in a styled panel"""
    console = Console()
    panel = Panel(
        Text(message, style=style),
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)

def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")