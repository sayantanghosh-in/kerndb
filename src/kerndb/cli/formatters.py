from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()


def print_results(results: list) -> None:
    """
    Prints query results as a formatted table in the terminal.
    Used by CLI commands — not the TUI.
    Uses rich for formatting.
    """
    if not results:
        console.print("[yellow]No results returned.[/yellow]")
        return

    # get column names from the first row
    columns = list(results[0].keys())

    # create a rich Table
    table = Table(show_header=True, header_style="bold cyan")

    # add a row number column
    table.add_column("#", style="dim", width=4)

    # add a column for each field in the results
    for column in columns:
        table.add_column(column)

    # add rows using enumerate for row numbers
    for index, row in enumerate(results, start=1):
        values = [str(index)] + [str(v) for v in row.values()]
        table.add_row(*values)

    console.print(table)
    console.print(f"[dim]{len(results)} rows returned[/dim]")


def print_connections(connections: dict) -> None:
    """
    Prints all saved connections as a formatted table.
    """
    if not connections:
        console.print("[yellow]No saved connections found.[/yellow]")
        console.print("Run [bold]kerndb[/bold] to add one.")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Name", style="bold")
    table.add_column("Host")
    table.add_column("Port")
    table.add_column("Database")
    table.add_column("User")

    for name, config in connections.items():
        table.add_row(
            name,
            config.get("host", ""),
            str(config.get("port", "")),
            config.get("database", ""),
            config.get("user", ""),
        )

    console.print(table)


def print_error(message: str) -> None:
    """Prints a formatted error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Prints a formatted success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def export_to_csv(results: list, filepath: str) -> None:
    """
    Exports query results to a CSV file.
    Uses Python's built-in csv module — no extra dependency needed.
    """
    import csv

    if not results:
        print_error("No results to export.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print_success(f"Exported {len(results)} rows to {filepath}")