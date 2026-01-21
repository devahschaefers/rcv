"""Init command - Initialize a resumes directory."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from rcv.core.config import Config

console = Console()


def init(
    path: Optional[Path] = typer.Argument(
        None,
        help="Path to initialize as resumes directory. Defaults to current directory.",
    ),
) -> None:
    """Initialize a directory as your resumes directory.

    This sets up the global configuration to point to your resumes.
    """
    if path is None:
        path = Path.cwd()

    path = path.resolve()

    # Create the directory if it doesn't exist
    path.mkdir(parents=True, exist_ok=True)

    # Update config
    config = Config.load()
    config.resumes_dir = path
    config.save()

    console.print(f"[green]Initialized resumes directory at:[/green] {path}")
    console.print(f"[dim]Config saved to ~/.config/rcv/config.yaml[/dim]")
