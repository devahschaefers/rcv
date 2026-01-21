# Agent Instructions

## Documentation Policy

**ALWAYS update documentation when making changes to the codebase.**

When adding, modifying, or removing features:

1. Update `README.md` with any user-facing changes
2. Update `docs/` files for detailed documentation
3. Keep command help text (docstrings) in sync with actual behavior
4. Update examples if command syntax changes

## Project Structure

```
src/rcv/
├── cli.py           # Main entry point, command registration
├── commands/        # One file per command
├── core/            # Business logic (config, resume model)
└── utils/           # Shared utilities
```

## Adding a New Command

1. Create `src/rcv/commands/<command>.py`
2. Import and register in `src/rcv/cli.py`
3. Add to `docs/commands.md`
4. Add to `README.md` commands table
5. Test with `uv run rcv <command> --help`

## Testing Changes

```bash
uv sync                    # Install/update dependencies
uv run rcv --help          # Test CLI
uv run rcv <command>       # Test specific command
```
