"""Replay recorded live API fixtures through the Pydantic models.

This test loads each JSON file from ``tests/fixtures/real/`` and parses it
through the model declared in :mod:`tests.fixture_registry`.  It verifies
that the models match the **real** RainbowMiner API contract — not just the
hand-written canned data in ``conftest.py``.

The test is skipped entirely when no fixtures directory exists (e.g. on a
fresh clone or in CI without recorded fixtures).  To populate the fixtures,
run ``uv run python -m tests.record_fixtures --host <rig-ip>`` against a
live RainbowMiner instance.  The resulting JSON files are git-ignored (they
may contain wallet addresses, IP addresses, and other private data), so the
replay test only runs locally — CI skips it automatically.

Only read-only endpoints are recorded/replayed — no fixture exercises a
server-mutating endpoint.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from tests.fixture_registry import READ_ONLY_ENDPOINTS, EndpointSpec, ParseKind

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "real"


def _available_specs() -> list[EndpointSpec]:
    """Return the subset of endpoint specs whose fixture file exists."""
    if not FIXTURES_DIR.is_dir():
        return []
    return [s for s in READ_ONLY_ENDPOINTS if (FIXTURES_DIR / f"{s.name}.json").is_file()]


def _load(name: str) -> Any:
    """Load a fixture file as decoded JSON."""
    return json.loads((FIXTURES_DIR / f"{name}.json").read_text())


def _parse(spec: EndpointSpec, data: Any) -> Any:
    """Parse ``data`` according to ``spec.kind`` and return the model object(s).

    Args:
        spec: The endpoint specification (path, kind, model).
        data: The raw decoded JSON payload.

    Returns:
        The parsed model object, list of model objects, or raw data.

    Raises:
        ValueError: If the spec has no model for a kind that requires one.
    """
    match spec.kind:
        case ParseKind.SINGLE:
            if spec.model is None:
                raise ValueError(f"Spec {spec.name} is SINGLE but has no model")
            return spec.model.model_validate(data if data is not None else {})
        case ParseKind.LIST:
            if spec.model is None:
                raise ValueError(f"Spec {spec.name} is LIST but has no model")
            items = data if isinstance(data, list) else ([] if data is None else [data])
            return [spec.model.model_validate(item) for item in items]
        case ParseKind.STRING_LIST:
            items = data if isinstance(data, list) else ([] if data is None else [data])
            return [str(item) for item in items]
        case ParseKind.DICT:
            if spec.model is None:
                raise ValueError(f"Spec {spec.name} is DICT but has no model")
            return spec.model.model_validate(data if data is not None else {})
        case ParseKind.RAW:
            return data


# --- test collection ------------------------------------------------------- #

SPECS = _available_specs()

# Sentinel used so the parametrized class always collects at least one item,
# even when no fixture files are present.  Without this, an empty parametrize
# list produces zero items and the test node IDs don't exist — making it
# impossible to target them explicitly (pytest reports "not found").
_NO_FIXTURES = object()

_SKIP_REASON = "no recorded fixtures in tests/fixtures/real — run `uv run python -m tests.record_fixtures`"


def _params() -> list[Any]:
    """Return the list of parametrize values, or a single skipped sentinel."""
    if SPECS:
        return list(SPECS)
    return [pytest.param(_NO_FIXTURES, marks=pytest.mark.skip(reason=_SKIP_REASON), id="no-fixtures")]


def _id(spec: Any) -> str:
    """Return a pytest id for a parametrized spec."""
    if spec is _NO_FIXTURES:
        return "no-fixtures"
    return spec.name


@pytest.mark.parametrize("spec", _params(), ids=_id)
class TestReplayFixtures:
    """Replay each recorded fixture through its declared model."""

    def test_fixture_parses_without_error(self, spec: EndpointSpec) -> None:
        """The recorded JSON must parse through the model without ValidationError."""
        data = _load(spec.name)
        try:
            result = _parse(spec, data)
        except ValidationError as exc:
            pytest.fail(f"{spec.name} ({spec.path}) failed to parse: {exc}")
        # Sanity: for list kinds, result should be a list.
        if spec.kind in (ParseKind.LIST, ParseKind.STRING_LIST):
            assert isinstance(result, list), f"{spec.name}: expected list, got {type(result)}"

    def test_fixture_model_types(self, spec: EndpointSpec) -> None:
        """Parsed objects should be instances of the declared model (where applicable)."""
        data = _load(spec.name)
        result = _parse(spec, data)
        match spec.kind:
            case ParseKind.SINGLE:
                assert isinstance(result, BaseModel), f"{spec.name}: expected BaseModel, got {type(result)}"
            case ParseKind.LIST:
                if result:  # non-empty
                    assert all(isinstance(item, BaseModel) for item in result), (
                        f"{spec.name}: expected all items to be BaseModel"
                    )
            case ParseKind.DICT:
                # Root models expose their dict via .root; plain dicts pass through.
                root = getattr(result, "root", result)
                assert isinstance(root, dict), f"{spec.name}: expected dict, got {type(root)}"
            case ParseKind.STRING_LIST:
                assert all(isinstance(item, str) for item in result), f"{spec.name}: expected all str"
            case ParseKind.RAW:
                # No type assertion — just that it was JSON-decodable.
                pass
