# AGENTS.md

Codara (`codara-mcp`) is a Python 3.12+ stdio MCP server for semantic code search, index maintenance, and read-only codebase retrieval. Source lives in `src/codara_mcp/`; tests in `tests/`. Read [docs/diagrams/architecture.html](docs/diagrams/architecture.html) and [docs/diagrams/data-flow.html](docs/diagrams/data-flow.html) before changing how components connect or how data moves.

## Invariants

- **Single writer.** Only `codara index` writes `<repo>/.codara/index-v2.sqlite`. The `index_update` tool spawns `python -m codara_mcp.cli index --json` as a subprocess under the `index.lock` flock. `semantic_search`, `index_status`, and `codebase_retrieval` open the index read-only and never build it.
- **Read-only retrieval.** `codebase_retrieval` runs the agent CLI with the per-driver flags in `_PRESETS` (`retrieval.py`), snapshots git state before and after, and raises `REPO_MODIFIED` on any change. A new driver gets a verified read-only preset with the CLI version cited in a comment.
- **Error codes.** Tool errors map to the fixed codes in `_error_code` (`server.py`). A new failure reuses an existing code; a new code also goes into the README error list.
- **Config precedence.** Non-empty `CODARA_*` env values, then `~/.codara/config.toml`, then defaults. A new setting adds one `_SCHEMA` row in `config.py` and one README configuration row.
- **Telemetry never raises.** `telemetry.py` uses the standard library only and swallows its own failures.
- **Index format.** A change to the SQLite schema or chunk boundaries bumps `SCHEMA_VERSION` (`store.py`) or `CHUNKER_VERSION` (`chunking.py`) so existing indexes rebuild.

## Conventions

- Tests use `unittest.TestCase` classes run by pytest. Use `tests/fake_embedder.py` for embeddings and `tests/fake_pi.py` for agent runs; tests never call Voyage AI or a real agent CLI.
- A version bump edits `pyproject.toml` and every manifest listed in `VERSION_FILES` (`scripts/check_versions.py`), then refreshes `uv.lock`.
- User-visible changes get an `[Unreleased]` entry in `CHANGELOG.md` (Keep a Changelog).
- Diagrams in `docs/diagrams/` are generated with the `diagram-design` skill. Edit the `.html` source, then re-export the matching `.svg` that README.md embeds.

## Done

Work is done when every command below passes. These mirror `.github/workflows/ci.yml`.

```bash
uv run --frozen pytest tests -q
uv run --frozen ruff check src tests scripts
uv run --frozen ty check src
uv run --frozen python scripts/check_versions.py
uv lock --check
```
