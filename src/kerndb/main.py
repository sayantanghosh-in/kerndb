import typer
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

from kerndb.tui.app import KernApp
from kerndb.cli import commands

app = typer.Typer(
    help="kerndb — a beautiful terminal database client.",
    invoke_without_command=True,
    no_args_is_help=False,
)

app.add_typer(commands.app, name="cli")


def _check_for_updates() -> None:
    """
    Silently checks PyPI for a newer version.
    Never crashes or blocks — times out after 2 seconds.
    """
    try:
        import httpx
        import importlib.metadata
        from rich.console import Console

        installed = importlib.metadata.version("kerndb")
        response = httpx.get(
            "https://pypi.org/pypi/kerndb/json",
            timeout=2.0
        )
        latest = response.json()["info"]["version"]
        if latest != installed:
            Console().print(
                f"[dim]kerndb {latest} is available — "
                f"run: pip install --upgrade kerndb[/dim]"
            )
    except Exception:
        # never crash the app because of a version check
        pass


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """kerndb — a beautiful terminal database client."""
    if ctx.invoked_subcommand is None:
        _check_for_updates()
        tui = KernApp()
        tui.run()


if __name__ == "__main__":
    app()