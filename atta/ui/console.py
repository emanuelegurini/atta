from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from atta.core.models import StudentStats

console = Console()

def print_banner():
    """Prints the application header."""
    console.print(Panel.fit(
        "[bold cyan]Atta[/bold cyan] - Attendance Tracker",
        subtitle="v0.1"
    ))

def print_stats_table(stats: StudentStats):
    """
    Renders the student statistics in a nice table.
    """
    table = Table(title=f"Report for Student: [bold green]{stats.student_id}[/bold green]")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Total Lessons", str(stats.total_lessons))
    table.add_row("Present", str(stats.present_count))
    
    # Color code the percentage
    perc_color = "green" if stats.percentage >= 70 else "red"
    table.add_row("Attendance Rate", f"[{perc_color}]{stats.percentage}%[/{perc_color}]")

    console.print(table)
    console.print("\n")

def show_loading(message: str):
    """Returns a status spinner context manager."""
    return console.status(f"[bold green]{message}[/bold green]", spinner="dots")

def print_error(message: str):
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_success(message: str):
    console.print(f"[bold green]Success:[/bold green] {message}")
