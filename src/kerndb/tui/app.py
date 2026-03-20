from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label

from kerndb.tui.screens.picker import ConnectionPickerScreen
from kerndb.tui.screens.connection import ConnectionScreen
from kerndb.tui.screens.password import PasswordScreen


class KernApp(App):
    """The root Textual application class for kerndb."""

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    SCREENS = {
        "picker": ConnectionPickerScreen,
        "connection": ConnectionScreen,
        "password": PasswordScreen,
    }

    CSS_PATH = "../tui/styles/app.tcss"

    def on_mount(self) -> None:
        self.title = "kerndb"
        self.sub_title = "terminal database client"
        self.push_screen("picker")

    def navigate_to_home(
        self,
        connection_name: str,
        password: str = ""
    ) -> None:
        """
        Navigates to the home screen with a specific connection.
        Password is passed directly if provided via the prompt.
        """
        from kerndb.tui.screens.home import HomeScreen
        self.push_screen(HomeScreen(connection_name, password))