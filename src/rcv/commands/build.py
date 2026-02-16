"""Build command - Compile resume to PDF."""

import subprocess
import shutil
from pathlib import Path

import typer
from rich.console import Console

from rcv.core.config import Config
from rcv.core.resume import find_resume

console = Console()


def cleanup_latex_artifacts(output_dir: Path, stem: str) -> None:
    """Remove common LaTeX intermediate files for a build target."""
    for ext in (".aux", ".log", ".out"):
        artifact = output_dir / f"{stem}{ext}"
        try:
            artifact.unlink(missing_ok=True)
        except OSError:
            # Best-effort cleanup; don't fail the build result on cleanup issues.
            pass


def resolve_output_file(
    resume_full_name: str,
    resume_file: Path,
    config: Config,
    output_dir_override: Path | None,
) -> Path:
    """Compute the output PDF file path."""
    if output_dir_override is not None:
        output_dir = output_dir_override.expanduser()
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / output_dir
        return output_dir / f"{resume_file.stem}.pdf"

    logical_resume_path = Path(*resume_full_name.split("/"))
    return (
        config.get_output_root_dir()
        / logical_resume_path
        / config.get_output_pdf_filename()
    )


def build(
    name: str = typer.Argument(..., help="Name of the resume to build"),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for the PDF. Defaults to project output_dir layout from .rcv.toml.",
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

    output_file = resolve_output_file(resume.full_name, resume_file, config, output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Build based on format
    if resume.metadata.format == "latex":
        success = build_latex(resume_file, output_file, config.latex_compiler)
    else:
        success = build_typst(resume_file, output_file, config.typst_compiler)

    if success:
        console.print(f"[green]Built successfully:[/green] {output_file}")
    else:
        console.print("[red]Build failed. See errors above.[/red]")
        raise typer.Exit(1)


def build_latex(source: Path, output_file: Path, compiler: str) -> bool:
    """Build a LaTeX resume."""
    # Check if compiler exists
    if not shutil.which(compiler):
        console.print(f"[red]LaTeX compiler not found:[/red] {compiler}")
        console.print(
            "[dim]Install LaTeX or configure a different compiler in .rcv.toml[/dim]"
        )
        return False

    output_dir = output_file.parent
    generated_pdf = output_dir / f"{source.stem}.pdf"

    cleanup_dirs = [output_dir]
    if source.parent != output_dir:
        cleanup_dirs.append(source.parent)

    try:
        # Run pdflatex (need to run twice for references)
        # Compile from the source directory with just the filename.
        # This avoids TeX parsing issues with absolute paths containing '~'
        # (common in iCloud paths like com~apple~CloudDocs).
        result = None
        for _ in range(2):
            result = subprocess.run(
                [
                    compiler,
                    "-interaction=nonstopmode",
                    f"-output-directory={output_dir}",
                    source.name,
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

        if generated_pdf != output_file:
            output_file.unlink(missing_ok=True)
            shutil.move(str(generated_pdf), str(output_file))

        return True

    except Exception as e:
        console.print(f"[red]Error running {compiler}:[/red] {e}")
        return False
    finally:
        for cleanup_dir in cleanup_dirs:
            cleanup_latex_artifacts(cleanup_dir, source.stem)


def build_typst(source: Path, output_file: Path, compiler: str) -> bool:
    """Build a Typst resume."""
    # Check if compiler exists
    if not shutil.which(compiler):
        console.print(f"[red]Typst compiler not found:[/red] {compiler}")
        console.print("[dim]Install Typst: https://typst.app/[/dim]")
        return False

    try:
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
