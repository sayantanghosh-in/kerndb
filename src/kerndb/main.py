import typer
from kerndb.tui.app import KernApp
from kerndb.cli import commands

# the root typer app
app = typer.Typer(
    help="kerndb — a beautiful terminal database client.",
    invoke_without_command=True,
    no_args_is_help=False,
)

# register all CLI commands from commands.py
# this makes `kerndb query`, `kerndb connections` etc. work
app.add_typer(commands.app, name="cli")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    kerndb — a beautiful terminal database client.

    Run without arguments to launch the interactive TUI.
    Use subcommands for scripting and automation.
    """
    if ctx.invoked_subcommand is None:
        # no subcommand given — launch the TUI
        tui = KernApp()
        tui.run()


if __name__ == "__main__":
    app()