# Resume Branching

RCV uses a folder-based branching system to organize resume variants.

## Concept

Instead of tracking changes over time (like git), RCV creates **snapshots** when you branch. Each variant is a complete, independent resume that you can edit freely.

The branching relationship is implicit from the folder structure - no need to track it in metadata.

## Directory Structure

```
~/resumes/
├── swe/                          # Root resume
│   ├── resume.tex
│   ├── .meta.json
│   └── variants/
│       ├── google/               # First-level variant
│       │   ├── resume.tex
│       │   ├── .meta.json
│       │   └── variants/
│       │       └── google-l5/    # Second-level variant
│       │           ├── resume.tex
│       │           └── .meta.json
│       └── ml/
│           ├── resume.tex
│           └── .meta.json
```

## Creating Branches

### From a Root Resume

```bash
rcv branch swe google
# Creates: swe/variants/google/
```

### From a Variant

```bash
rcv branch swe/google google-l5
# Creates: swe/variants/google/variants/google-l5/
```

## Naming Conventions

Use the path-style naming to reference resumes:

| Location | Name |
|----------|------|
| `~/resumes/swe/` | `swe` |
| `~/resumes/swe/variants/google/` | `swe/google` |
| `~/resumes/swe/variants/google/variants/l5/` | `swe/google/l5` |

## Viewing the Hierarchy

```bash
rcv tree
```

Output:
```
Resumes
├── swe
│   ├── google [faang]
│   │   └── google-l5
│   └── ml
└── designer
```

## When to Branch

**Create a new branch when:**
- Applying to a specific company (customize for their stack/culture)
- Targeting a different role (SWE → ML Engineer)
- Creating a significantly different version

**Don't branch when:**
- Making small updates that apply to all resumes
- Fixing typos

## Syncing Changes

RCV uses simple snapshots, so changes to a parent don't automatically flow to children.

**To update a variant with changes from the parent:**

1. Use `rcv diff` to see differences:
   ```bash
   rcv diff swe swe/google
   ```

2. Manually apply desired changes to the variant

**Future feature idea:** `rcv sync` command to pull updates from parent.

## Archiving Old Variants

Instead of deleting, archive variants you no longer need:

```bash
rcv archive swe/old-company
```

They'll be hidden from `list` and `tree` but still available if needed.
