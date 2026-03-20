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

    # reactive variables — like useState in React
    # when these change, Textual re-renders automatically
    active_table: reactive[str] = reactive("")
    query_results: reactive[list] = reactive([])
    connection_name: reactive[str] = reactive("")

    def __init__(self, connection_name: str) -> None:
        """
        HomeScreen receives the name of the saved connection to use.
        It looks up the connection details from config and connects.
        """
        super().__init__()
        self.connection_name = connection_name
        self.connector = PostgresConnector()

    def compose(self) -> ComposeResult:
        """
        Defines the layout of the home screen.
        We import widgets here to avoid circular imports at the top of the file.
        """
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
        config = get_connection(self.connection_name)
        if config is None:
            self.notify("Connection not found", severity="error")
            self.app.pop_screen()
            return

        password = get_password(self.connection_name)
        config_with_password = {**config, "password": password or ""}

        try:
            self.connector.connect(config_with_password)
            self.notify(
                f"Connected to {self.connection_name}",
                severity="information"
            )
            self._load_tables()
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
        self.active_table = message.table
        self.title = f"kerndb — {self.connection_name} — {message.table}"
        default_query = f"SELECT * FROM {message.table} LIMIT 100;"
        self._run_query(default_query)

    def on_query_editor_query_submitted(self, message) -> None:
        """
        Fires when the user runs a query from the query editor.
        """
        self._run_query(message.query)

    def _run_query(self, query: str) -> None:
        """
        Runs a SQL query and sends results to the results table.
        Central place for all query execution — both from sidebar
        clicks and manual query editor input go through here.
        """
        from kerndb.tui.widgets.results_table import ResultsTable

        try:
            results = self.connector.execute(query)
            self.query_results = results
            self.query_one("#results-table", ResultsTable).update_results(results)
        except RuntimeError as e:
            self.notify(str(e), severity="error")

    def on_unmount(self) -> None:
        """
        Runs when the screen is removed.
        Always disconnect cleanly when leaving the home screen.
        """
        self.connector.disconnect()