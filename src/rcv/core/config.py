"""Configuration management for RCV."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback for Python 3.10
    tomllib = None


CONFIG_FILE_NAME = ".rcv.toml"


def _toml_quote(value: str) -> str:
    """Quote a TOML string value."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _parse_simple_toml(content: str) -> dict[str, Any]:
    """Parse flat key=value TOML used by the local RCV config.

    This lightweight fallback is only used when tomllib is unavailable.
    """
    data: dict[str, Any] = {}

    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue

        key_part, value_part = line.split("=", 1)
        key = key_part.strip()
        value = value_part.strip()

        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            parsed_value = value[1:-1]
            parsed_value = parsed_value.replace('\\"', '"').replace("\\\\", "\\")
            data[key] = parsed_value
            continue

        if value.startswith("'") and value.endswith("'") and len(value) >= 2:
            data[key] = value[1:-1]
            continue

        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
            continue

        data[key] = value

    return data


def _read_toml_file(config_file: Path) -> dict[str, Any]:
    """Read and parse TOML configuration data."""
    if tomllib is not None:
        with open(config_file, "rb") as f:
            parsed = tomllib.load(f)
            if isinstance(parsed, dict):
                return parsed
            return {}

    return _parse_simple_toml(config_file.read_text())


@dataclass
class Config:
    """Project-local RCV configuration."""

    project_dir: Optional[Path] = None
    default_format: str = "latex"  # latex or typst
    latex_compiler: str = "pdflatex"  # pdflatex, xelatex, lualatex
    typst_compiler: str = "typst"
    output_dir: Optional[str] = None
    output_pdf_name: Optional[str] = None

    @classmethod
    def _find_project_dir(cls, start_dir: Optional[Path] = None) -> Optional[Path]:
        """Find project root by searching for .rcv.toml upward from start_dir."""
        current = (start_dir or Path.cwd()).resolve()
        candidates = [current, *current.parents]

        for candidate in candidates:
            if (candidate / CONFIG_FILE_NAME).exists():
                return candidate

        return None

    @classmethod
    def load(cls, start_dir: Optional[Path] = None) -> "Config":
        """Load config from the nearest project .rcv.toml, if available."""
        project_dir = cls._find_project_dir(start_dir)
        if project_dir is None:
            return cls()

        config_file = project_dir / CONFIG_FILE_NAME
        data = _read_toml_file(config_file)

        return cls(
            project_dir=project_dir,
            default_format=str(data.get("default_format", "latex")),
            latex_compiler=str(data.get("latex_compiler", "pdflatex")),
            typst_compiler=str(data.get("typst_compiler", "typst")),
            output_dir=(
                str(data["output_dir"]) if data.get("output_dir") is not None else None
            ),
            output_pdf_name=(
                str(data["output_pdf_name"])
                if data.get("output_pdf_name") is not None
                else None
            ),
        )

    @classmethod
    def load_from_project_dir(cls, project_dir: Path) -> "Config":
        """Load config specifically from a project root path."""
        resolved = project_dir.resolve()
        config_file = resolved / CONFIG_FILE_NAME
        if not config_file.exists():
            return cls(project_dir=resolved)

        data = _read_toml_file(config_file)
        return cls(
            project_dir=resolved,
            default_format=str(data.get("default_format", "latex")),
            latex_compiler=str(data.get("latex_compiler", "pdflatex")),
            typst_compiler=str(data.get("typst_compiler", "typst")),
            output_dir=(
                str(data["output_dir"]) if data.get("output_dir") is not None else None
            ),
            output_pdf_name=(
                str(data["output_pdf_name"])
                if data.get("output_pdf_name") is not None
                else None
            ),
        )

    def save(self) -> None:
        """Save config to the project-local .rcv.toml file."""
        project_dir = self.get_resumes_dir()
        config_file = project_dir / CONFIG_FILE_NAME

        toml_content = (
            "# RCV project configuration\n"
            "# This file is local to this resumes project.\n\n"
            f"default_format = {_toml_quote(self.default_format)}\n"
            f"latex_compiler = {_toml_quote(self.latex_compiler)}\n"
            f"typst_compiler = {_toml_quote(self.typst_compiler)}\n"
        )
        if self.output_dir is not None:
            toml_content += f"output_dir = {_toml_quote(self.output_dir)}\n"
        if self.output_pdf_name is not None:
            toml_content += f"output_pdf_name = {_toml_quote(self.output_pdf_name)}\n"
        config_file.write_text(toml_content)

    def get_resumes_dir(self) -> Path:
        """Get the resumes directory for this project."""
        if self.project_dir is None:
            raise ValueError(
                "No .rcv.toml found in this directory tree. "
                "Run 'rcv init <path>' for your project first."
            )
        return self.project_dir

    def get_output_root_dir(self) -> Path:
        """Get absolute output root directory for generated PDFs."""
        if self.output_dir is None:
            raise ValueError("output_dir is not configured.")
        output_root = Path(self.output_dir).expanduser()
        if not output_root.is_absolute():
            output_root = self.get_resumes_dir() / output_root
        return output_root

    def get_output_pdf_filename(self) -> str:
        """Get normalized output PDF filename."""
        if self.output_pdf_name is None:
            raise ValueError("output_pdf_name is not configured.")
        name = self.output_pdf_name.strip() or "resume"
        if name.lower().endswith(".pdf"):
            return name
        return f"{name}.pdf"
