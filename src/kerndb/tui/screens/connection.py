from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, Input, Button
from textual.containers import Vertical, Horizontal


class ConnectionScreen(Screen):
    """
    The connection manager screen.
    Shown on first launch or when the user wants to add a new connection.
    """

    CSS = """
    ConnectionScreen {
        align: center middle;
    }

    Vertical {
        width: 60;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }

    Label {
        margin-bottom: 1;
    }

    Input {
        margin-bottom: 1;
    }

    Horizontal {
        height: auto;
        margin-top: 1;
    }

    Button {
        margin-right: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Label("New Connection", id="title")
            yield Label("Name")
            yield Input(placeholder="my-database", id="name")
            yield Label("Host")
            yield Input(placeholder="localhost", id="host")
            yield Label("Port")
            yield Input(placeholder="5432", id="port")
            yield Label("User")
            yield Input(placeholder="postgres", id="user")
            yield Label("Database")
            yield Input(placeholder="mydb", id="database")
            with Horizontal():
                yield Button("Connect", variant="primary", id="connect")
                yield Button("Cancel", variant="default", id="cancel")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles button clicks."""
        if event.button.id == "connect":
            self._handle_connect()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def _handle_connect(self) -> None:
        """
        Reads the form values, validates them,
        saves the connection and notifies the user.
        """
        from kerndb.config.settings import save_connection

        name = self.query_one("#name", Input).value.strip()
        host = self.query_one("#host", Input).value.strip()
        port = self.query_one("#port", Input).value.strip()
        user = self.query_one("#user", Input).value.strip()
        database = self.query_one("#database", Input).value.strip()

        # check all fields are filled
        if not all([name, host, port, user, database]):
            self.notify("Please fill in all fields", severity="error")
            return

        # validate port is a number
        if not port.isdigit():
            self.notify("Port must be a number", severity="error")
            return

        # validate port is in valid range
        if not (1 <= int(port) <= 65535):
            self.notify("Port must be between 1 and 65535", severity="error")
            return

        save_connection(name, {
            "type": "postgres",
            "host": host,
            "port": int(port),
            "user": user,
            "database": database,
        })

        self.notify(f"Connection '{name}' saved!", severity="information")
        self.app.pop_screen()
        self.app.navigate_to_home(name)