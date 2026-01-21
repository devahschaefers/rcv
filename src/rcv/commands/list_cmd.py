"""List command - List all resumes."""

import typer
from rich.console import Console
from rich.table import Table

from rcv.core.config import Config
from rcv.core.resume import get_all_resumes

console = Console()


def list_resumes(
    all: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Include archived resumes",
    ),
    tags: str = typer.Option(
        None,
        "--tags",
        "-t",
        help="Filter by tags (comma-separated)",
    ),
) -> None:
    """List all resumes.

    Shows a flat list of all resumes with their metadata.
    Use 'rcv tree' to see the branching hierarchy.
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    resumes = get_all_resumes(resumes_dir)

    if not resumes:
        console.print("[dim]No resumes found. Create one with 'rcv new <name>'[/dim]")
        return

    # Filter archived
    if not all:
        resumes = [r for r in resumes if not r.metadata.archived]

    # Filter by tags
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        resumes = [r for r in resumes if any(t in r.metadata.tags for t in tag_list)]

    if not resumes:
        console.print("[dim]No matching resumes found.[/dim]")
        return

    # Build table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Format")
    table.add_column("Tags")
    table.add_column("Updated")
    table.add_column("Status")

    for resume in resumes:
        status = "[dim]archived[/dim]" if resume.metadata.archived else ""
        tags_str = (
            ", ".join(resume.metadata.tags) if resume.metadata.tags else "[dim]-[/dim]"
        )
        updated = resume.metadata.updated_at.strftime("%Y-%m-%d")

        table.add_row(
            resume.full_name,
            resume.metadata.format,
            tags_str,
            updated,
            status,
        )

    console.print(table)
