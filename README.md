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
| `rcv init [path]` | Initialize a directory as your resumes directory |
| `rcv new <name>` | Create a new base resume |
| `rcv branch <source> <name>` | Create a variant of an existing resume |
| `rcv list` | List all resumes in a table |
| `rcv tree` | Display resume hierarchy as a tree |
| `rcv build <name>` | Compile resume to PDF |
| `rcv tag <name> <tag>` | Add a tag to a resume |
| `rcv untag <name> <tag>` | Remove a tag from a resume |
| `rcv watch <name>` | Auto-rebuild on file changes |
| `rcv archive <name>` | Archive a resume (hide from listings) |
| `rcv diff <a> <b>` | Show differences between two resumes |

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

Global config is stored at `~/.config/rcv/config.yaml`:

```yaml
resumes_dir: /home/user/resumes
default_format: latex          # latex or typst
latex_compiler: pdflatex       # pdflatex, xelatex, or lualatex
typst_compiler: typst
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
