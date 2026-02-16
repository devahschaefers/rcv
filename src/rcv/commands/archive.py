"""Archive command - Archive/unarchive resumes."""

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import find_resume
from rcv.utils.completion import complete_resume_name

console = Console()


def archive(
    name: str = typer.Argument(
        ...,
        help="Name of the resume",
        shell_complete=complete_resume_name,
    ),
    unarchive: bool = typer.Option(
        False,
        "--unarchive",
        "-u",
        help="Unarchive instead of archiving",
    ),
) -> None:
    """Archive a resume to hide it from default listings.

    Archived resumes are hidden from 'rcv list' and 'rcv tree' by default.
    Use the --all flag with those commands to see archived resumes.

    Examples:
        rcv archive swe/old-version
        rcv archive swe/old-version --unarchive
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    resume = find_resume(resumes_dir, name)
    if resume is None:
        console.print(f"[red]Resume not found:[/red] {name}")
        raise typer.Exit(1)

    if unarchive:
        if not resume.metadata.archived:
            console.print(f"[yellow]Resume is not archived:[/yellow] {name}")
            return

        resume.metadata.archived = False
        resume.save()
        console.print(f"[green]Unarchived:[/green] {name}")
    else:
        if resume.metadata.archived:
            console.print(f"[yellow]Resume is already archived:[/yellow] {name}")
            return

        resume.metadata.archived = True
        resume.save()
        console.print(f"[green]Archived:[/green] {name}")
