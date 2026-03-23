import re
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, ListView, ListItem, Label, Button, Header
from textual.containers import Vertical, Horizontal


def _slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


ASCII_ART = """
 ██╗  ██╗███████╗██████╗ ███╗   ██╗██████╗ ██████╗
 ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗
 █████╔╝ █████╗  ██████╔╝██╔██╗ ██║██║  ██║██████╔╝
 ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██║  ██║██╔══██╗
 ██║  ██╗███████╗██║  ██║██║ ╚████║██████╔╝██████╔╝
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═════╝
"""


class ConnectionPickerScreen(Screen):

    BINDINGS = [
        ("n", "add_new", "New Connection"),
        ("q", "quit", "Quit"),
    ]

    DEFAULT_CSS = """
    ConnectionPickerScreen {
        align: center middle;
    }

    #picker-container {
        width: 64;
        height: auto;
        padding: 2 3;
        border: solid $primary;
        background: $surface;
    }

    #ascii-art {
        color: $accent;
        text-align: center;
        width: 100%;
        height: auto;
        padding: 0 0 1 0;
    }

    #tagline {
        text-align: center;
        color: $text-muted;
        width: 100%;
        padding: 0 0 2 0;
    }

    #connections-label {
        color: $text-muted;
        padding: 0 0 0 0;
        text-style: bold;
    }

    #connection-list {
        height: auto;
        max-height: 8;
        border: solid $primary;
        margin: 0 0 0 0;
    }

    ListView > ListItem {
        padding: 0 1;
        border-left: solid transparent;
    }

    ListView > ListItem:hover {
        background: $accent;
        color: $background;
    }

    ListView > ListItem.--highlight {
        background: $primary;
        color: $background;
        border-left: solid $accent;
    }

    #hint-label {
        text-align: center;
        color: $text-muted;
        width: 100%;
        padding: 1 0 0 0;
    }

    #no-connections {
        color: $text-muted;
        padding: 1;
        text-align: center;
        border: solid $surface;
        margin-bottom: 1;
    }

    #picker-actions {
        height: auto;
        align: center middle;
        padding-top: 1;
    }

    #picker-actions Button {
        margin: 0 1;
        min-width: 20;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._slug_to_name: dict = {}

    def on_mount(self) -> None:
        self.app.sub_title = (
            "Sayantan Ghosh  •  sayantanghosh.in"
            "  •  github.com/sayantanghosh-in"
        )

    def compose(self) -> ComposeResult:
        from kerndb.config.settings import get_all_connections

        connections = get_all_connections()
        self._slug_to_name = {
            _slugify(name): name
            for name in connections.keys()
        }

        yield Header()
        with Vertical(id="picker-container"):
            yield Label(ASCII_ART, id="ascii-art")
            yield Label(
                "minimal terminal database client",
                id="tagline"
            )

            if not connections:
                yield Label(
                    "No connections yet — press N to add one.",
                    id="no-connections"
                )
            else:
                yield Label("Saved connections", id="connections-label")
                yield ListView(
                    *[
                        ListItem(
                            Label(f"  {name}"),
                            id=f"conn-{_slugify(name)}"
                        )
                        for name in connections.keys()
                    ],
                    id="connection-list"
                )
                yield Label(
                    "↑ ↓ navigate   enter connect   n new   q quit",
                    id="hint-label"
                )

            with Horizontal(id="picker-actions"):
                yield Button(
                    "N  New Connection",
                    variant="primary",
                    id="add-new"
                )
                yield Button(
                    "Q  Quit",
                    variant="default",
                    id="quit"
                )

        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
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
            from kerndb.tui.screens.password import PasswordScreen
            self.app.push_screen(
                PasswordScreen(original_name),
                callback=lambda pwd: self.app.navigate_to_home(
                    original_name, pwd
                )
            )
        else:
            self.app.navigate_to_home(original_name, password)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-new":
            self.action_add_new()
        elif event.button.id == "quit":
            self.app.exit()

    def action_add_new(self) -> None:
        self.app.push_screen("connection")

    def action_quit(self) -> None:
        self.app.exit()