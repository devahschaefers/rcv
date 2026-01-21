"""Resume model and metadata handling."""

from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import json


METADATA_FILE = ".meta.json"
VARIANTS_DIR = "variants"


@dataclass
class ResumeMetadata:
    """Metadata for a resume."""

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    format: str = "latex"  # latex or typst
    archived: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "notes": self.notes,
            "format": self.format,
            "archived": self.archived,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ResumeMetadata":
        """Create from dictionary."""
        return cls(
            created_at=datetime.fromisoformat(
                data.get("created_at", datetime.now().isoformat())
            ),
            updated_at=datetime.fromisoformat(
                data.get("updated_at", datetime.now().isoformat())
            ),
            tags=data.get("tags", []),
            notes=data.get("notes", ""),
            format=data.get("format", "latex"),
            archived=data.get("archived", False),
        )

    def save(self, path: Path) -> None:
        """Save metadata to file."""
        self.updated_at = datetime.now()
        meta_file = path / METADATA_FILE
        with open(meta_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "ResumeMetadata":
        """Load metadata from file."""
        meta_file = path / METADATA_FILE
        if not meta_file.exists():
            return cls()

        with open(meta_file) as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class Resume:
    """Represents a resume in the system."""

    path: Path
    metadata: ResumeMetadata

    @property
    def name(self) -> str:
        """Get the resume name (last part of path)."""
        return self.path.name

    @property
    def full_name(self) -> str:
        """Get the full resume name including parent path."""
        # Get path relative to resumes_dir, excluding 'variants' directories
        parts = []
        for part in self.path.parts:
            if part != VARIANTS_DIR:
                parts.append(part)
        return "/".join(parts[-self._depth() :]) if parts else self.name

    def _depth(self) -> int:
        """Calculate depth by counting 'variants' in path."""
        return str(self.path).count(VARIANTS_DIR) + 1

    @property
    def parent_path(self) -> Optional[Path]:
        """Get the parent resume path, if this is a variant."""
        if VARIANTS_DIR not in self.path.parts:
            return None

        # Go up past 'variants' directory
        idx = list(self.path.parts).index(VARIANTS_DIR)
        return Path(*self.path.parts[:idx])

    @property
    def parent_name(self) -> Optional[str]:
        """Get the parent resume name."""
        parent = self.parent_path
        return parent.name if parent else None

    @property
    def variants_dir(self) -> Path:
        """Get the variants directory for this resume."""
        return self.path / VARIANTS_DIR

    @property
    def resume_file(self) -> Path:
        """Get the main resume file path."""
        ext = ".tex" if self.metadata.format == "latex" else ".typ"
        return self.path / f"resume{ext}"

    def get_variants(self) -> List["Resume"]:
        """Get all direct variants of this resume."""
        variants = []
        variants_path = self.variants_dir

        if not variants_path.exists():
            return variants

        for item in variants_path.iterdir():
            if item.is_dir() and (item / METADATA_FILE).exists():
                variants.append(Resume.load(item))

        return sorted(variants, key=lambda r: r.name)

    def get_all_descendants(self) -> List["Resume"]:
        """Get all variants recursively."""
        descendants = []
        for variant in self.get_variants():
            descendants.append(variant)
            descendants.extend(variant.get_all_descendants())
        return descendants

    def save(self) -> None:
        """Save resume metadata."""
        self.metadata.save(self.path)

    @classmethod
    def load(cls, path: Path) -> "Resume":
        """Load a resume from a directory."""
        metadata = ResumeMetadata.load(path)
        return cls(path=path, metadata=metadata)

    @classmethod
    def create(
        cls,
        path: Path,
        format: str = "latex",
        template_content: Optional[str] = None,
    ) -> "Resume":
        """Create a new resume."""
        path.mkdir(parents=True, exist_ok=True)

        metadata = ResumeMetadata(format=format)
        metadata.save(path)

        # Create the resume file
        ext = ".tex" if format == "latex" else ".typ"
        resume_file = path / f"resume{ext}"

        if template_content:
            resume_file.write_text(template_content)
        else:
            # Write a minimal template
            if format == "latex":
                resume_file.write_text(LATEX_TEMPLATE)
            else:
                resume_file.write_text(TYPST_TEMPLATE)

        return cls(path=path, metadata=metadata)


def get_all_resumes(resumes_dir: Path) -> List[Resume]:
    """Get all resumes in the resumes directory."""
    resumes = []

    if not resumes_dir.exists():
        return resumes

    # Find all directories with .meta.json
    for meta_file in resumes_dir.rglob(METADATA_FILE):
        resume_path = meta_file.parent
        resumes.append(Resume.load(resume_path))

    return sorted(resumes, key=lambda r: r.full_name)


def get_root_resumes(resumes_dir: Path) -> List[Resume]:
    """Get only root-level resumes (not variants)."""
    resumes = []

    if not resumes_dir.exists():
        return resumes

    for item in resumes_dir.iterdir():
        if item.is_dir() and (item / METADATA_FILE).exists():
            resumes.append(Resume.load(item))

    return sorted(resumes, key=lambda r: r.name)


def find_resume(resumes_dir: Path, name: str) -> Optional[Resume]:
    """Find a resume by name.

    Name can be:
    - Simple name: "swe" -> finds resumes_dir/swe
    - Path name: "swe/google" -> finds resumes_dir/swe/variants/google
    """
    # Handle path-style names
    parts = name.split("/")

    if len(parts) == 1:
        # Simple name - could be anywhere
        for resume in get_all_resumes(resumes_dir):
            if resume.name == name:
                return resume
        return None

    # Path-style name - build the actual path
    path = resumes_dir / parts[0]
    for part in parts[1:]:
        path = path / VARIANTS_DIR / part

    if (path / METADATA_FILE).exists():
        return Resume.load(path)

    return None


# Templates

LATEX_TEMPLATE = r"""\documentclass[11pt,a4paper]{article}

\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}

\begin{document}

\begin{center}
    {\LARGE \textbf{Your Name}}\\[0.5em]
    your.email@example.com | (555) 123-4567 | City, State\\
    \href{https://linkedin.com/in/yourprofile}{LinkedIn} | 
    \href{https://github.com/yourusername}{GitHub}
\end{center}

\section*{Experience}
\textbf{Job Title} \hfill Company Name\\
\textit{Start Date -- End Date} \hfill Location
\begin{itemize}[leftmargin=*, nosep]
    \item Accomplishment or responsibility
    \item Another accomplishment
\end{itemize}

\section*{Education}
\textbf{Degree} \hfill Institution\\
\textit{Graduation Date} \hfill Location

\section*{Skills}
\textbf{Languages:} Python, JavaScript, etc.\\
\textbf{Tools:} Git, Docker, etc.

\end{document}
"""

TYPST_TEMPLATE = """#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(size: 20pt, weight: "bold")[Your Name]
  
  your.email\\@example.com | (555) 123-4567 | City, State
  
  #link("https://linkedin.com/in/yourprofile")[LinkedIn] |
  #link("https://github.com/yourusername")[GitHub]
]

= Experience

*Job Title* #h(1fr) Company Name \\
_Start Date -- End Date_ #h(1fr) Location

- Accomplishment or responsibility
- Another accomplishment

= Education

*Degree* #h(1fr) Institution \\
_Graduation Date_ #h(1fr) Location

= Skills

*Languages:* Python, JavaScript, etc. \\
*Tools:* Git, Docker, etc.
"""
