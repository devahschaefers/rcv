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
- Saves the path to `~/.config/rcv/config.yaml`
- You only need to run this once
- Also creates `assets/latex/preamble.tex` and `assets/typst/resume_config.typ` under the resumes directory for shared macros/config (optional to use)

---

## new

Create a new base resume.

```bash
rcv new <NAME> [--format FORMAT] [--from SOURCE]
```

**Arguments:**
- `NAME`: Name for the resume (becomes folder name)

**Options:**
- `-f, --format`: Resume format (`latex` or `typst`). Defaults to config setting.
- `-s, --from`: Create a new base resume from an existing resume name **or** a path to a `.tex`/`.typ` file.

**Examples:**
```bash
rcv new swe
rcv new designer --format typst
rcv new principal --from swe/google
```

**Notes:**
- Creates a new folder with a template resume file
- Template includes basic structure (contact, experience, education, skills)
- When using `--from`, it copies the source resume content and format
- `--from` accepts either a managed resume name (e.g., `swe/google`) or a direct `.tex`/`.typ` file path
- `--format` must match the source format when used with `--from`
- When `--from` is given a file path, the source file is moved into the new resume folder and renamed to `resume.tex` / `resume.typ`

---

## branch

Create a variant (branch) of an existing resume.

```bash
rcv branch <SOURCE> <NAME>
```

**Arguments:**
- `SOURCE`: Name of the resume to branch from
- `NAME`: Name for the new variant

**Examples:**
```bash
rcv branch swe google           # Creates swe/variants/google
rcv branch swe/google meta      # Creates swe/variants/google/variants/meta
```

**Notes:**
- Copies the resume file from the source
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
- `-o, --output`: Output directory for PDF. Defaults to resume directory.

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
- `-o, --output`: Output directory for PDF

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
