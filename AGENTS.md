# Agent Instructions — rainbowminer-api-client

## Project Overview

**rainbowminer-api-client** is a Python API client for [RainbowMiner](https://github.com/RainbowMiner/RainbowMiner), a multipool cryptominer. The client provides a typed Python interface to interact with the RainbowMiner local API, making it easier to monitor and control mining operations programmatically or integrate with home automation systems like Home Assistant.

## Architecture

### Project Layout (src layout)

```text
rainbowminer-api-client/
├── src/rainbowminer_api_client/   # The Python package (importable as `rainbowminer_api_client`)
│   ├── __init__.py                # Package init — public API exports go here
│   └── py.typed                   # PEP 561 marker — declares this package ships type annotations
├── tests/                         # Unit tests (pytest), mirrors src structure
│   └── test_*.py
├── pyproject.toml                 # Project metadata, build system, dependency groups, tool configs
├── uv.lock                        # Lock file for reproducible environments (commit to VCS)
├── .python-version                # Pinned Python version (3.14)
└── AGENTS.md                      # This file
```

### Key Architectural Decisions

1. **src layout** — The package lives under `src/rainbowminer_api_client/`, not the repo root. This prevents accidental imports from the source tree when tests should import the installed package. Setuptools is configured with `[tool.setuptools.packages.find] where = ["src"]` to match.

2. **Dynamic versioning via setuptools_scm** — Version is derived from git tags at build time. The `version` field in `[project]` is declared as `dynamic = ["version"]`, and `[tool.setuptools_scm]` handles resolution. A `fallback_version = "0.1.0"` ensures builds succeed even before the first git tag is created. **To release a new version, create a git tag** (e.g., `git tag 0.2.0`). Development versions are automatically generated as `0.1.1.dev1+g<commit>` style strings.

3. **PEP 561 type marker** — The `py.typed` file in the package root signals to type checkers (ty, mypy, pyright) that this package includes inline type annotations. Type annotations are **required** on all public APIs.

4. **PEP 735 dependency groups** — Dev dependencies are managed via `[dependency-groups] dev` in `pyproject.toml`, not legacy `[project.optional-dependencies]` or `[tool.uv] dev-dependencies`. This is the modern standard natively supported by `uv`. Dependencies are added with `uv add --dev <package>`.

5. **SPDX license expression** — The license is declared as `license = "MIT"` (PEP 639 SPDX string), not via license classifiers. The `License :: OSI Approved :: MIT License` classifier is **not** used because it conflicts with the SPDX expression in newer setuptools.

## Tooling

### uv-only policy — NO raw python/pip commands

**Always use `uv` for all Python-related operations.** Never use `python`, `pip`, `python -m`, `pip install`, or similar raw commands.

| Operation | Correct | Wrong |
| --------- | ------- | ----- |
| Run a Python script/tool | `uv run <script>` | `python <script>` |
| Run a module | `uv run python -m <module>` | `python -m <module>` |
| Install a runtime dependency | `uv add <package>` | `pip install <package>` |
| Install a dev dependency | `uv add --dev <package>` | `pip install <package>` |
| Sync environment from lock | `uv sync` | `pip install -r requirements.txt` |
| Build a distribution | `uv build` | `python -m build` |
| Run pytest | `uv run pytest` | `python -m pytest` |
| Run ruff format | `uv run ruff format` | `ruff format` |
| Run ruff check | `uv run ruff check` | `ruff check` |
| Run ty check | `uv run ty check` | `ty check` |
| Run pydoclint | `uv run pydoclint src tests` | `pydoclint src tests` |

The virtual environment is managed by uv in `.venv/`. There is no need to manually activate it — `uv run` handles environment isolation automatically.

## Verification Flow — ALWAYS run before completing work

**Before completing any task that modifies Python files (`.py`), configuration (`pyproject.toml`), or test files, you MUST run the verification flow.**

### Use VS Code Tasks — not individual commands

Run the verification flow using the VS Code task system, not by executing `uv run` commands individually. This ensures consistent execution order and proper problem matching.

**To verify:** Run the VS Code task named **`verify`**. This task runs all four steps below in sequence:

1. **ruff format** — `uv run ruff format` (formats the codebase)
2. **ruff lint** — `uv run ruff check` (lints for code quality issues; must pass with zero errors)
3. **ty check** — `uv run ty check` (type checks the codebase; must pass with no errors)
4. **pydoclint** — `uv run pydoclint src tests` (checks docstrings against Google style; must pass with no errors)
5. **pytest run** — `uv run pytest` (runs all unit tests; must pass)

The `verify` task uses `dependsOrder: "sequence"` so steps run one after another, stopping on first failure.

### When to run verification

- **Always** — after modifying any `.py` file
- **Always** — after modifying `pyproject.toml` (tool configs, dependencies)
- **Always** — before reporting a task as complete
- **Not needed** — for changes to `README.md`, `AGENTS.md`, `.gitignore`, or other non-Python files only

### Iterating on tests — use the VS Code Testing tool

When iterating on test failures during development, **do not** run `uv run pytest` in the terminal. Instead, use the VS Code `runTests` tool (the testing integration), passing specific `files` paths to run only the relevant test files. This is faster and provides structured pass/fail output. The `verify` task (above) is still used for the full pre-completion verification flow, but `runTests` is the preferred tool for day-to-day test iteration.

## Code Style

- **Formatter:** Ruff (line length 120, `target-version = "py314"`)
- **Linter:** Ruff with rules: `E` (pycodestyle errors), `W` (pycodestyle warnings), `F` (pyflakes), `I` (isort), `UP` (pyupgrade), `B` (flake8-bugbear), `SIM` (flake8-simplify), `C4` (flake8-comprehensions), `RUF` (ruff-specific)
- **Type checker:** ty (Astral's type checker, `python-version = "3.14"`)
- **Docstring linter:** pydoclint (Google style, checks docstrings in `src/` and `tests/`)
- **Type annotations:** Required on all public functions and methods. The package ships `py.typed` (PEP 561).
- **Test framework:** pytest (tests in `tests/`, strict markers enabled, warnings treated as errors)
- **Python version:** 3.14+ (pinned in `.python-version` and `requires-python = ">=3.14"`)

### Ruff configuration (in `pyproject.toml`)

```toml
[tool.ruff]
line-length = 120
target-version = "py314"
src = ["src"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM", "C4", "RUF"]

[tool.ruff.format]
docstring-code-format = true
```

### pytest configuration (in `pyproject.toml`)

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-ra --strict-markers"
filterwarnings = ["error"]
```

### ty configuration (in `pyproject.toml`)

```toml
[tool.ty.environment]
python-version = "3.14"

[[tool.ty.overrides]]
include = ["tests/**"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
```

The test override relaxes `possibly-unresolved-reference` to `warn` in test files, since tests may import modules that aren't fully resolved in the type-checking environment. ty checks both `src/` and `tests/` by default — the override only changes rule severity for test files, not the check scope.

### pydoclint configuration (in `pyproject.toml`)

```toml
[tool.pydoclint]
style = "google"
require-return-section-when-returning-nothing = false
require-yield-section-when-yielding-nothing = false
```

Google style docstrings are required. Functions returning `None` (no `return` statement, `-> None` annotation) do not need a "Returns" section. Similarly, generators yielding `None` do not need a "Yields" section.

## Build & Release

- **Versioning:** setuptools_scm derives the version from git tags. No manual version bumps in `pyproject.toml`.
- **Development versions:** Automatically generated (e.g., `0.1.1.dev1+g298f9f0e1.d20260707`).
- **Releasing a new version:** `git tag <version>` then `uv build` to produce sdist + wheel.
- **Building:** `uv build` (produces `dist/` with sdist and wheel).
- **Fallback version:** `0.1.0` is used when no git tags exist (configured in `[tool.setuptools_scm]`).

## Conventions

- New modules go in `src/rainbowminer_api_client/`.
- New tests go in `tests/` with `test_*.py` naming.
- Public API exports should be re-exported in `src/rainbowminer_api_client/__init__.py`.
- Use `from __future__ import annotations` only if supporting older Python versions is needed (not required for 3.14+).
- Prefer type annotations on all function signatures.
- **Sync/async parity:** Every public async method on `RainbowMinerClient` must have a corresponding sync method on `SyncRainbowMinerClient` with the same name and signature (minus `async`/`await`). Parity is enforced by `tests/test_sync_client.py`. When adding a new async method to `RainbowMinerClient`, add the sync counterpart to `SyncRainbowMinerClient` in the same change.
