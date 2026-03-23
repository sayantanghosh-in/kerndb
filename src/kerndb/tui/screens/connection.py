from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Input, Button, Header
from textual.containers import Vertical, Horizontal


class ConnectionScreen(Screen):

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    ConnectionScreen {
        align: center middle;
    }

    #form-container {
        width: 56;
        height: auto;
        border: solid $primary;
        padding: 1 2;
        background: $surface;
    }

    #form-title {
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
        width: 100%;
    }

    #form-divider {
        height: 1;
        border-bottom: solid $primary;
        margin: 0 0 1 0;
    }

    .field-row {
        height: 3;
        margin-bottom: 1;
        align: left middle;
    }

    .field-label {
        width: 10;
        color: $text-muted;
        padding: 0 1 0 0;
    }

    .field-input {
        width: 1fr;
    }

    #form-actions {
        height: auto;
        margin-top: 1;
        align: right middle;
        border-top: solid $primary;
        padding-top: 1;
    }

    #form-actions Button {
        margin-left: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="form-container"):
            yield Label("New Connection", id="form-title")
            yield Label("", id="form-divider")

            with Horizontal(classes="field-row"):
                yield Label("Name", classes="field-label")
                yield Input(
                    placeholder="my-database",
                    id="name",
                    classes="field-input"
                )
            with Horizontal(classes="field-row"):
                yield Label("Host", classes="field-label")
                yield Input(
                    placeholder="localhost",
                    id="host",
                    classes="field-input"
                )
            with Horizontal(classes="field-row"):
                yield Label("Port", classes="field-label")
                yield Input(
                    placeholder="5432",
                    id="port",
                    classes="field-input"
                )
            with Horizontal(classes="field-row"):
                yield Label("User", classes="field-label")
                yield Input(
                    placeholder="postgres",
                    id="user",
                    classes="field-input"
                )
            with Horizontal(classes="field-row"):
                yield Label("Database", classes="field-label")
                yield Input(
                    placeholder="mydb",
                    id="database",
                    classes="field-input"
                )

            with Horizontal(id="form-actions"):
                yield Button("Save", variant="primary", id="connect")
                yield Button("Esc  Cancel", variant="default", id="cancel")

        yield Footer()

    def on_mount(self) -> None:
        self.app.sub_title = "Sayantan Ghosh  •  sayantanghosh.in  •  github.com/sayantanghosh-in"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "connect":
            self._handle_connect()
        elif event.button.id == "cancel":
            self.action_cancel()

    def action_cancel(self) -> None:
        self.app.pop_screen()

    def _handle_connect(self) -> None:
        from kerndb.config.settings import save_connection

        name = self.query_one("#name", Input).value.strip()
        host = self.query_one("#host", Input).value.strip()
        port = self.query_one("#port", Input).value.strip()
        user = self.query_one("#user", Input).value.strip()
        database = self.query_one("#database", Input).value.strip()

        if not all([name, host, port, user, database]):
            self.notify("Please fill in all fields", severity="error")
            return

        if not port.isdigit():
            self.notify("Port must be a number", severity="error")
            return

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
        self.app.switch_screen("picker")