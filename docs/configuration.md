# Configuration

RCV uses a YAML configuration file stored at `~/.config/rcv/config.yaml`.

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `resumes_dir` | (none) | Path to your resumes directory |
| `default_format` | `latex` | Default format for new resumes (`latex` or `typst`) |
| `latex_compiler` | `pdflatex` | LaTeX compiler to use |
| `typst_compiler` | `typst` | Typst compiler command |

## Example Configuration

```yaml
resumes_dir: /home/user/resumes
default_format: latex
latex_compiler: pdflatex
typst_compiler: typst
```

## Setting the Resumes Directory

The easiest way to set up your resumes directory is with `rcv init`:

```bash
rcv init ~/resumes
```

This creates the directory if needed and saves the path to the config file.

## Changing the LaTeX Compiler

If you need XeTeX (for custom fonts) or LuaTeX:

```yaml
latex_compiler: xelatex
# or
latex_compiler: lualatex
```

## Using Typst by Default

To create all new resumes in Typst format:

```yaml
default_format: typst
```

Or specify format per-resume:

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

This metadata is managed automatically by RCV commands:
- `created_at` / `updated_at`: Set automatically
- `tags`: Managed with `rcv tag` / `rcv untag`
- `format`: Set when creating resume
- `archived`: Set with `rcv archive`
- `notes`: Currently not exposed via CLI (edit manually if needed)
