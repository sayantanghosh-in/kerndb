from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea, Button, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message


class QueryEditor(Widget):
    """
    The SQL query editor widget.
    Contains a text area for writing SQL and a Run button.
    When the user runs a query it posts a QuerySubmitted message
    which HomeScreen listens for and executes.
    """

    # nested message class — posted when user runs a query
    class QuerySubmitted(Message):
        """Posted when the user submits a query to run."""
        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()

    # class variable — the placeholder text shown in the editor
    PLACEHOLDER = "-- write your SQL here\nSELECT * FROM users LIMIT 10;"

    DEFAULT_CSS = """
    QueryEditor {
        height: 40%;
        border-bottom: solid $primary;
    }

    QueryEditor TextArea {
        height: 1fr;
    }

    QueryEditor Horizontal {
        height: auto;
        padding: 0 1;
        align: right middle;
    }

    QueryEditor Button {
        margin-left: 1;
    }

    QueryEditor Label.editor-title {
        text-style: bold;
        padding: 1 1;
        color: $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Query Editor", classes="editor-title")
        yield TextArea(
            self.PLACEHOLDER,
            language="sql",
            id="sql-input",
        )
        with Horizontal():
            yield Button("Run  F5", variant="primary", id="run-query")
            yield Button("Clear", variant="default", id="clear-query")

    def on_mount(self) -> None:
        """Select all placeholder text on mount so user can just start typing."""
        editor = self.query_one("#sql-input", TextArea)
        editor.select_all()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles Run and Clear button clicks."""
        if event.button.id == "run-query":
            self._submit_query()
        elif event.button.id == "clear-query":
            self._clear_editor()

    def on_key(self, event) -> None:
        """
        Listens for F5 keypress to run the query.
        Keyboard shortcut so users don't have to reach for the mouse.
        """
        if event.key == "f5":
            self._submit_query()

    def _submit_query(self) -> None:
        """
        Reads the current text from the editor and posts
        a QuerySubmitted message. HomeScreen receives it
        and runs the actual query against the database.
        """
        editor = self.query_one("#sql-input", TextArea)
        query = editor.text.strip()

        if not query:
            self.notify("Please enter a query", severity="warning")
            return

        if query == self.PLACEHOLDER.strip():
            self.notify("Please enter a query", severity="warning")
            return

        self.post_message(self.QuerySubmitted(query))

    def _clear_editor(self) -> None:
        """Clears the text area."""
        editor = self.query_one("#sql-input", TextArea)
        editor.clear()