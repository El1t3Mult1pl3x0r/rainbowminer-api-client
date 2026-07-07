# Recorded API fixtures

This directory holds real JSON responses captured from a live RainbowMiner
server.  The replay test suite (`tests/test_replay_fixtures.py`) parses each
file through the corresponding Pydantic model to verify that the models match
the upstream API contract — not just the hand-written canned data in
`conftest.py`.

## Recording fixtures

Run the recorder against a live rig:

```sh
uv run python -m tests.record_fixtures --host 192.168.1.50 --port 4000
```

Optional flags:

| Flag | Purpose |
| ---- | ------- |
| `--username <user> --password <pass>` | HTTP Basic auth credentials |
| `--tls` | Use `https://` |
| `--outdir <path>` | Override output directory |
| `--overwrite` | Overwrite existing fixtures instead of skipping them |

The recorder only fetches **read-only** endpoints (defined in
`tests/fixture_registry.py`).  It never calls any endpoint that mutates
server state (pause, stop, reboot, toggle, save, update, etc.).

## Replaying fixtures

```sh
uv run pytest tests/test_replay_fixtures.py
```

If no fixtures are present, the test is skipped automatically.

## Privacy & version control

The recorded JSON files are **git-ignored** (`tests/fixtures/real/*.json` in
`.gitignore`).  Real responses can contain wallet addresses, IP addresses,
worker names, and other private data from your rig — they must never be
committed.

The replay test is skipped automatically when no fixtures are present, so CI
stays green without them.  To run the replay test locally, record fixtures
against your own rig first.

## When to re-record

Re-record after upgrading RainbowMiner to a new version, or when adding a
new endpoint to the client.  Run the recorder with `--overwrite`, then run
`uv run pytest tests/test_replay_fixtures.py` to confirm the models still
parse the new responses.  If a `ValidationError` appears, the models need
updating to match the upstream API changes.
