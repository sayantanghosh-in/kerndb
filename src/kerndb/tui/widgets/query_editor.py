from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea, Button, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message


class QueryEditor(Widget):

    class QuerySubmitted(Message):
        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()

    DEFAULT_CSS = """
    QueryEditor {
        height: 40%;
        border-bottom: solid $primary;
    }

    QueryEditor #editor-header {
        height: 1;
        padding: 0 1;
        align: left middle;
    }

    QueryEditor #editor-title {
        text-style: bold;
        color: $accent;
        width: 1fr;
    }

    QueryEditor #editor-actions {
        width: auto;
        height: 1;
        align: right middle;
    }

    QueryEditor #run-query {
        background: $primary;
        color: $background;
        border: none;
        min-width: 10;
        height: 1;
        padding: 0 1;
    }

    QueryEditor #run-query:hover {
        background: $accent;
    }

    QueryEditor #clear-query {
        background: transparent;
        color: $text-muted;
        border: none;
        min-width: 8;
        height: 1;
        padding: 0 1;
    }

    QueryEditor #clear-query:hover {
        color: $accent;
    }

    QueryEditor #hint-label {
        color: $text-muted;
        padding: 0 1;
        height: 1;
    }

    QueryEditor TextArea {
        height: 1fr;
        border: none;
        padding: 0;
    }
    """

    def compose(self) -> ComposeResult:
        # header row — title on left, buttons on right
        with Horizontal(id="editor-header"):
            yield Label("Query Editor", id="editor-title")
            with Horizontal(id="editor-actions"):
                yield Button("▶ Run F5", id="run-query")
                yield Button("✕ Clear", id="clear-query")

        # hint label — always visible, never gets in the way
        yield Label(
            "-- write your SQL below and press F5 to run",
            id="hint-label"
        )

        # empty TextArea — no placeholder content to clear
        yield TextArea(
            "",
            language="sql",
            id="sql-input",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-query":
            self._submit_query()
        elif event.button.id == "clear-query":
            self.query_one("#sql-input", TextArea).clear()

    def on_key(self, event) -> None:
        if event.key == "f5":
            self._submit_query()

    def _submit_query(self) -> None:
        editor = self.query_one("#sql-input", TextArea)
        
        # if user has selected text, run only the selection
        # otherwise run the entire editor content
        selected = editor.selected_text.strip()
        full = editor.text.strip()
        
        query = selected if selected else full

        if not query:
            self.notify("Please write a query first", severity="warning")
            return

        self.post_message(self.QuerySubmitted(query))