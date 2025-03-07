from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
import shutil
import pyfiglet

def get_logo():
    """Return ASCII art logo with dynamic width scaling"""
    terminal_width = shutil.get_terminal_size().columns

    # Create figlet logo with a cool font
    figlet = pyfiglet.Figlet(font='big')
    logo_text = figlet.renderText('Video DL')

    # Add a subtitle
    subtitle = "Download videos with ease!"

    # Center both logo and subtitle
    lines = logo_text.split('\n')
    styled_lines = []

    # Create gradient effect using different shades
    colors = ["cyan", "bright_cyan", "blue", "bright_blue"]
    for i, line in enumerate(lines):
        color = colors[min(i, len(colors)-1)]
        styled_line = Text(line.center(terminal_width), style=f"bold {color}")
        styled_lines.append(styled_line)

    # Join lines with gradient effect
    logo_content = Text("\n").join(styled_lines)

    # Add styled subtitle
    subtitle_text = Text("\n\n" + subtitle.center(terminal_width), 
                        style="bold magenta")

    # Combine logo and subtitle
    full_logo = logo_content + subtitle_text

    return Panel(
        full_logo,
        border_style="bright_blue",
        padding=(1, 2),
        subtitle="[bright_cyan]v1.0.0[/]"
    )

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