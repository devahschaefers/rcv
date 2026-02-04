"""New command - Create a new base resume."""

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import Resume, find_resume

console = Console()


def new(
    name: str = typer.Argument(..., help="Name for the new resume"),
    format: str = typer.Option(
        None,
        "--format",
        "-f",
        help="Resume format: latex or typst. Defaults to config setting.",
    ),
    source: Optional[str] = typer.Option(
        None,
        "--from",
        "-s",
        help="Create a new base resume from an existing resume name.",
    ),
) -> None:
    """Create a new base resume.

    This creates a new resume at the root level (not a variant of another resume).
    You can optionally seed it from an existing resume.
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    source_resume = None
    template_content: Optional[str] = None
    template_format: Optional[str] = None
    move_source_file: Optional[Path] = None

    if source is not None:
        # Try to resolve as a managed resume first
        source_resume = find_resume(resumes_dir, source)

        # If not found, try file-path sources (tex/typ) relative to cwd and resumes_dir
        if source_resume is None:
            candidates = []
            source_path = Path(source)
            if source_path.is_absolute():
                candidates.append(source_path)
            else:
                candidates.append(Path.cwd() / source_path)
                candidates.append(resumes_dir / source_path)

            for candidate in candidates:
                if candidate.is_file() and candidate.suffix in {".tex", ".typ"}:
                    template_content = None
                    template_format = "latex" if candidate.suffix == ".tex" else "typst"
                    move_source_file = candidate
                    break

        if source_resume is None and template_content is None:
            console.print(
                f"[red]Source not found:[/red] {source}\n"
                "Provide a managed resume name (e.g., 'swe/google') or a path to a .tex/.typ file."
            )
            raise typer.Exit(1)

    if source_resume is not None:
        if source_resume.resume_file.exists():
            template_content = source_resume.resume_file.read_text()
        template_format = source_resume.metadata.format

    if template_format is not None and format is not None:
        if format != template_format:
            console.print(
                "[red]Format mismatch:[/red] --format must match the source resume or template."
            )
            raise typer.Exit(1)

    # Use default format if not specified
    if format is None:
        if template_format is not None:
            format = template_format
        else:
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
    resume = Resume.create(
        resume_path, format=format, template_content=template_content
    )

    # If sourcing from a file path, move it into place and rename to resume.<ext>
    if move_source_file is not None:
        dest_file = resume.resume_file
        if dest_file.exists():
            dest_file.unlink()
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(move_source_file), str(dest_file))

    console.print(f"[green]Created new resume:[/green] {name}")
    if source is not None:
        console.print(f"[dim]Seeded from: {source}[/dim]")
    console.print(f"[dim]Location: {resume.resume_file}[/dim]")
    console.print(f"[dim]Format: {format}[/dim]")
