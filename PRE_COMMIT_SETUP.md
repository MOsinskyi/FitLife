# Pre-commit Hooks Setup Guide

This project uses [pre-commit](https://pre-commit.com/) to automatically check code quality before commits.

## What is Pre-commit?

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It runs automated checks on your code before you commit, ensuring code quality and consistency.

## Installation

### 1. Install Dependencies

```bash
make install
```

This will install all required dev dependencies including pre-commit.

### 2. Install Pre-commit Hooks

```bash
make pre-commit-install
```

Or manually:

```bash
cd backend
poetry run pre-commit install
```

## Usage

### Automatic (Recommended)

Once installed, pre-commit hooks will run automatically on `git commit`. If any check fails, the commit will be aborted and you'll need to fix the issues.

### Manual Runs

Run on staged files only:

```bash
make pre-commit-run
```

Run on all files in the repository:

```bash
make pre-commit-all
```

### Skip Hooks (Use Sparingly)

If you need to commit without running hooks (not recommended):

```bash
git commit --no-verify -m "your message"
```

## What Checks Are Included?

### Code Formatting

- **Black**: Python code formatter (line length: 100)
- **isort**: Import statement sorter
- **Ruff Format**: Fast modern formatter
- **Prettier**: YAML, JSON, and Markdown formatter

### Code Quality & Linting

- **Ruff**: Fast Python linter (replaces flake8, pylint)
  - Checks for code errors, style issues, and best practices
  - Auto-fixes many issues
- **MyPy**: Static type checker
  - Helps catch type-related bugs

### Security

- **Bandit**: Security vulnerability scanner
  - Detects common security issues in Python code
- **Safety**: Checks for known security vulnerabilities in dependencies
- **detect-private-key**: Prevents committing private keys

### General File Quality

- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml/json/toml**: Validates file syntax
- **check-merge-conflict**: Detects merge conflict markers
- **debug-statements**: Prevents committing debug code
- **check-ast**: Validates Python syntax

## Configuration

### Main Configuration

Pre-commit hooks are configured in `.pre-commit-config.yaml` at the project root.

### Tool Configurations

Individual tool settings are in `backend/pyproject.toml`:

- `[tool.black]` - Black formatter settings
- `[tool.isort]` - Import sorter settings
- `[tool.ruff]` - Ruff linter settings
- `[tool.mypy]` - MyPy type checker settings
- `[tool.bandit]` - Bandit security scanner settings

## Updating Hooks

Pre-commit hooks can be updated to their latest versions:

```bash
cd backend
poetry run pre-commit autoupdate
```

## Troubleshooting

### Hook Installation Failed

Make sure you're in the backend directory and poetry is installed:

```bash
cd backend
poetry install
poetry run pre-commit install
```

### Hook is Slow

Some hooks (like mypy, bandit) can be slow on first run. They cache results and subsequent runs are faster.

You can skip slow hooks during development:

```bash
SKIP=mypy,bandit git commit -m "your message"
```

### Clear Hook Cache

If hooks are behaving strangely:

```bash
cd backend
poetry run pre-commit clean
poetry run pre-commit install --install-hooks
```

## CI/CD Integration

Pre-commit checks are also integrated into the CI/CD pipeline. The same checks that run locally will run in CI, ensuring consistency.

## Best Practices

1. **Run hooks before committing**: Let pre-commit catch issues early
2. **Fix issues, don't skip**: Skipping hooks defeats their purpose
3. **Keep hooks updated**: Run `pre-commit autoupdate` regularly
4. **Add new hooks carefully**: Test them first with `pre-commit run --all-files`

## Getting Help

- Pre-commit documentation: https://pre-commit.com/
- Ruff documentation: https://docs.astral.sh/ruff/
- Black documentation: https://black.readthedocs.io/
- MyPy documentation: https://mypy.readthedocs.io/
