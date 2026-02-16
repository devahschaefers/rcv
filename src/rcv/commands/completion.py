"""Completion setup commands."""

import os
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

console = Console()


def setup_fish_completion(
    output: Path = typer.Option(
        Path("~/.config/fish/completions/rcv.fish"),
        "--output",
        "-o",
        help="Where to write the fish completion script.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing completion file.",
    ),
) -> None:
    """Install fish shell completion for rcv.

    This writes fish completion script to ~/.config/fish/completions/rcv.fish
    by default, then fish will load it automatically in new sessions.
    """
    output_path = output.expanduser()
    if output_path.exists() and not force:
        console.print(
            f"[yellow]Completion file already exists:[/yellow] {output_path}\n"
            "Use --force to overwrite."
        )
        raise typer.Exit(1)

    env = os.environ.copy()
    env["_RCV_COMPLETE"] = "source_fish"

    result = subprocess.run(
        [sys.argv[0]],
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        console.print("[red]Failed to generate fish completion script.[/red]")
        if result.stderr.strip():
            console.print(result.stderr.strip())
        raise typer.Exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result.stdout)

    console.print(f"[green]Installed fish completion:[/green] {output_path}")
    console.print("[dim]Start a new fish shell (or run: exec fish)[/dim]")

