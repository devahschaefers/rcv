"""Shell completion helpers for CLI commands."""

from pathlib import Path
from typing import List

import click
from click.shell_completion import CompletionItem

from rcv.core.config import Config
from rcv.core.resume import Resume, get_all_resumes


def _load_resumes() -> List[Resume]:
    """Load all resumes from the current project context, if available."""
    try:
        config = Config.load()
        resumes_dir = config.get_resumes_dir()
    except Exception:
        return []

    return get_all_resumes(resumes_dir)


def _resume_help_text(name: str, resume: Resume | None, has_children: bool) -> str:
    """Build completion help text for a resume candidate."""
    if resume is None:
        return "resume path"

    kind = "variant" if "/" in name else "base resume"
    details = [kind, resume.metadata.format]
    if has_children:
        details.append("has variants")
    if resume.metadata.archived:
        details.append("archived")
    return ", ".join(details)


def complete_resume_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    """Complete resume names and nested variant paths.

    Completion is hierarchical:
    - Top-level input (no slash) completes root resumes.
    - Path input (with slash) completes the next variant segment.
    - If input is an exact resume name that has variants, show child variants.
    """
    resumes = _load_resumes()
    if not resumes:
        return []

    by_name = {resume.full_name: resume for resume in resumes}
    all_names = set(by_name)

    exact_name = incomplete.rstrip("/")
    force_children = (
        bool(exact_name)
        and not incomplete.endswith("/")
        and exact_name in all_names
        and any(name.startswith(f"{exact_name}/") for name in all_names)
    )

    if force_children:
        prefix_parts = exact_name.split("/")
        partial = ""
    elif "/" in incomplete:
        if incomplete.endswith("/"):
            prefix_parts = [part for part in incomplete.split("/") if part]
            partial = ""
        else:
            parts = incomplete.split("/")
            prefix_parts = parts[:-1]
            partial = parts[-1]
    else:
        prefix_parts = []
        partial = incomplete

    candidates: dict[str, dict[str, object]] = {}
    prefix_len = len(prefix_parts)

    for full_name, resume in by_name.items():
        parts = full_name.split("/")
        if len(parts) <= prefix_len:
            continue
        if parts[:prefix_len] != prefix_parts:
            continue

        next_part = parts[prefix_len]
        if partial and not next_part.startswith(partial):
            continue

        candidate = "/".join(prefix_parts + [next_part]) if prefix_parts else next_part
        info = candidates.setdefault(
            candidate,
            {"resume": None, "has_children": False},
        )

        if len(parts) > prefix_len + 1:
            info["has_children"] = True

        if len(parts) == prefix_len + 1 and full_name == candidate:
            info["resume"] = resume

    items = []
    for name in sorted(candidates):
        info = candidates[name]
        resume = info["resume"]  # type: ignore[assignment]
        has_children = bool(info["has_children"])
        value = f"{name}/" if has_children else name
        items.append(
            CompletionItem(
                value,
                help=_resume_help_text(name, resume, has_children),
            )
        )

    # Deduplicate while preserving order.
    deduped: list[CompletionItem] = []
    seen: set[str] = set()
    for item in items:
        if item.value in seen:
            continue
        seen.add(item.value)
        deduped.append(item)
    return deduped


def complete_resume_format(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    """Complete supported resume formats."""
    formats = [
        CompletionItem("latex", help="LaTeX (.tex)"),
        CompletionItem("typst", help="Typst (.typ)"),
    ]
    return [item for item in formats if item.value.startswith(incomplete)]


def complete_seed_file(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    """Complete .tex/.typ file paths for --from seed options."""
    path = Path(incomplete).expanduser() if incomplete else Path(".")

    if incomplete.endswith("/"):
        parent = path
        name_prefix = ""
        token_prefix = incomplete
    else:
        parent = path.parent if str(path.parent) != "" else Path(".")
        name_prefix = path.name
        token_prefix = incomplete[: len(incomplete) - len(name_prefix)]

    if not parent.is_absolute():
        parent = (Path.cwd() / parent).resolve()

    if not parent.exists() or not parent.is_dir():
        return []

    items: list[CompletionItem] = []
    for child in sorted(parent.iterdir(), key=lambda p: p.name):
        if not child.name.startswith(name_prefix):
            continue

        if child.is_dir():
            suffix = "/" if not incomplete.endswith("/") else ""
            display = f"{token_prefix}{child.name}{suffix}"
            items.append(CompletionItem(display, help="directory"))
            continue

        if child.suffix not in {".tex", ".typ"}:
            continue
        items.append(
            CompletionItem(
                f"{token_prefix}{child.name}",
                help=f"seed file ({child.suffix})",
            )
        )

    return items
