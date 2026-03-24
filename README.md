# kerndb

> A minimal, UI-first terminal database client. Connect, explore,
> and query your PostgreSQL database without leaving the terminal.

![Python](https://img.shields.io/badge/python-3.9+-blue)
![PyPI](https://img.shields.io/pypi/v/kerndb)
![License](https://img.shields.io/badge/license-MIT-green)

![kerndb homescreen](/main/docs/home.png)

---

## Installation

### Recommended — pipx (no venv needed)

```bash
pipx install kerndb
```

### Alternative — pip

```bash
pip install kerndb
```

### Verify

```bash
kerndb --version
```

> **Why pipx?** pipx installs CLI tools in isolated environments
> automatically. You get the `kerndb` command globally without
> managing a virtual environment yourself. Install pipx with
> `pip install pipx` or `brew install pipx`.

---

## Quick Start

```bash
kerndb
```

That's it. The UI opens. Add a connection and start querying.

---

## What is kerndb?

**kerndb** is a terminal-based database client with a full
interactive UI that runs inside your terminal. Built for developers
who want the speed of the terminal without sacrificing the visual
clarity of a GUI tool like TablePlus or DBeaver.

> _The terminal is not a limitation. It is a canvas._

---

## Using the TUI

### Adding a connection

Launch kerndb and press `N` to add a new connection. Fill in
your PostgreSQL details and press Save. Passwords are never stored
on disk — kerndb reads them from environment variables:

```bash
# set password for a connection named "mydb"
# Windows
$env:KERNDB_PASSWORD_MYDB="yourpassword"

# Mac/Linux
export KERNDB_PASSWORD_MYDB=yourpassword
```

Or use a `.env` file in your project directory:

```bash
KERNDB_PASSWORD_MYDB=yourpassword
```

### Running queries

- Click any table in the sidebar to preview its data
- Write SQL in the query editor and press `F5` to run
- Select part of your SQL and press `F5` to run just the selection
- Write multiple statements separated by `;` and press `F5` to run all

### Keyboard shortcuts

| Key      | Action                                     |
| -------- | ------------------------------------------ |
| `F5`     | Run query (or selected text)               |
| `N`      | New connection (from picker screen)        |
| `D`      | Delete connection (press twice to confirm) |
| `Ctrl+B` | Go back to connection picker               |
| `Q`      | Quit                                       |
| `Ctrl+C` | Force quit                                 |

---

## CLI Commands

For scripting and automation — bypasses the TUI entirely.

```bash
# list saved connections
kerndb cli connections

# run a query
kerndb cli query "SELECT * FROM users LIMIT 10" --connection mydb

# export to CSV
kerndb cli query "SELECT * FROM orders" --export orders.csv --connection mydb

# save a connection
kerndb cli save mydb --user postgres --database mydb

# remove a connection
kerndb cli remove mydb

# update kerndb
kerndb cli update
```

---

## Supported Databases

| Database       | Status     |
| -------------- | ---------- |
| PostgreSQL 12+ | ✅ v1.0    |
| MySQL 8+       | 🔜 v2.0    |
| SQLite 3+      | 🔜 v2.0    |
| MariaDB        | 🔜 planned |
| Supabase       | 🔜 planned |
| MongoDB        | 🔜 planned |

---

## Configuration

Connections are stored at `~/.kerndb/config.json`.
Passwords are never stored — use environment variables or a `.env` file.

```json
{
  "connections": {
    "mydb": {
      "type": "postgres",
      "host": "localhost",
      "port": 5432,
      "user": "postgres",
      "database": "mydb"
    }
  }
}
```

---

## Known Limitations

- Template strings in INSERT/UPDATE queries
  (e.g. `INSERT INTO users VALUES ('{{name}}')`) are not
  supported in v1.0. Planned for a future release.

---

## Development

```bash
git clone https://github.com/sayantanghosh-in/kerndb.git
cd kerndb
python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
kerndb
```

Run tests:

```bash
python -m pytest tests/ -v
```

---

## Contributing

Issues and PRs are welcome at
[github.com/sayantanghosh-in/kerndb](https://github.com/sayantanghosh-in/kerndb).

Please make sure your code passes `flake8 src/` and `black src/`
before submitting a PR.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

_Built by [Sayantan Ghosh](https://sayantanghosh.in)_
