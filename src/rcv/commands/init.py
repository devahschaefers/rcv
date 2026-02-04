"""Init command - Initialize a resumes directory."""

from pathlib import Path
import shutil
from typing import Optional

import typer
from rich.console import Console

from rcv.core.config import Config

console = Console()


def init(
    path: Optional[Path] = typer.Argument(
        None,
        help="Path to initialize as resumes directory. Defaults to current directory.",
    ),
) -> None:
    """Initialize a directory as your resumes directory.

    This sets up the global configuration to point to your resumes.
    """
    if path is None:
        path = Path.cwd()

    path = path.resolve()

    # Create the directory if it doesn't exist
    path.mkdir(parents=True, exist_ok=True)

    assets_dir = path / "assets"
    assets_latex_dir = assets_dir / "latex"
    assets_typst_dir = assets_dir / "typst"
    assets_latex_dir.mkdir(parents=True, exist_ok=True)
    assets_typst_dir.mkdir(parents=True, exist_ok=True)

    package_assets_dir = Path(__file__).resolve().parents[1] / "assets"
    assets_to_copy = {
        package_assets_dir / "latex" / "preamble.tex": assets_latex_dir
        / "preamble.tex",
        package_assets_dir / "typst" / "resume_config.typ": assets_typst_dir
        / "resume_config.typ",
    }

    for source_path, dest_path in assets_to_copy.items():
        if source_path.exists() and not dest_path.exists():
            shutil.copy2(source_path, dest_path)

    # Update config
    config = Config.load()
    config.resumes_dir = path
    config.save()

    console.print(f"[green]Initialized resumes directory at:[/green] {path}")
    console.print(f"[dim]Config saved to ~/.config/rcv/config.yaml[/dim]")
