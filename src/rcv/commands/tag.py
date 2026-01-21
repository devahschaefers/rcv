"""Tag commands - Add and remove tags from resumes."""

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import find_resume

console = Console()


def tag(
    name: str = typer.Argument(..., help="Name of the resume"),
    tag: str = typer.Argument(..., help="Tag to add"),
) -> None:
    """Add a tag to a resume.

    Tags help organize and filter resumes.

    Examples:
        rcv tag swe applied
        rcv tag swe/google faang
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    resume = find_resume(resumes_dir, name)
    if resume is None:
        console.print(f"[red]Resume not found:[/red] {name}")
        raise typer.Exit(1)

    if tag in resume.metadata.tags:
        console.print(f"[yellow]Tag already exists:[/yellow] {tag}")
        return

    resume.metadata.tags.append(tag)
    resume.save()

    console.print(f"[green]Added tag:[/green] {tag} to {name}")


def untag(
    name: str = typer.Argument(..., help="Name of the resume"),
    tag: str = typer.Argument(..., help="Tag to remove"),
) -> None:
    """Remove a tag from a resume.

    Examples:
        rcv untag swe applied
        rcv untag swe/google faang
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    resume = find_resume(resumes_dir, name)
    if resume is None:
        console.print(f"[red]Resume not found:[/red] {name}")
        raise typer.Exit(1)

    if tag not in resume.metadata.tags:
        console.print(f"[yellow]Tag not found:[/yellow] {tag}")
        return

    resume.metadata.tags.remove(tag)
    resume.save()

    console.print(f"[green]Removed tag:[/green] {tag} from {name}")
