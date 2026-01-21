"""Branch command - Create a variant of an existing resume."""

import shutil
from pathlib import Path

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import Resume, ResumeMetadata, find_resume, VARIANTS_DIR

console = Console()


def branch(
    source: str = typer.Argument(..., help="Name of the resume to branch from"),
    name: str = typer.Argument(..., help="Name for the new variant"),
) -> None:
    """Create a new variant (branch) of an existing resume.

    The new resume will be created under the source resume's variants directory.

    Examples:
        rcv branch swe google        # Creates swe/variants/google
        rcv branch swe/google meta   # Creates swe/variants/google/variants/meta
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    # Find source resume
    source_resume = find_resume(resumes_dir, source)
    if source_resume is None:
        console.print(f"[red]Resume not found:[/red] {source}")
        raise typer.Exit(1)

    # Create variant path
    variant_path = source_resume.variants_dir / name

    if variant_path.exists():
        console.print(f"[red]Variant already exists:[/red] {source}/{name}")
        raise typer.Exit(1)

    # Create variants directory if needed
    source_resume.variants_dir.mkdir(exist_ok=True)

    # Copy source resume to variant
    variant_path.mkdir(parents=True)

    # Copy the resume file
    source_file = source_resume.resume_file
    if source_file.exists():
        dest_file = variant_path / source_file.name
        shutil.copy2(source_file, dest_file)

    # Create new metadata for variant
    metadata = ResumeMetadata(format=source_resume.metadata.format)
    metadata.save(variant_path)

    console.print(f"[green]Created variant:[/green] {source}/{name}")
    console.print(f"[dim]Location: {variant_path}[/dim]")
    console.print(f"[dim]Branched from: {source}[/dim]")
