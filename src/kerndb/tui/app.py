from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label

class KernApp(App):
    """
    The root Textual application class for kerndb.
    This is the entry point for the entire TUI.
    """

    CSS = """
    Screen {
        align: center middle;
    }

    Label {
        padding: 1 2;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Welcome to kerndb. Press Q to quit.")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "kerndb"
        self.sub_title = "terminal database client"