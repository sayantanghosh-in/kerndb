from kerndb.connectors.postgres import PostgresConnector


def test_postgres_connector_can_be_instantiated():
    """PostgresConnector should be creatable with no arguments."""
    db = PostgresConnector()
    assert db is not None


def test_initial_connection_is_none():
    """Connection and cursor should both be None before connecting."""
    db = PostgresConnector()
    assert db.connection is None
    assert db.cursor is None


def test_test_connection_returns_false_when_not_connected():
    """test_connection should return False when no connection exists."""
    db = PostgresConnector()
    result = db.test_connection()
    assert result is False


def test_disconnect_when_not_connected_does_not_crash():
    """Calling disconnect before connecting should not raise any errors."""
    db = PostgresConnector()
    db.disconnect()