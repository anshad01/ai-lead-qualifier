from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich import print as rprint

console = Console()


def get_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )


def print_summary_table(results: list) -> None:
    table = Table(title="Lead Qualification Results", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Company", style="white")
    table.add_column("Score", justify="center")
    table.add_column("Tier", justify="center")
    table.add_column("Action", style="green")

    for r in results:
        tier_color = "red" if r.tier == "Hot" else "yellow" if r.tier == "Warm" else "blue"
        table.add_row(
            r.name,
            r.company,
            str(r.lead_score),
            f"[{tier_color}]{r.tier}[/{tier_color}]",
            r.recommended_action,
        )

    console.print(table)


def log_info(msg: str) -> None:
    console.print(f"[bold green]INFO[/bold green] {msg}")


def log_error(msg: str) -> None:
    console.print(f"[bold red]ERROR[/bold red] {msg}")