from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """
    Abstract base class for all kerndb database connectors.

    Every database connector (Postgres, MySQL, SQLite etc.)
    must inherit from this class and implement all methods below.
    This ensures the TUI and CLI can work with any connector
    without knowing which database is underneath.
    """

    @abstractmethod
    def connect(self, config: dict) -> None:
        """
        Establish a connection to the database.
        config is a dict with keys: host, port, user, password, database
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the database connection cleanly.
        """
        pass

    @abstractmethod
    def get_tables(self) -> list:
        """
        Return a list of all table names in the database.
        Example return value: ["users", "orders", "products"]
        """
        pass

    @abstractmethod
    def get_columns(self, table: str) -> list:
        """
        Return column info for a given table.
        Example return value:
        [
            {"name": "id", "type": "integer"},
            {"name": "email", "type": "varchar"},
        ]
        """
        pass

    @abstractmethod
    def execute(self, query: str) -> list:
        """
        Run a SQL query and return results as a list of dicts.
        Example return value:
        [
            {"id": 1, "email": "a@example.com"},
            {"id": 2, "email": "b@example.com"},
        ]
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if the connection is alive.
        Returns True if connected, False otherwise.
        """
        pass