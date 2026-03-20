from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message


class PasswordScreen(Screen):
    """
    A modal screen that asks for a password before connecting.
    Only shown if no environment variable is set for the connection.
    """

    class PasswordSubmitted(Message):
        """Posted when the user submits a password."""
        def __init__(self, password: str) -> None:
            self.password = password
            super().__init__()

    DEFAULT_CSS = """
    PasswordScreen {
        align: center middle;
        background: $background 60%;
    }

    Vertical {
        width: 50;
        height: auto;
        border: solid $primary;
        padding: 1 2;
        background: $surface;
    }

    Label.password-title {
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }

    Label.password-hint {
        color: $text-muted;
        padding: 0 0 1 0;
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

    def __init__(self, connection_name: str) -> None:
        super().__init__()
        self.connection_name = connection_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Label("Password Required", classes="password-title")
            yield Label(
                f"Enter password for '{self.connection_name}'",
                classes="password-hint"
            )
            yield Label(
                "Tip: Set KERNDB_PASSWORD_"
                f"{self.connection_name.upper().replace(' ', '_')} "
                "to skip this prompt.",
                classes="password-hint"
            )
            yield Input(
                placeholder="password",
                password=True,
                id="password-input"
            )
            with Horizontal():
                yield Button("Connect", variant="primary", id="connect")
                yield Button("Cancel", variant="default", id="cancel")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "connect":
            self._submit()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def on_key(self, event) -> None:
        """Allow pressing Enter to submit."""
        if event.key == "enter":
            self._submit()

    def _submit(self) -> None:
        password = self.query_one("#password-input", Input).value
        self.dismiss(password)