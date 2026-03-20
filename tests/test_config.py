import os

from kerndb.config.settings import (
    save_connection,
    get_connection,
    get_all_connections,
    delete_connection,
)


def test_save_and_get_connection():
    """Saving a connection and reading it back should return the same data."""
    save_connection("testdb", {
        "type": "postgres",
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "database": "testdb"
    })
    conn = get_connection("testdb")
    assert conn is not None
    assert conn["host"] == "localhost"
    assert conn["port"] == 5432
    assert conn["database"] == "testdb"


def test_get_connection_returns_none_for_missing():
    """Getting a connection that doesn't exist should return None."""
    conn = get_connection("this_does_not_exist")
    assert conn is None


def test_get_all_connections_returns_dict():
    """get_all_connections should always return a dict."""
    result = get_all_connections()
    assert isinstance(result, dict)


def test_delete_connection():
    """Deleting a connection should remove it from the config."""
    save_connection("to_delete", {
        "type": "postgres",
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "database": "to_delete"
    })
    delete_connection("to_delete")
    conn = get_connection("to_delete")
    assert conn is None


def test_delete_nonexistent_connection_does_not_crash():
    """Deleting a connection that doesn't exist should not raise any errors."""
    delete_connection("this_never_existed")

def test_get_password_from_env():
    """Password should be read from environment variable."""
    from kerndb.config.settings import get_password
    os.environ["KERNDB_PASSWORD_TESTDB"] = "supersecret"
    assert get_password("testdb") == "supersecret"
    del os.environ["KERNDB_PASSWORD_TESTDB"]


def test_get_password_returns_none_when_not_set():
    """get_password returns None if no env variable is set."""
    from kerndb.config.settings import get_password
    result = get_password("connection_that_has_no_password_set")
    assert result is None

def test_get_password_from_env():
    """Password should be read from environment variable."""
    from kerndb.config.settings import get_password
    os.environ["KERNDB_PASSWORD_TESTDB"] = "supersecret"
    assert get_password("testdb") == "supersecret"
    del os.environ["KERNDB_PASSWORD_TESTDB"]


def test_get_password_with_spaces_in_name():
    """Connection names with spaces should map to underscores in env key."""
    from kerndb.config.settings import get_password
    os.environ["KERNDB_PASSWORD_DUMMY_1"] = "supersecret"
    assert get_password("Dummy 1") == "supersecret"
    del os.environ["KERNDB_PASSWORD_DUMMY_1"]