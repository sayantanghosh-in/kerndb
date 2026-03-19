from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label
from kerndb.tui.screens.connection import ConnectionScreen
from kerndb.config.settings import get_all_connections


class KernApp(App):
    """
    The root Textual application class for kerndb.
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "show_connection", "New Connection"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Welcome to kerndb — press C to add a connection.")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "kerndb"
        self.sub_title = "terminal database client"
        connections = get_all_connections()
        if not connections:
            self.push_screen(ConnectionScreen())

    def action_show_connection(self) -> None:
        """Opens the connection manager screen."""
        self.push_screen(ConnectionScreen())