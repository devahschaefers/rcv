# RCV Commands Reference

Detailed documentation for all RCV commands.

## init

Initialize a directory as your resumes directory.

```bash
rcv init [PATH]
```

**Arguments:**
- `PATH` (optional): Directory path. Defaults to current directory.

**Examples:**
```bash
rcv init ~/resumes
rcv init .
rcv init    # Uses current directory
```

**Notes:**
- Creates the directory if it doesn't exist
- Creates project-local config at `.rcv.toml`
- Run commands from this project directory (or any child directory)
- Also creates `assets/latex/preamble.tex` and `assets/typst/resume_config.typ` under the resumes directory for shared macros/config (optional to use)

---

## new

Create a new base resume.

```bash
rcv new <NAME> [--format FORMAT] [--from SOURCE_FILE]
```

**Arguments:**
- `NAME`: Name for the resume (becomes folder name)

**Options:**
- `-f, --format`: Resume format (`latex` or `typst`). Defaults to config setting.
- `-s, --from`: Create a new base resume from a `.tex`/`.typ` file path (absolute, cwd-relative, or project-root-relative).

**Examples:**
```bash
rcv new swe
rcv new designer --format typst
rcv new principal --from /path/to/main.tex
```

**Notes:**
- Creates a new folder with a template resume file
- Template includes basic structure (contact, experience, education, skills)
- When using `--from`, it copies the source file content and format
- `--from` accepts only a `.tex`/`.typ` file path (absolute, cwd-relative, or project-root-relative)
- `--format` must match the source format when used with `--from`
- When `--from` is given a file path, the source file is copied into the new resume folder and renamed to `resume.tex` / `resume.typ`

---

## branch

Create a variant (branch) of an existing resume.

```bash
rcv branch <SOURCE> <NAME> [--from SEED_FILE]
```

**Arguments:**
- `SOURCE`: Name of the resume to branch from
- `NAME`: Name for the new variant

**Examples:**
```bash
rcv branch swe google                        # Creates swe/variants/google
rcv branch swe/google meta                   # Creates swe/variants/google/variants/meta
rcv branch swe/google meta --from /tmp/base.tex  # Seeds from file but places under swe/google/variants/meta
```

**Notes:**
- Copies the resume file from the source by default
- Optional `--from` seeds content from a `.tex`/`.typ` file path (absolute, cwd-relative, or project-root-relative)
- Seed file format must match the source resume format; otherwise an error is raised
- Seed file is copied into the new variant as `resume.tex` / `resume.typ`
- Creates new metadata with current timestamp
- Inherits the format (latex/typst) from source

---

## list

List all resumes in a table format.

```bash
rcv list [--all] [--tags TAGS]
```

**Options:**
- `-a, --all`: Include archived resumes
- `-t, --tags`: Filter by tags (comma-separated)

**Examples:**
```bash
rcv list
rcv list --all
rcv list --tags faang,applied
```

**Output columns:**
- Name (full path like `swe/google`)
- Format (latex/typst)
- Tags
- Updated date
- Status (archived or empty)

---

## tree

Display resumes as a branching tree.

```bash
rcv tree [--all]
```

**Options:**
- `-a, --all`: Include archived resumes

**Examples:**
```bash
rcv tree
```

**Sample output:**
```
Resumes
├── swe
│   ├── google [faang, applied]
│   └── ml
│       └── startup
└── designer
```

---

## build

Compile a resume to PDF.

```bash
rcv build <NAME> [--output DIR]
```

**Arguments:**
- `NAME`: Name of the resume to build

**Options:**
- `-o, --output`: Output directory for PDF. If omitted, uses `.rcv.toml` defaults and writes to `<output_dir>/<resume-path>/<output_pdf_name>.pdf`.

**Examples:**
```bash
rcv build swe
rcv build swe/google
rcv build swe/google -o ~/Documents/
```

**Notes:**
- For LaTeX: Runs compiler twice (for references)
- Errors are displayed if compilation fails
- Requires appropriate compiler installed (pdflatex/typst)
- LaTeX builds support resume paths with spaces and iCloud-style `~` segments
- LaTeX intermediate files (`.aux`, `.log`, `.out`) are cleaned up after each build
- Default output mirrors resume hierarchy under configured `output_dir`

---

## tag

Add a tag to a resume.

```bash
rcv tag <NAME> <TAG>
```

**Arguments:**
- `NAME`: Resume name
- `TAG`: Tag to add

**Examples:**
```bash
rcv tag swe/google faang
rcv tag swe/google applied
```

---

## untag

Remove a tag from a resume.

```bash
rcv untag <NAME> <TAG>
```

**Arguments:**
- `NAME`: Resume name
- `TAG`: Tag to remove

**Examples:**
```bash
rcv untag swe/google applied
```

---

## watch

Watch a resume for changes and auto-rebuild.

```bash
rcv watch <NAME> [--output DIR]
```

**Arguments:**
- `NAME`: Resume name to watch

**Options:**
- `-o, --output`: Output directory for PDF. If omitted, uses `.rcv.toml` defaults and writes to `<output_dir>/<resume-path>/<output_pdf_name>.pdf`.

**Examples:**
```bash
rcv watch swe
rcv watch swe/google -o ~/Documents/
```

**Notes:**
- Does an initial build when started
- Rebuilds automatically when the resume file changes
- Press `Ctrl+C` to stop watching
- Uses 1-second debounce to avoid rapid rebuilds
- For LaTeX resumes, watch mode supports paths with spaces and iCloud-style `~` segments
- LaTeX intermediate files (`.aux`, `.log`, `.out`) are cleaned up after each rebuild
- Default output mirrors resume hierarchy under configured `output_dir`

---

## archive

Archive or unarchive a resume.

```bash
rcv archive <NAME> [--unarchive]
```

**Arguments:**
- `NAME`: Resume name

**Options:**
- `-u, --unarchive`: Unarchive instead of archiving

**Examples:**
```bash
rcv archive swe/old-version
rcv archive swe/old-version --unarchive
```

**Notes:**
- Archived resumes are hidden from `list` and `tree` by default
- Use `--all` flag with those commands to see archived resumes
- Doesn't delete any files

---

## diff

Show differences between two resumes.

```bash
rcv diff <A> <B> [--context LINES]
```

**Arguments:**
- `A`: First resume name
- `B`: Second resume name

**Options:**
- `-c, --context`: Number of context lines (default: 3)

**Examples:**
```bash
rcv diff swe swe/google
rcv diff swe/google swe/amazon -c 5
```

**Notes:**
- Shows unified diff format with syntax highlighting
- Useful for seeing what changed between base and variant
