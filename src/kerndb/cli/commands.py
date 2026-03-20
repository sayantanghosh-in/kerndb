from typing import Optional
import typer

from kerndb.cli.formatters import (
    print_results,
    print_connections,
    print_error,
    print_success,
    export_to_csv,
)
from kerndb.config.settings import (
    get_all_connections,
    get_connection,
    get_password,
    save_connection,
    delete_connection,
)

app = typer.Typer(help="kerndb CLI — power user commands.")


@app.command()
def query(
    sql: str = typer.Argument(..., help="SQL query to run"),
    connection: str = typer.Option("", "--connection", "-c", help="Saved connection name"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export results to CSV file"),
) -> None:
    """Run a SQL query against a saved connection."""
    if not connection:
        print_error("Please provide a connection name with --connection")
        raise typer.Exit(1)

    config = get_connection(connection)
    if config is None:
        print_error(f"Connection '{connection}' not found.")
        print_error("Run 'kerndb connections' to see saved connections.")
        raise typer.Exit(1)

    from kerndb.connectors.postgres import PostgresConnector
    connector = PostgresConnector()

    try:
        password = get_password(connection)
        config_with_password = {**config, "password": password or ""}
        connector.connect(config_with_password)
        results = connector.execute(sql)

        if export:
            export_to_csv(results, export)
        else:
            print_results(results)

    except ConnectionError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)
    finally:
        connector.disconnect()


@app.command()
def connections() -> None:
    """List all saved database connections."""
    all_connections = get_all_connections()
    print_connections(all_connections)


@app.command()
def save(
    name: str = typer.Argument(..., help="Name for this connection"),
    host: str = typer.Option("localhost", "--host", help="Database host"),
    port: int = typer.Option(5432, "--port", help="Database port"),
    user: str = typer.Option(..., "--user", "-u", help="Database user"),
    database: str = typer.Option(..., "--database", "-d", help="Database name"),
) -> None:
    """Save a new database connection."""
    save_connection(name, {
        "type": "postgres",
        "host": host,
        "port": port,
        "user": user,
        "database": database,
    })
    print_success(f"Connection '{name}' saved.")
    print_success(f"Set password with: $env:KERNDB_PASSWORD_{name.upper()}='yourpassword'")


@app.command()
def remove(
    name: str = typer.Argument(..., help="Connection name to remove"),
) -> None:
    """Remove a saved database connection."""
    config = get_connection(name)
    if config is None:
        print_error(f"Connection '{name}' not found.")
        raise typer.Exit(1)

    delete_connection(name)
    print_success(f"Connection '{name}' removed.")