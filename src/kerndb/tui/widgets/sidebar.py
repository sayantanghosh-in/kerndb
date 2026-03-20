from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label
from textual.message import Message


class Sidebar(Widget):
    """
    The left sidebar widget.
    Shows a list of all tables in the connected database.
    When a table is clicked it posts a TableSelected message
    which HomeScreen listens for.
    """

    # nested class — defines the message this widget can post
    class TableSelected(Message):
        """Posted when the user selects a table from the sidebar."""
        def __init__(self, table: str) -> None:
            self.table = table
            super().__init__()

    DEFAULT_CSS = """
    Sidebar {
        width: 25%;
        height: 100%;
        border-right: solid $primary;
        padding: 0 1;
    }

    Sidebar Label.sidebar-title {
        text-style: bold;
        padding: 1 0;
        color: $accent;
    }

    Sidebar ListView {
        height: 1fr;
        border: none;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Tables", classes="sidebar-title")
        yield ListView(id="table-list")

    def update_tables(self, tables: list) -> None:
        """
        Called by HomeScreen after fetching tables from the DB.
        Clears the list and repopulates it with the new table names.
        """
        list_view = self.query_one("#table-list", ListView)
        list_view.clear()

        if not tables:
            list_view.append(ListItem(Label("No tables found")))
            return

        for table in tables:
            list_view.append(ListItem(Label(table), id=f"table-{table}"))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Fires when the user clicks or presses Enter on a list item.
        Extracts the table name and posts a TableSelected message.
        """
        if event.item.id is None:
            return

        # id is "table-users" so we strip the "table-" prefix
        table_name = event.item.id.replace("table-", "", 1)
        self.post_message(self.TableSelected(table_name))