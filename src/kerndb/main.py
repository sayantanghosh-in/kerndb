import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main():
    """kerndb — a beautiful terminal database client."""
    print("kerndb is working!")

if __name__ == "__main__":
    app()