import re
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, Button, ListView, ListItem
from textual.containers import Vertical, Horizontal


def _slugify(name: str) -> str:
    """
    Converts a connection name to a valid Textual widget ID.
    Replaces any character that isn't a letter, number,
    underscore, or hyphen with an underscore.
    Example: "Dummy 1" -> "Dummy_1"
    """
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


class ConnectionPickerScreen(Screen):
    """
    Shown on every launch.
    Lists saved connections and lets the user pick one or add a new one.
    """

    DEFAULT_CSS = """
    ConnectionPickerScreen {
        align: center middle;
    }

    Vertical {
        width: 60;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }

    Label.picker-title {
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }

    Label.picker-empty {
        color: $text-muted;
        padding: 1 0;
    }

    ListView {
        height: auto;
        max-height: 15;
        border: solid $surface;
        margin-bottom: 1;
    }

    ListItem {
        padding: 0 1;
    }

    Horizontal {
        height: auto;
        margin-top: 1;
    }

    Button {
        margin-right: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        # maps slug -> original name so we can look up the
        # real connection name when a list item is selected
        self._slug_to_name: dict = {}

    def compose(self) -> ComposeResult:
        from kerndb.config.settings import get_all_connections
        connections = get_all_connections()

        # build the slug map fresh every time compose runs
        self._slug_to_name = {
            _slugify(name): name
            for name in connections.keys()
        }

        yield Header()
        with Vertical():
            yield Label("kerndb", classes="picker-title")
            if not connections:
                yield Label(
                    "No saved connections. Add one to get started.",
                    classes="picker-empty"
                )
            else:
                yield Label("Select a connection:")
                yield ListView(
                    *[
                        ListItem(Label(name), id=f"conn-{_slugify(name)}")
                        for name in connections.keys()
                    ],
                    id="connection-list"
                )
            with Horizontal():
                yield Button("Add New", variant="primary", id="add-new")
                yield Button("Quit", variant="default", id="quit")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """User clicked a saved connection — connect to it."""
        if event.item.id is None:
            return

        slug = event.item.id.replace("conn-", "", 1)
        original_name = self._slug_to_name.get(slug)

        if original_name is None:
            self.notify("Connection not found", severity="error")
            return

        from kerndb.config.settings import get_password
        password = get_password(original_name)

        if password is None:
            # no env variable set — ask for password via modal
            from kerndb.tui.screens.password import PasswordScreen
            self.app.push_screen(
                PasswordScreen(original_name),
                callback=lambda pwd: self.app.navigate_to_home(original_name, pwd)
            )
        else:
            # env variable exists — connect directly
            self.app.navigate_to_home(original_name, password)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-new":
            self.app.push_screen("connection")
        elif event.button.id == "quit":
            self.app.exit()