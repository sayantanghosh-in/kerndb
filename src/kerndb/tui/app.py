from textual.app import App

from kerndb.tui.screens.picker import ConnectionPickerScreen
from kerndb.tui.screens.connection import ConnectionScreen
from kerndb.tui.screens.password import PasswordScreen


class KernApp(App):

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    SCREENS = {
        "connection": ConnectionScreen,
        "password": PasswordScreen,
    }

    CSS_PATH = "../tui/styles/app.tcss"

    def on_mount(self) -> None:
        self.title = "kerndb"
        self.push_screen(ConnectionPickerScreen())

    def navigate_to_home(self, connection_name: str, password: str = "") -> None:
        from kerndb.tui.screens.home import HomeScreen
        self.push_screen(HomeScreen(connection_name, password))