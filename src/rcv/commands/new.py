"""New command - Create a new base resume."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import Resume

console = Console()


def new(
    name: str = typer.Argument(..., help="Name for the new resume"),
    format: str = typer.Option(
        None,
        "--format",
        "-f",
        help="Resume format: latex or typst. Defaults to config setting.",
    ),
) -> None:
    """Create a new base resume.

    This creates a new resume at the root level (not a variant of another resume).
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    # Use default format if not specified
    if format is None:
        format = config.default_format

    if format not in ("latex", "typst"):
        console.print(
            f"[red]Invalid format:[/red] {format}. Must be 'latex' or 'typst'."
        )
        raise typer.Exit(1)

    # Check if resume already exists
    resume_path = resumes_dir / name
    if resume_path.exists():
        console.print(f"[red]Resume already exists:[/red] {name}")
        raise typer.Exit(1)

    # Create the resume
    resume = Resume.create(resume_path, format=format)

    console.print(f"[green]Created new resume:[/green] {name}")
    console.print(f"[dim]Location: {resume.resume_file}[/dim]")
    console.print(f"[dim]Format: {format}[/dim]")
