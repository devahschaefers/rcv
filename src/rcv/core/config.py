"""Configuration management for RCV."""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import yaml


CONFIG_DIR = Path.home() / ".config" / "rcv"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


@dataclass
class Config:
    """Global RCV configuration."""

    resumes_dir: Optional[Path] = None
    default_format: str = "latex"  # latex or typst
    latex_compiler: str = "pdflatex"  # pdflatex, xelatex, lualatex
    typst_compiler: str = "typst"

    @classmethod
    def load(cls) -> "Config":
        """Load config from file, creating defaults if needed."""
        if not CONFIG_FILE.exists():
            return cls()

        with open(CONFIG_FILE) as f:
            data = yaml.safe_load(f) or {}

        resumes_dir = data.get("resumes_dir")
        return cls(
            resumes_dir=Path(resumes_dir) if resumes_dir else None,
            default_format=data.get("default_format", "latex"),
            latex_compiler=data.get("latex_compiler", "pdflatex"),
            typst_compiler=data.get("typst_compiler", "typst"),
        )

    def save(self) -> None:
        """Save config to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        data = {
            "resumes_dir": str(self.resumes_dir) if self.resumes_dir else None,
            "default_format": self.default_format,
            "latex_compiler": self.latex_compiler,
            "typst_compiler": self.typst_compiler,
        }

        with open(CONFIG_FILE, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    def get_resumes_dir(self) -> Path:
        """Get the resumes directory, raising an error if not configured."""
        if self.resumes_dir is None:
            raise ValueError(
                "Resumes directory not configured. Run 'rcv init <path>' first."
            )
        return self.resumes_dir
