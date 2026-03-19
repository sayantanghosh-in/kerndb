import json
import os
from pathlib import Path


# this is the path to ~/.kerndb/config.json
# Path.home() returns the user's home directory on any OS
CONFIG_DIR = Path.home() / ".kerndb"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _ensure_config_exists() -> None:
    """
    Creates the ~/.kerndb/ directory and an empty config.json
    if they don't already exist.
    The underscore prefix means this is a private helper function
    — internal use only, not meant to be called from outside this file.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        _write_config({"connections": {}, "defaults": {}})


def _read_config() -> dict:
    """
    Reads and returns the full config file as a dict.
    Private helper — use the public functions below instead.
    """
    _ensure_config_exists()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def _write_config(data: dict) -> None:
    """
    Writes a dict to the config file as formatted JSON.
    Private helper — use the public functions below instead.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_all_connections() -> dict:
    """
    Returns all saved connections as a dict.
    Example return value:
    {
        "mydb": {
            "type": "postgres",
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "database": "mydb"
        }
    }
    """
    config = _read_config()
    return config.get("connections", {})


def get_connection(name: str) -> dict | None:
    """
    Returns a single saved connection by name.
    Returns None if the connection doesn't exist.
    """
    connections = get_all_connections()
    return connections.get(name, None)


def save_connection(name: str, connection: dict) -> None:
    """
    Saves a named connection to the config file.
    If a connection with the same name exists, it overwrites it.
    """
    config = _read_config()
    config["connections"][name] = connection
    _write_config(config)


def delete_connection(name: str) -> None:
    """
    Deletes a saved connection by name.
    Does nothing if the connection doesn't exist.
    """
    config = _read_config()
    if name in config["connections"]:
        del config["connections"][name]
        _write_config(config)


def get_defaults() -> dict:
    """
    Returns the defaults section of the config.
    """
    config = _read_config()
    return config.get("defaults", {})

def get_password(name: str) -> str | None:
    """
    Retrieves the password for a connection.
    Never stored in config — reads from environment variable instead.
    Environment variable format: KERNDB_PASSWORD_<NAME> (uppercased)
    Example: connection named "mydb" -> KERNDB_PASSWORD_MYDB
    """
    env_key = f"KERNDB_PASSWORD_{name.upper()}"
    return os.environ.get(env_key, None)