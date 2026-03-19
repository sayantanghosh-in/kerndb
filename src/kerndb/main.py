import typer
from kerndb.tui.app import KernApp

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """kerndb — a beautiful terminal database client."""
    if ctx.invoked_subcommand is None:
        tui = KernApp()
        tui.run()

if __name__ == "__main__":
    app()