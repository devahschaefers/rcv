# Configuration

RCV uses a project-local TOML configuration file at `.rcv.toml` in your resumes project root.

Commands discover this file by searching upward from your current working directory.

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `default_format` | `latex` | Default format for new resumes (`latex` or `typst`) |
| `latex_compiler` | `pdflatex` | LaTeX compiler to use |
| `typst_compiler` | `typst` | Typst compiler command |
| `output_dir` | `PDFs` | Root folder for default PDF output paths (relative to project root if not absolute) |
| `output_pdf_name` | `resume` | Default output PDF filename used by `build`/`watch` when `--output` is not passed |

## Example `.rcv.toml`

```toml
default_format = "latex"
latex_compiler = "pdflatex"
typst_compiler = "typst"
output_dir = "PDFs"
output_pdf_name = "resume"
```

## Setting Up a Project

Initialize a project with:

```bash
rcv init ~/resumes
```

This creates:
- `.rcv.toml` in the project root
- `assets/latex/preamble.tex`
- `assets/typst/resume_config.typ`
- Prompts for `output_dir` and `output_pdf_name`

## Default Output Layout

When `--output` is not provided, `rcv build` and `rcv watch` write PDFs to:

```text
<output_dir>/<resume-logical-path>/<output_pdf_name>.pdf
```

Examples:

```text
Resume name: swe
Output:      PDFs/swe/resume.pdf

Resume name: swe/google/meta
Output:      PDFs/swe/google/meta/resume.pdf
```

If `output_dir` or `output_pdf_name` is missing in `.rcv.toml`, `rcv build` and
`rcv watch` will prompt for values and persist them automatically.

## Changing the LaTeX Compiler

If you need XeTeX or LuaTeX, edit `.rcv.toml`:

```toml
latex_compiler = "xelatex"
# or
latex_compiler = "lualatex"
```

## Using Typst by Default

```toml
default_format = "typst"
```

Or specify per resume:

```bash
rcv new modern-resume --format typst
```

## Resume Metadata

Each resume has a `.meta.json` file with its own metadata:

```json
{
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-01-20T14:00:00",
  "tags": ["faang", "applied"],
  "notes": "Emphasized distributed systems experience",
  "format": "latex",
  "archived": false
}
```
