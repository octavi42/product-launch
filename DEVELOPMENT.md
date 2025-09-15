# Development Guide

## 🚀 Quick Commands

```bash
# Format all code automatically
make format
# or
python fix_code.py

# Run linting
make lint

# Start the application
make run

# Test the application
make test

# Full setup
make setup
```

## 🔧 Code Formatting

The project uses automatic code formatting with:

- **Black** - Code formatter (88 character line length)
- **isort** - Import sorter (Black-compatible)
- **autopep8** - PEP8 compliance fixer
- **flake8** - Linter (with relaxed rules for Black compatibility)

### Configuration Files

- `.flake8` - Flake8 configuration
- `pyproject.toml` - Black and isort configuration
- `.vscode/settings.json` - VS Code auto-formatting

### Line Length

- **88 characters** (Black default, more readable than 79)
- Auto-wrapping for long lines
- Ignored rules: E203, W503, E501 (Black compatibility)

## 🎯 Hackathon Ready

Your code is now:

- ✅ Properly formatted
- ✅ PEP8 compliant
- ✅ Import organized
- ✅ Lint-free
- ✅ Ready for demo

## 🔄 Workflow

1. Write code
2. Run `make format` to auto-fix
3. Run `make lint` to check
4. Run `make test` to verify
5. Run `make run` to start

## 📝 Notes

- All formatting is automatic
- No manual line breaking needed
- Black handles complex formatting decisions
- VS Code will format on save
