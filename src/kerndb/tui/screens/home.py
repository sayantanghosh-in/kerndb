from textual.app import ComposeResult
from textual.screen import Screen
from textual.reactive import reactive
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from kerndb.connectors.postgres import PostgresConnector
from kerndb.config.settings import get_connection, get_password


class HomeScreen(Screen):
    """
    The main screen of kerndb.
    Shown after a connection is established.
    Composes the sidebar, query editor, and results table together.
    """

    BINDINGS = [
        ("ctrl+b", "go_back", "Connections"),
        ("ctrl+n", "new_connection", "New Connection"),
    ]

    # reactive variables — like useState in React
    # when these change, Textual re-renders automatically
    active_table: reactive[str] = reactive("")
    query_results: reactive[list] = reactive([])
    connection_name: reactive[str] = reactive("")

    def __init__(self, connection_name: str, password: str = "") -> None:
        super().__init__()
        self.connection_name = connection_name
        self.connector = PostgresConnector()
        self._password = password   # password passed directly from picker

    def compose(self) -> ComposeResult:
        from kerndb.tui.widgets.sidebar import Sidebar
        from kerndb.tui.widgets.query_editor import QueryEditor
        from kerndb.tui.widgets.results_table import ResultsTable
        from kerndb.tui.widgets.status_bar import StatusBar

        yield Header()
        with Horizontal(id="main-layout"):
            yield Sidebar(id="sidebar")
            with Vertical(id="right-panel"):
                yield QueryEditor(id="query-editor")
                yield ResultsTable(id="results-table")
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """
        Runs once after the screen is rendered.
        Connects to the database and loads the table list.
        """
        from kerndb.tui.widgets.status_bar import StatusBar
        from kerndb.tui.widgets.query_editor import QueryEditor

        self.app.sub_title = (
            "Sayantan Ghosh  •  sayantanghosh.in"
            "  •  github.com/sayantanghosh-in"
        )

        config = get_connection(self.connection_name)
        if config is None:
            self.notify("Connection not found", severity="error")
            self.app.pop_screen()
            return

        # use directly passed password first
        # fall back to env variable if not provided
        password = self._password or get_password(self.connection_name) or ""
        config_with_password = {**config, "password": password}

        try:
            self.connector.connect(config_with_password)
            self.notify(
                f"Connected to {self.connection_name}",
                severity="information"
            )
            self.query_one("#status-bar", StatusBar).update_connection(
                self.connection_name, True
            )
            self._load_tables()
            # autofocus the query editor after connecting
            self.query_one("#query-editor", QueryEditor).focus()
        except ConnectionError as e:
            self.notify(str(e), severity="error")

    def _load_tables(self) -> None:
        """Fetches tables from the DB and sends them to the sidebar."""
        from kerndb.tui.widgets.sidebar import Sidebar
        tables = self.connector.get_tables()
        self.query_one("#sidebar", Sidebar).update_tables(tables)

    def on_sidebar_table_selected(self, message) -> None:
        """
        Fires when the user clicks a table in the sidebar.
        Loads the first 100 rows of that table automatically.
        """
        from kerndb.tui.widgets.status_bar import StatusBar

        self.active_table = message.table
        self.title = f"kerndb — {self.connection_name} — {message.table}"
        default_query = f"SELECT * FROM {message.table} LIMIT 100;"
        self._run_query(default_query)
        self.query_one("#status-bar", StatusBar).update_table(message.table)

    def on_query_editor_query_submitted(self, message) -> None:
        """
        Fires when the user runs a query from the query editor.
        """
        self._run_query(message.query)

    def _run_query(self, query: str) -> None:
        from kerndb.tui.widgets.results_table import ResultsTable
        from kerndb.tui.widgets.status_bar import StatusBar

        # split on semicolon to get individual statements
        # filter out empty strings from trailing semicolons or blank lines
        statements = [s.strip() for s in query.split(";") if s.strip()]

        if not statements:
            self.notify("No valid statements found", severity="warning")
            return

        last_results = []
        success_count = 0
        error_count = 0
        total_affected = 0

        for statement in statements:
            try:
                results = self.connector.execute(statement)
                last_results = results
                success_count += 1

                # if this statement returned rows it was a SELECT
                # if it returned empty list it was INSERT/UPDATE/DELETE
                if not results:
                    total_affected += 1

            except RuntimeError as e:
                error_count += 1
                self.notify(
                    f"Statement {success_count + error_count} failed: {e}",
                    severity="error"
                )
                # stop on first error — don't run remaining statements
                break

        # update the results table with whatever the last SELECT returned
        self.query_results = last_results
        self.query_one("#results-table", ResultsTable).update_results(last_results)
        self.query_one("#status-bar", StatusBar).update_row_count(len(last_results))

        # notify the user about what happened
        if len(statements) == 1:
            # single statement — no need for a summary
            if error_count == 0 and not last_results:
                self.notify(
                    "Statement executed successfully",
                    severity="information"
                )
        else:
            # multiple statements — show a summary
            if error_count == 0:
                self.notify(
                    f"All {success_count} statements executed successfully",
                    severity="information"
                )
            else:
                self.notify(
                    f"{success_count} succeeded, {error_count} failed",
                    severity="warning"
                )

    def on_unmount(self) -> None:
        """
        Runs when the screen is removed.
        Always disconnect cleanly when leaving the home screen.
        """
        self.connector.disconnect()

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_new_connection(self) -> None:
        self.app.push_screen("connection")