from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Label
from textual.containers import Vertical


class ResultsTable(Widget):
    """
    The query results widget.
    Displays rows returned from a SQL query as a scrollable table.
    Updated by HomeScreen after every query execution.
    """

    DEFAULT_CSS = """
    ResultsTable {
        height: 1fr;
        padding: 0 1;
    }

    ResultsTable Label.results-title {
        text-style: bold;
        padding: 1 0;
        color: $accent;
    }

    ResultsTable Label.results-meta {
        color: $text-muted;
        padding: 0 0 1 0;
    }

    ResultsTable DataTable {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Results", classes="results-title")
            yield Label("", id="results-meta", classes="results-meta")
            yield DataTable(id="results-data")

    def on_mount(self) -> None:
        """Set up the DataTable with zebra stripes and a cursor on mount."""
        table = self.query_one("#results-data", DataTable)
        table.zebra_stripes = True
        table.cursor_type = "row"

    def update_results(self, results: list) -> None:
        """
        Called by HomeScreen after a query runs.
        Clears the table and repopulates it with new results.
        """
        table = self.query_one("#results-data", DataTable)
        meta = self.query_one("#results-meta", Label)

        # clear previous results
        table.clear(columns=True)

        # guard clause — nothing to render if results is empty
        if not results:
            meta.update("No results returned")
            return

        # get column names from the first row's keys
        # remember rows are dicts thanks to RealDictCursor
        columns = list(results[0].keys())

        # add columns to the table
        # "#" is a row number column we add ourselves
        table.add_columns("#", *columns)

        # add rows using enumerate to get the row number
        for index, row in enumerate(results, start=1):
            values = [str(index)] + [str(v) for v in row.values()]
            table.add_row(*values)

        # update the meta label with row count
        row_count = len(results)
        col_count = len(columns)
        meta.update(f"{row_count} rows · {col_count} columns")

    def show_error(self, message: str) -> None:
        """
        Displays an error message in the meta label.
        Called by HomeScreen when a query fails.
        """
        meta = self.query_one("#results-meta", Label)
        meta.update(f"Error: {message}")

        table = self.query_one("#results-data", DataTable)
        table.clear(columns=True)