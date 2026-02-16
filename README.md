# RCV - Resume Control Versioning

A CLI tool for managing versioned resumes with branching support.

## Installation

```bash
# Clone and install
cd resume_org
uv sync

# Run directly
uv run rcv --help

# Or install globally with pipx
pipx install .
rcv --help
```

## Quick Start

```bash
# 1. Initialize your resumes directory
rcv init ~/resumes

# 2. Create your first resume
rcv new swe

# 3. Edit the resume
# Opens ~/resumes/swe/resume.tex

# 4. Create variants for different roles/companies
rcv branch swe google
rcv branch swe ml

# 5. Create sub-variants
rcv branch swe/ml startup

# 6. View your resume hierarchy
rcv tree
```

## Commands

| Command | Description |
|---------|-------------|
| `rcv init [path]` | Initialize a directory as an RCV project |
| `rcv new <name>` | Create a new base resume (optionally from existing) |
| `rcv branch <source> <name>` | Create a variant of an existing resume |
| `rcv list` | List all resumes in a table |
| `rcv tree` | Display resume hierarchy as a tree |
| `rcv build <name>` | Compile resume to PDF |
| `rcv tag <name> <tag>` | Add a tag to a resume |
| `rcv untag <name> <tag>` | Remove a tag from a resume |
| `rcv watch <name>` | Auto-rebuild on file changes |
| `rcv archive <name>` | Archive a resume (hide from listings) |
| `rcv diff <a> <b>` | Show differences between two resumes |

### Shared Assets

When you run `rcv init`, the tool also creates an `assets/` directory inside your resumes directory:

- `assets/latex/preamble.tex` — LaTeX preamble (macros, header styles, spacing). Include it in your LaTeX resumes with `\input{../assets/latex/preamble.tex}` (adjust the relative path as needed).
- `assets/typst/resume_config.typ` — Typst config/macros for similar spacing and helpers. Import with `#import "../assets/typst/resume_config.typ": *`.

These files are optional; `rcv new` still creates a blank resume. Edit the assets to fit your style.

You can also seed a new resume from an existing `.tex`/`.typ` file using `--from`:

```bash
rcv new data-eng --from /path/to/main.tex
```
When using `--from` with a file path, the source file is copied into the new resume folder and renamed to `resume.tex` / `resume.typ`.

Branching with an external seed:

```bash
rcv branch swe/google meta --from /path/to/main.tex
```
This creates `swe/variants/google/variants/meta/` and copies the seed file to `resume.tex`.

See [docs/commands.md](docs/commands.md) for detailed documentation.

## Resume Directory Structure

```
~/resumes/
├── swe/                      # Base SWE resume
│   ├── resume.tex            # The actual resume
│   ├── .meta.json            # Metadata (tags, dates, etc.)
│   └── variants/
│       ├── google/           # Google-specific variant
│       │   ├── resume.tex
│       │   └── .meta.json
│       └── ml/               # ML-focused variant
│           ├── resume.tex
│           ├── .meta.json
│           └── variants/
│               └── startup/  # ML + startup variant
│                   ├── resume.tex
│                   └── .meta.json
```

## Configuration

RCV uses a project-local config file at `<project>/.rcv.toml`.
RCV discovers this file by walking upward from your current working directory.

```toml
default_format = "latex"       # latex or typst
latex_compiler = "pdflatex"    # pdflatex, xelatex, or lualatex
typst_compiler = "typst"
output_dir = "PDFs"
output_pdf_name = "resume"
```

Default PDF output layout (when `--output` is not provided):

```text
<project>/PDFs/<resume-name-path>/resume.pdf
```

Example:

```text
DataEngineer/google  ->  PDFs/DataEngineer/google/resume.pdf
```

## Supported Formats

- **LaTeX**: Uses `pdflatex` by default (configurable to `xelatex` or `lualatex`)
- **Typst**: Modern alternative to LaTeX, uses `typst compile`

Create a Typst resume:
```bash
rcv new modern-resume --format typst
```

## Examples

### Workflow for Job Applications

```bash
# Create base resume
rcv new swe

# Create company-specific variants
rcv branch swe google
rcv branch swe amazon
rcv branch swe startup

# Create a new base resume from an existing file
rcv new principal --from /path/to/main.tex

# Branch from an existing resume but seed content from a file
rcv branch swe/google meta --from /path/to/main.tex

# Tag resumes as you apply
rcv tag swe/google applied
rcv tag swe/google faang

# Build PDF for application
rcv build swe/google

# Archive old variants
rcv archive swe/old-company
```

### Watch Mode for Editing

```bash
# Start watching - auto-rebuilds PDF on save
rcv watch swe/google

# Edit resume.tex in your favorite editor
# PDF updates automatically on save
# Press Ctrl+C to stop
# LaTeX watch/build supports paths with spaces and iCloud-style "~" segments
# LaTeX intermediate files (.aux/.log/.out) are cleaned up automatically
# Default output path mirrors resume hierarchy under PDFs/
```

### Comparing Variants

```bash
# See what changed between base and variant
rcv diff swe swe/google
```

## Requirements

- Python 3.10+
- For LaTeX: `pdflatex`, `xelatex`, or `lualatex`
- For Typst: `typst` CLI
