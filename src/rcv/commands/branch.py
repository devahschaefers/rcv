"""Branch command - Create a variant of an existing resume."""

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import Resume, ResumeMetadata, find_resume, VARIANTS_DIR
from rcv.utils.completion import complete_resume_name, complete_seed_file

console = Console()


def branch(
    source: str = typer.Argument(
        ...,
        help="Name of the resume to branch from",
        shell_complete=complete_resume_name,
    ),
    name: str = typer.Argument(..., help="Name for the new variant"),
    seed: Optional[str] = typer.Option(
        None,
        "--from",
        "-s",
        help="Seed the new variant from a .tex/.typ file path instead of the source resume.",
        shell_complete=complete_seed_file,
    ),
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

    # Determine seed file (source resume file by default, or --from file path)
    seed_file: Optional[Path] = None
    seed_format: Optional[str] = source_resume.metadata.format

    if seed is not None:
        seed_path = Path(seed)
        candidates = []
        if seed_path.is_absolute():
            candidates.append(seed_path)
        else:
            candidates.append(Path.cwd() / seed_path)
            candidates.append(resumes_dir / seed_path)

        for candidate in candidates:
            if candidate.is_file() and candidate.suffix in {".tex", ".typ"}:
                seed_file = candidate
                seed_format = "latex" if candidate.suffix == ".tex" else "typst"
                break

        if seed_file is None:
            console.print(
                f"[red]Seed source not found:[/red] {seed}\n"
                "Provide a .tex/.typ file path (absolute, cwd-relative, or project-root-relative)."
            )
            raise typer.Exit(1)

        if seed_format != source_resume.metadata.format:
            console.print(
                "[red]Format mismatch:[/red] Seed file format must match the base resume format."
            )
            raise typer.Exit(1)
    else:
        source_file = source_resume.resume_file
        if source_file.exists():
            seed_file = source_file

    # Copy the seed file into the new variant as resume.<ext>
    if seed_file is not None:
        dest_file = variant_path / f"resume{seed_file.suffix}"
        shutil.copy2(seed_file, dest_file)

    # Create new metadata for variant
    metadata = ResumeMetadata(format=source_resume.metadata.format)
    metadata.save(variant_path)

    console.print(f"[green]Created variant:[/green] {source}/{name}")
    console.print(f"[dim]Location: {variant_path}[/dim]")
    console.print(f"[dim]Branched from: {source}[/dim]")
