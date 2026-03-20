from kerndb.cli.formatters import print_results, print_connections


def test_print_results_with_empty_list(capsys):
    """
    print_results with empty list should print a no results message.
    capsys is a pytest built-in that captures terminal output.
    """
    print_results([])
    captured = capsys.readouterr()
    assert "No results" in captured.out


def test_print_connections_with_empty_dict(capsys):
    """print_connections with empty dict should say no connections found."""
    print_connections({})
    captured = capsys.readouterr()
    assert "No saved connections" in captured.out


def test_print_results_with_data(capsys):
    """print_results with real data should print the rows."""
    results = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]
    print_results(results)
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "2 rows" in captured.out