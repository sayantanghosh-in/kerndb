import psycopg2
import psycopg2.extras

from kerndb.connectors.base import BaseConnector

class PostgresConnector(BaseConnector):
    """
    PostgreSQL implementation of BaseConnector.
    Uses psycopg2 to talk to a PostgreSQL database.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, config: dict) -> None:
        """
        Establish a connection to PostgreSQL.
        config expects: host, port, user, password, database
        """
        try:
            self.connection = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                dbname=config["database"],
            )
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Could not connect to PostgreSQL: {e}")

    def disconnect(self) -> None:
        """
        Close the cursor and connection cleanly.
        Always close cursor before connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None

    def test_connection(self) -> bool:
        """
        Returns True if the connection is alive, False otherwise.
        """
        try:
            if self.connection is None:
                return False
            self.cursor.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_tables(self) -> list:
        """
        Returns all table names in the public schema.
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [row["table_name"] for row in rows]

    def get_columns(self, table: str) -> list:
        """
        Returns column names and types for a given table.
        """
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        self.cursor.execute(query, (table,))
        rows = self.cursor.fetchall()
        return [{"name": row["column_name"], "type": row["data_type"]} for row in rows]

    def execute(self, query: str) -> list:
        """
        Run any SQL query and return results as a list of dicts.
        Returns empty list for queries that don't return rows (INSERT, UPDATE etc.)
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            try:
                rows = self.cursor.fetchall()
                return [dict(row) for row in rows]
            except psycopg2.ProgrammingError:
                return []
        except psycopg2.Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Query failed: {e}")