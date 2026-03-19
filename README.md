# kerndb

> A beautiful, UI-first terminal database client. Connect, explore, and query your database without leaving the terminal.

---

![Python](https://img.shields.io/badge/python-3.9+-blue)
![PyPI](https://img.shields.io/pypi/v/kerndb)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

- [What is kerndb?](#what-is-kerndb)
- [Philosophy](#philosophy)
- [What it looks like](#what-it-looks-like)
- [Features](#features)
- [Supported Databases](#supported-databases)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Using the TUI](#using-the-tui)
- [CLI Commands (Power Users)](#cli-commands-power-users)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## What is kerndb?

**kerndb** is a terminal-based database client with a full interactive UI that runs entirely inside your terminal. It is built for developers who want the speed of the terminal without sacrificing the visual clarity of a GUI tool like TablePlus or DBeaver.

Launch it with one command and you get a full app — sidebar with your tables, a query editor, a results panel, and a connection manager — all inside your terminal.

```bash
kerndb
```

That's it. The UI opens and you're home.

---

## Philosophy

Most database clients fall into one of two camps:

- **GUI tools** — beautiful and visual, but heavy, mouse-driven, and you have to leave your terminal
- **Raw CLI tools** — fast and terminal-native, but intimidating, no visual structure, steep learning curve

**kerndb lives in neither camp.** It is built on a simple belief:

> _The terminal is not a limitation. It is a canvas._

kerndb is **UI-first**. When you launch it, you get a full interactive application with panels, navigation, and a query editor — all rendered beautifully inside your terminal using the `textual` framework.

The raw CLI commands (`kerndb connect`, `kerndb query`) exist as a **fallback** for terminal power users, automation scripts, and CI pipelines. But they are not the primary experience.

**If you have never used a terminal database client before, kerndb is built for you.**

---

## What it looks like

```
╔═════════════════════════════════════════════════════════════════╗
║  kerndb  │  mydb (PostgreSQL)  │  connected ●                   ║
╠═══════════════╦═════════════════════════════════════════════════╣
║  TABLES       ║  QUERY EDITOR                                   ║
║  ─────────    ║  ┌──────────────────────────────────────────┐   ║
║  users        ║  │ SELECT * FROM users                      │   ║
║  orders       ║  │ WHERE active = true                      │   ║
║  products     ║  │ LIMIT 10;                                │   ║
║  sessions     ║  └──────────────────────────────────────────┘   ║
║  invoices     ║  [ Run Query F5 ]  [ Clear ]  [ Export ]        ║
║               ╠═════════════════════════════════════════════════╣
║  SCHEMAS      ║  RESULTS                  10 rows  │  4.2ms     ║
║  ─────────    ║  ┌──────┬───────────────┬──────────┬──────────┐ ║
║  public       ║  │ id   │ name          │ email    │ active   │ ║
║  auth         ║  ├──────┼───────────────┼──────────┼──────────┤ ║
║               ║  │ 1    │ Arjun Sharma  │ a@...    │ true     │ ║
║               ║  │ 2    │ Priya Nair    │ p@...    │ true     │ ║
║               ║  │ 3    │ Rohan Mehta   │ r@...    │ false    │ ║
╚═══════════════╩═════════════════════════════════════════════════╝
```

---

## Features

### TUI — Primary Experience

- Full interactive UI inside your terminal
- Sidebar showing all tables and schemas
- SQL query editor with syntax highlighting
- Results panel with scrollable, paginated table output
- Connection manager — save and switch between multiple databases
- Table inspector — select any table to see its columns, types, and constraints
- Query history — browse and re-run previous queries
- Export results to CSV from inside the UI

### CLI — Power User Fallback

- Connect to a database from the command line
- Run a query and get output directly in the terminal
- Pipe results into other commands
- Scriptable and CI-friendly

---

## Supported Databases

| Database   | Version | Status          |
| ---------- | ------- | --------------- |
| PostgreSQL | 12+     | ✅ v1.0         |
| MySQL      | 8+      | 🔜 v2.0 planned |
| SQLite     | 3+      | 🔜 v2.0 planned |
| MariaDB    | 10+     | 🔜 planned      |
| Supabase   | —       | 🔜 planned      |
| MongoDB    | 6+      | 🔜 planned      |

> **v1.0 ships with PostgreSQL only.** The architecture is built from the ground up
> to make adding new connectors straightforward — each database is a self-contained
> plugin that implements a shared interface. Adding MySQL in v2.0 will not require
> touching any existing code.

---

## Installation

### Requirements

- Python 3.9 or higher
- pip

### Install from PyPI

```bash
pip install kerndb
```

### Verify installation

```bash
kerndb --version
```

---

## Quick Start

### Launch the TUI (recommended)

```bash
kerndb
```

Opens the full interactive UI. From here you can add a connection,
browse your tables, and run queries — no further commands needed.

### Launch and connect directly

```bash
kerndb --connect postgres://user:password@localhost:5432/mydb
```

Opens the TUI already connected to your database.

---

## Using the TUI

### Step 1 — Add a connection

When you first launch kerndb you will see the connection manager.
Fill in your PostgreSQL details and give the connection a name:

```
Name:      mydb
Host:      localhost
Port:      5432
User:      postgres
Password:  ••••••••
Database:  mydb
```

Press `Enter` to connect. kerndb saves this for next time.

### Step 2 — Browse your tables

The left sidebar lists all tables and schemas. Use arrow keys or
your mouse to navigate. Press `Enter` on any table to preview its
data and inspect its columns in the results panel.

### Step 3 — Write a query

The query editor is in the top-right panel. Click it or press `Q`
to focus it. Write your SQL and press `F5` to run.

### Step 4 — Read your results

Results appear in the bottom-right panel. Scroll through rows and
columns with arrow keys. Press `E` to export to CSV.

### Step 5 — Switch connections

Press `C` to open the connection manager and switch databases.

---

## CLI Commands (Power Users)

These commands bypass the TUI entirely. Useful for scripting,
automation, and piping output into other tools.

### Open the TUI

```bash
kerndb
```

### Open TUI connected to a specific database

```bash
kerndb --connect postgres://user:password@localhost:5432/mydb
```

### Run a query (no TUI, plain output)

```bash
kerndb query "SELECT * FROM users LIMIT 10" --connection mydb
```

### List saved connections

```bash
kerndb connections
```

### Save a named connection

```bash
kerndb save mydb postgres://user:password@localhost:5432/mydb
```

### Export a query to CSV

```bash
kerndb query "SELECT * FROM orders" --export orders.csv --connection mydb
```

---

## Keyboard Shortcuts

| Key      | Action                      |
| -------- | --------------------------- |
| `F5`     | Run query                   |
| `Tab`    | Move focus between panels   |
| `C`      | Open connection manager     |
| `T`      | Focus table sidebar         |
| `Q`      | Focus query editor          |
| `R`      | Focus results panel         |
| `E`      | Export results to CSV       |
| `H`      | Open query history          |
| `?`      | Show keyboard shortcut help |
| `Ctrl+C` | Quit                        |

---

## Configuration

kerndb stores configuration at `~/.kerndb/config.json`:

```json
{
  "connections": {
    "mydb": {
      "type": "postgres",
      "host": "localhost",
      "port": 5432,
      "user": "postgres",
      "database": "mydb"
    },
    "staging": {
      "type": "postgres",
      "host": "staging.example.com",
      "port": 5432,
      "user": "postgres",
      "database": "mydb"
    }
  },
  "defaults": {
    "page_size": 50,
    "export_format": "csv",
    "theme": "dark"
  }
}
```

> Passwords are never stored in the config file. kerndb prompts for
> a password on connect, or reads from the environment:

```bash
export KERNDB_PASSWORD=yourpassword
kerndb --connect postgres://user@localhost:5432/mydb
```

---

## Project Structure

```
kerndb/
├── src/
│   └── kerndb/
│       ├── __init__.py
│       ├── main.py                   ← entry point, launches TUI or routes to CLI
│       │
│       ├── tui/                      ← everything related to the terminal UI
│       │   ├── __init__.py
│       │   ├── app.py                ← main Textual App class, boots the UI
│       │   ├── screens/              ← full-screen views
│       │   │   ├── __init__.py
│       │   │   ├── home.py           ← main screen (sidebar + editor + results)
│       │   │   └── connection.py     ← connection manager screen
│       │   ├── widgets/              ← reusable UI components
│       │   │   ├── __init__.py
│       │   │   ├── sidebar.py        ← tables and schemas list
│       │   │   ├── query_editor.py   ← SQL input panel
│       │   │   ├── results_table.py  ← query results panel
│       │   │   └── status_bar.py     ← bottom connection status bar
│       │   └── styles/
│       │       └── app.tcss          ← Textual CSS stylesheet
│       │
│       ├── connectors/               ← one file per database type
│       │   ├── __init__.py
│       │   ├── base.py               ← abstract base class (the shared interface)
│       │   └── postgres.py           ← PostgreSQL connector (v1)
│       │
│       ├── cli/                      ← raw terminal commands (power user fallback)
│       │   ├── __init__.py
│       │   ├── commands.py           ← typer CLI command definitions
│       │   └── formatters.py         ← formats output for plain terminal (no TUI)
│       │
│       └── config/                   ← config file management
│           ├── __init__.py
│           └── settings.py           ← read/write ~/.kerndb/config.json
│
├── tests/
│   └── __init__.py
│   └── test_config.py
│   └── test_postgres_connector.py
│
├── pyproject.toml                    ← package metadata for PyPI
├── requirements.txt                  ← pinned deps for local dev
├── .env.example                      ← template for environment variables
├── .gitignore
├── LICENSE
└── README.md
```

---

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/kerndb.git
cd kerndb
```

### 2. Create and activate a virtual environment

```bash
virtualenv venv
source venv/bin/activate        # mac/linux
venv\Scripts\activate           # windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install kerndb in editable mode

```bash
pip install -e .
```

The `-e` flag means editable — changes you make to the source are
immediately reflected when you run `kerndb`. No reinstall needed.

### 5. Run kerndb

```bash
kerndb
```

### 6. Run tests

```bash
pytest tests/
```

### Adding a new dependency

```bash
pip install some-package
pip freeze > requirements.txt
git add requirements.txt
```

---

## Roadmap

### v1.0 — PostgreSQL + Full TUI

- [x] Project scaffolding
- [ ] Base connector interface
- [ ] PostgreSQL connector
- [ ] TUI home screen (sidebar + query editor + results)
- [ ] Connection manager screen
- [ ] Save and load named connections
- [ ] Table inspector
- [ ] Query history
- [ ] Export to CSV
- [ ] PyPI publish

### v2.0 — More Connectors

- [ ] MySQL connector
- [ ] SQLite connector
- [ ] MariaDB connector

### v3.0 — Power Features

- [ ] Supabase connector
- [ ] MongoDB connector
- [ ] Natural language to SQL (`kerndb ask "show me recent orders"`)
- [ ] Homebrew tap
- [ ] Standalone binaries (no Python required)

---

## Contributing

This is a hobby project. Contributions, bug reports, and feature
requests are all welcome. Open an issue or a pull request.

Please make sure your code:

- Has no linting errors (`flake8 src/`)
- Is formatted with black (`black src/`)
- Includes a test for any new functionality

---

## License

MIT License. See [LICENSE](LICENSE) for details.
