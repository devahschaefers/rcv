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
        help="Create a new base resume from a .tex/.typ file path.",
    ),
) -> None:
    """Create a new base resume.

    This creates a new resume at the root level (not a variant of another resume).
    You can optionally seed it from an existing resume.
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    template_content: Optional[str] = None
    template_format: Optional[str] = None
    source_file_path: Optional[Path] = None

    if source is not None:
        # --from accepts only file paths (tex/typ)
        source_path = Path(source)
        candidates = []
        if source_path.is_absolute():
            candidates.append(source_path)
        else:
            candidates.append(Path.cwd() / source_path)
            candidates.append(resumes_dir / source_path)

        for candidate in candidates:
            if candidate.is_file() and candidate.suffix in {".tex", ".typ"}:
                source_file_path = candidate
                template_format = "latex" if candidate.suffix == ".tex" else "typst"
                break

        if source_file_path is None:
            console.print(
                f"[red]Source not found:[/red] {source}\n"
                "Provide a .tex/.typ file path (absolute, cwd-relative, or project-root-relative)."
            )
            raise typer.Exit(1)

    if template_format is not None and format is not None:
        if format != template_format:
            console.print(
                "[red]Format mismatch:[/red] --format must match the source file format."
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

    # If sourcing from a file path, copy its content; otherwise use template_content
    if source_file_path is not None:
        template_content = source_file_path.read_text()

    # Create the resume
    resume = Resume.create(
        resume_path, format=format, template_content=template_content
    )

    # If sourcing from a file path, ensure the file is placed as resume.<ext>
    if source_file_path is not None:
        dest_file = resume.resume_file
        if dest_file.exists():
            dest_file.unlink()
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file_path, dest_file)

    console.print(f"[green]Created new resume:[/green] {name}")
    if source is not None:
        console.print(f"[dim]Seeded from: {source}[/dim]")
    console.print(f"[dim]Location: {resume.resume_file}[/dim]")
    console.print(f"[dim]Format: {format}[/dim]")
