import re
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, ListView, ListItem, Label, Button, Header
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive


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
        ("d", "delete_connection", "Delete"),
        ("q", "quit", "Quit"),
    ]

    # tracks which connection is currently highlighted
    _highlighted: reactive[str] = reactive("")
    # tracks if user has pressed D once already (confirmation)
    _pending_delete: reactive[str] = reactive("")

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
        max-height: 6;
        border: solid $primary;
        margin: 0 0 0 0;
    }

    ListView > ListItem {
        height: 1;
        padding: 0 0;
        border-left: solid transparent;
    }

    ListView > ListItem Horizontal {
        height: 1;
        align: left middle;
    }

    ListView > ListItem .conn-name {
        height: 1;
        width: 1fr;
        padding: 0 1;
        color: $accent;
    }

    ListView > ListItem.--highlight .conn-name {
        color: $accent;
        text-style: bold;
    }

    ListView > ListItem .delete-hint {
        height: 1;
        width: auto;
        padding: 0 1;
        color: transparent;
    }

    ListView > ListItem:hover {
        background: $accent;
        color: $background;
    }

    ListView > ListItem:hover .delete-hint {
        color: $error;
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
        height: 1;
        border: none;
        min-width: 16;
        padding: 0 1;
    }

    #add-new {
        background: $primary;
        color: $background;
    }

    #add-new:hover {
        background: $accent;
        color: $background;
    }

    #quit-btn {
        background: transparent;
        color: $text-muted;
    }

    #quit-btn:hover {
        color: $accent;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._slug_to_name: dict = {}

    def on_mount(self) -> None:
        try:
            import importlib.metadata
            version = importlib.metadata.version("kerndb")
        except Exception:
            version = "dev"

        self.app.sub_title = (
            f"v{version}  •  Sayantan Ghosh  •  sayantanghosh.in"
            "  •  github.com/sayantanghosh-in/kerndb"
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
                            Horizontal(
                                Label(f"  {name}", classes="conn-name"),
                                Label("[D] delete", classes="delete-hint"),
                            ),
                            id=f"conn-{_slugify(name)}"
                        )
                        for name in connections.keys()
                    ],
                    id="connection-list"
                )
                yield Label(
                    "↑ ↓ navigate   enter connect   d delete   n new   q quit",
                    id="hint-label"
                )

            with Horizontal(id="picker-actions"):
                yield Button("▶ N  New Connection", id="add-new")
                yield Button("✕ Q  Quit", id="quit-btn")

        yield Footer()

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """
        Fires when the highlighted item changes via keyboard or mouse.
        Tracks which connection is currently highlighted for delete.
        """
        if event.item and event.item.id:
            slug = event.item.id.replace("conn-", "", 1)
            self._highlighted = self._slug_to_name.get(slug, "")
            # reset pending delete when navigation changes
            self._pending_delete = ""

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Fires when user presses Enter on a connection."""
        if event.item.id is None:
            return
        slug = event.item.id.replace("conn-", "", 1)
        original_name = self._slug_to_name.get(slug)
        if original_name is None:
            self.notify("Connection not found", severity="error")
            return
        self._connect(original_name)

    def _connect(self, name: str) -> None:
        """Handles connecting to a saved connection."""
        from kerndb.config.settings import get_password
        password = get_password(name)
        if password is None:
            from kerndb.tui.screens.password import PasswordScreen
            self.app.push_screen(
                PasswordScreen(name),
                callback=lambda pwd: self.app.navigate_to_home(name, pwd)
            )
        else:
            self.app.navigate_to_home(name, password)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-new":
            self.action_add_new()
        elif event.button.id == "quit-btn":
            self.app.exit()

    def action_add_new(self) -> None:
        self.app.push_screen("connection")

    def action_quit(self) -> None:
        self.app.exit()

    def action_delete_connection(self) -> None:
        """
        First D press — show confirmation toast.
        Second D press on same item — delete it.
        Navigating away resets the confirmation.
        """
        if not self._highlighted:
            return

        if self._pending_delete == self._highlighted:
            # second D press — confirmed, delete it
            from kerndb.config.settings import delete_connection
            delete_connection(self._highlighted)
            self.notify(
                f"'{self._highlighted}' deleted",
                severity="information"
            )
            self._pending_delete = ""
            # refresh the picker with a fresh instance
            from kerndb.tui.screens.picker import ConnectionPickerScreen
            self.app.switch_screen(ConnectionPickerScreen())
        else:
            # first D press — ask for confirmation
            self._pending_delete = self._highlighted
            self.notify(
                f"Press D again to delete '{self._highlighted}'",
                severity="warning"
            )