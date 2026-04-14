from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def print_header():
    """Print the AI-Brain header for commands."""
    console.print(Panel(
        "[bold cyan]🧠 AI-Brain[/bold cyan] - [dim]Persistent Long-Term Memory[/dim]",
        border_style="cyan"
    ))

def print_success(message: str):
    console.print(f"[bold green]✓[/bold green] {message}")

def print_info(message: str):
    console.print(f"[bold cyan]ℹ[/bold cyan] {message}")

def print_warning(message: str):
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")

def print_error(message: str):
    console.print(f"[bold red]✗[/bold red] {message}")

def print_markdown(markdown_content: str):
    md = Markdown(markdown_content)
    console.print(md)

def create_table(title: str, *columns):
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    return table

def render_table(table: Table):
    console.print(table)
