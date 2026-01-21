"""Tree command - Show resume hierarchy as a tree."""

import typer
from rich.console import Console
from rich.tree import Tree as RichTree

from rcv.core.config import Config
from rcv.core.resume import Resume, get_root_resumes

console = Console()


def build_tree(tree: RichTree, resume: Resume, show_archived: bool) -> None:
    """Recursively build tree from resume and its variants."""
    for variant in resume.get_variants():
        if not show_archived and variant.metadata.archived:
            continue

        # Build label
        label = variant.name
        if variant.metadata.tags:
            label += f" [dim][{', '.join(variant.metadata.tags)}][/dim]"
        if variant.metadata.archived:
            label += " [dim](archived)[/dim]"

        branch = tree.add(label)
        build_tree(branch, variant, show_archived)


def tree(
    all: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Include archived resumes",
    ),
) -> None:
    """Display resumes as a tree showing the branching hierarchy.

    This visualizes how resumes are related through branching.
    """
    config = Config.load()
    resumes_dir = config.get_resumes_dir()

    root_resumes = get_root_resumes(resumes_dir)

    if not root_resumes:
        console.print("[dim]No resumes found. Create one with 'rcv new <name>'[/dim]")
        return

    # Filter archived at root level
    if not all:
        root_resumes = [r for r in root_resumes if not r.metadata.archived]

    if not root_resumes:
        console.print("[dim]No active resumes found.[/dim]")
        return

    # Build the tree
    tree_root = RichTree("[bold]Resumes[/bold]")

    for resume in root_resumes:
        # Build label
        label = f"[bold]{resume.name}[/bold]"
        if resume.metadata.tags:
            label += f" [dim][{', '.join(resume.metadata.tags)}][/dim]"
        if resume.metadata.archived:
            label += " [dim](archived)[/dim]"

        branch = tree_root.add(label)
        build_tree(branch, resume, all)

    console.print(tree_root)
