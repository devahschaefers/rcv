"""Main CLI entry point for RCV."""

import typer
from rich.console import Console

from rcv.commands import (
    init,
    new,
    branch,
    list_cmd,
    tree,
    build,
    tag,
    watch,
    archive,
    diff,
    completion,
)

app = typer.Typer(
    name="rcv",
    help="Resume Control Versioning - Manage versioned resumes with branching support",
    no_args_is_help=True,
    add_completion=True,
)

console = Console()

# Register commands
app.command(name="init")(init.init)
app.command(name="new")(new.new)
app.command(name="branch")(branch.branch)
app.command(name="list")(list_cmd.list_resumes)
app.command(name="tree")(tree.tree)
app.command(name="build")(build.build)
app.command(name="tag")(tag.tag)
app.command(name="untag")(tag.untag)
app.command(name="watch")(watch.watch)
app.command(name="archive")(archive.archive)
app.command(name="diff")(diff.diff)
app.command(name="setup-fish-completion")(completion.setup_fish_completion)


@app.callback()
def main():
    """RCV - Resume Control Versioning"""
    pass


if __name__ == "__main__":
    app()
