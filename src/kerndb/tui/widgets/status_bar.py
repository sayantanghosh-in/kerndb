from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label
from textual.containers import Horizontal
from textual.reactive import reactive


class StatusBar(Widget):
    """
    The bottom status bar widget.
    Shows the current connection name, database type, and status.
    Updates reactively when the connection state changes.
    """

    # reactive variables — changing these auto-updates the UI
    connection_name: reactive[str] = reactive("")
    is_connected: reactive[bool] = reactive(False)
    active_table: reactive[str] = reactive("")
    row_count: reactive[int] = reactive(0)

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: $primary;
        color: $background;
        padding: 0 1;
    }

    StatusBar Horizontal {
        height: 1;
    }

    StatusBar Label {
        margin-right: 2;
    }

    StatusBar Label.status-connected {
        color: $success;
    }

    StatusBar Label.status-disconnected {
        color: $error;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("", id="status-connection")
            yield Label("", id="status-table")
            yield Label("", id="status-rows")

    def on_mount(self) -> None:
        """Render initial state on mount."""
        self._refresh_labels()

    def update_connection(self, name: str, connected: bool) -> None:
        """
        Called by HomeScreen after connecting to a database.
        Updates the connection name and status.
        """
        self.connection_name = name
        self.is_connected = connected
        self._refresh_labels()

    def update_table(self, table: str) -> None:
        """
        Called by HomeScreen when the user selects a table.
        Updates the active table name.
        """
        self.active_table = table
        self._refresh_labels()

    def update_row_count(self, count: int) -> None:
        """
        Called by HomeScreen after a query runs.
        Updates the row count shown in the status bar.
        """
        self.row_count = count
        self._refresh_labels()

    def _refresh_labels(self) -> None:
        """
        Private method that updates all three labels at once.
        Called whenever any state changes.
        """
        # connection label
        connection_label = self.query_one("#status-connection", Label)
        if self.is_connected:
            status = "● connected"
            connection_label.remove_class("status-disconnected")
            connection_label.add_class("status-connected")
        else:
            status = "○ disconnected"
            connection_label.remove_class("status-connected")
            connection_label.add_class("status-disconnected")

        connection_text = (
            f"{self.connection_name}  {status}"
            if self.connection_name
            else status
        )
        connection_label.update(connection_text)

        # active table label
        table_label = self.query_one("#status-table", Label)
        table_text = f"table: {self.active_table}" if self.active_table else ""
        table_label.update(table_text)

        # row count label
        rows_label = self.query_one("#status-rows", Label)
        rows_text = f"{self.row_count:,} rows" if self.row_count else ""
        rows_label.update(rows_text)