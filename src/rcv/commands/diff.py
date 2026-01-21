"""Diff command - Show differences between resumes."""

import difflib

import typer
from rich.console import Console
from rich.syntax import Syntax

from rcv.core.config import Config
from rcv.core.resume import find_resume

console = Console()


def diff(
    a: str = typer.Argument(..., help="First resume name"),
    b: str = typer.Argument(..., help="Second resume name"),
    context: int = typer.Option(
        3,
        "--context",
        "-c",
        help="Number of context lines around changes",
    ),
) -> None:
    """Show differences between two resumes.

    This performs a text diff between the resume files.

    Examples:
        rcv diff swe swe/google
        rcv diff swe/google swe/meta -c 5
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    # Find both resumes
    resume_a = find_resume(resumes_dir, a)
    if resume_a is None:
        console.print(f"[red]Resume not found:[/red] {a}")
        raise typer.Exit(1)

    resume_b = find_resume(resumes_dir, b)
    if resume_b is None:
        console.print(f"[red]Resume not found:[/red] {b}")
        raise typer.Exit(1)

    # Get resume files
    file_a = resume_a.resume_file
    file_b = resume_b.resume_file

    if not file_a.exists():
        console.print(f"[red]Resume file not found:[/red] {file_a}")
        raise typer.Exit(1)

    if not file_b.exists():
        console.print(f"[red]Resume file not found:[/red] {file_b}")
        raise typer.Exit(1)

    # Read contents
    content_a = file_a.read_text().splitlines(keepends=True)
    content_b = file_b.read_text().splitlines(keepends=True)

    # Generate diff
    diff_lines = list(
        difflib.unified_diff(
            content_a,
            content_b,
            fromfile=a,
            tofile=b,
            n=context,
        )
    )

    if not diff_lines:
        console.print(f"[green]No differences between {a} and {b}[/green]")
        return

    # Print diff with syntax highlighting
    diff_text = "".join(diff_lines)
    syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=False)
    console.print(syntax)
