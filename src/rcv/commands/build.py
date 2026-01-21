"""Build command - Compile resume to PDF."""

import subprocess
import shutil
from pathlib import Path

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import find_resume

console = Console()


def build(
    name: str = typer.Argument(..., help="Name of the resume to build"),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for the PDF. Defaults to resume directory.",
    ),
) -> None:
    """Compile a resume to PDF.

    Supports both LaTeX and Typst formats.

    Examples:
        rcv build swe
        rcv build swe/google -o ~/Documents/
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    # Find the resume
    resume = find_resume(resumes_dir, name)
    if resume is None:
        console.print(f"[red]Resume not found:[/red] {name}")
        raise typer.Exit(1)

    resume_file = resume.resume_file
    if not resume_file.exists():
        console.print(f"[red]Resume file not found:[/red] {resume_file}")
        raise typer.Exit(1)

    # Determine output directory
    output_dir = output if output else resume.path
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build based on format
    if resume.metadata.format == "latex":
        success = build_latex(resume_file, output_dir, config.latex_compiler)
    else:
        success = build_typst(resume_file, output_dir, config.typst_compiler)

    if success:
        pdf_name = resume_file.stem + ".pdf"
        console.print(f"[green]Built successfully:[/green] {output_dir / pdf_name}")
    else:
        console.print("[red]Build failed. See errors above.[/red]")
        raise typer.Exit(1)


def build_latex(source: Path, output_dir: Path, compiler: str) -> bool:
    """Build a LaTeX resume."""
    # Check if compiler exists
    if not shutil.which(compiler):
        console.print(f"[red]LaTeX compiler not found:[/red] {compiler}")
        console.print(
            "[dim]Install LaTeX or configure a different compiler in ~/.config/rcv/config.yaml[/dim]"
        )
        return False

    try:
        # Run pdflatex (need to run twice for references)
        result = None
        for _ in range(2):
            result = subprocess.run(
                [
                    compiler,
                    "-interaction=nonstopmode",
                    f"-output-directory={output_dir}",
                    str(source),
                ],
                cwd=source.parent,
                capture_output=True,
                text=True,
            )

        if result is None or result.returncode != 0:
            console.print("[red]LaTeX compilation errors:[/red]")
            # Extract relevant error lines
            if result is not None:
                for line in result.stdout.split("\n"):
                    if line.startswith("!") or "Error" in line:
                        console.print(f"  {line}")
            return False

        return True

    except Exception as e:
        console.print(f"[red]Error running {compiler}:[/red] {e}")
        return False


def build_typst(source: Path, output_dir: Path, compiler: str) -> bool:
    """Build a Typst resume."""
    # Check if compiler exists
    if not shutil.which(compiler):
        console.print(f"[red]Typst compiler not found:[/red] {compiler}")
        console.print("[dim]Install Typst: https://typst.app/[/dim]")
        return False

    try:
        output_file = output_dir / (source.stem + ".pdf")

        result = subprocess.run(
            [compiler, "compile", str(source), str(output_file)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            console.print("[red]Typst compilation errors:[/red]")
            console.print(result.stderr)
            return False

        return True

    except Exception as e:
        console.print(f"[red]Error running typst:[/red] {e}")
        return False
