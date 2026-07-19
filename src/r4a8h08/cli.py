"""Console script for r4a8h08."""

import typer
from rich.console import Console

from r4a8h08 import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for r4a8h08."""
    console.print("Replace this message by putting your code into r4a8h08.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
