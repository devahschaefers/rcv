"""Watch command - Auto-rebuild resume on file changes."""

import time
from pathlib import Path

import typer
from rich.console import Console
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from rcv.core.config import Config
from rcv.core.resume import find_resume
from rcv.commands.build import (
    build_latex,
    build_typst,
    ensure_output_settings,
    resolve_output_file,
)
from rcv.utils.completion import complete_resume_name

console = Console()


class ResumeWatcher(FileSystemEventHandler):
    """Handler for resume file changes."""

    def __init__(self, resume_file: Path, output_file: Path, format: str, compiler: str):
        self.resume_file = resume_file
        self.output_file = output_file
        self.format = format
        self.compiler = compiler
        self.last_build = 0
        self.debounce_seconds = 1.0

    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if it's our resume file
        if Path(event.src_path).name != self.resume_file.name:
            return

        # Debounce rapid changes
        now = time.time()
        if now - self.last_build < self.debounce_seconds:
            return
        self.last_build = now

        console.print(f"\n[dim]File changed, rebuilding...[/dim]")

        if self.format == "latex":
            success = build_latex(self.resume_file, self.output_file, self.compiler)
        else:
            success = build_typst(self.resume_file, self.output_file, self.compiler)

        if success:
            console.print(f"[green]Rebuilt successfully[/green]")
        else:
            console.print(f"[red]Build failed[/red]")


def watch(
    name: str = typer.Argument(
        ...,
        help="Name of the resume to watch",
        shell_complete=complete_resume_name,
    ),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for the PDF. Defaults to project output_dir layout from .rcv.toml.",
    ),
) -> None:
    """Watch a resume for changes and auto-rebuild.

    This starts a file watcher that automatically rebuilds the PDF
    whenever the resume file is modified.

    Press Ctrl+C to stop watching.

    Examples:
        rcv watch swe
        rcv watch swe/google -o ~/Documents/
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

    ensure_output_settings(config)
    output_file = resolve_output_file(resume.full_name, resume_file, config, output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Determine compiler
    if resume.metadata.format == "latex":
        compiler = config.latex_compiler
    else:
        compiler = config.typst_compiler

    # Do initial build
    console.print(f"[bold]Watching:[/bold] {resume_file}")
    console.print(f"[dim]Press Ctrl+C to stop[/dim]\n")
    console.print(f"[dim]Output PDF:[/dim] {output_file}\n")

    console.print("[dim]Initial build...[/dim]")
    if resume.metadata.format == "latex":
        success = build_latex(resume_file, output_file, compiler)
    else:
        success = build_typst(resume_file, output_file, compiler)

    if success:
        console.print("[green]Initial build successful[/green]")
    else:
        console.print("[yellow]Initial build failed, watching for changes...[/yellow]")

    # Set up watcher
    event_handler = ResumeWatcher(
        resume_file=resume_file,
        output_file=output_file,
        format=resume.metadata.format,
        compiler=compiler,
    )

    observer = Observer()
    observer.schedule(event_handler, str(resume.path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n[dim]Stopped watching.[/dim]")

    observer.join()
