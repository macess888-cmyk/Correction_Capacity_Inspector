import pytest

from models.inspection_context import InspectionContext
from registries.inspection_context_registry import (
    InspectionContextRegistry,
)


def make_context(
    inspection_id: str = "inspection-001",
) -> InspectionContext:
    return InspectionContext(
        inspection_id=inspection_id,
        subject="Example subject",
        scope="Example scope",
        objective="Example objective",
        operator="Example operator",
    )


def test_registry_add_get_exists_and_count() -> None:
    registry = InspectionContextRegistry()
    context = make_context()

    registry.add(context)

    assert registry.get("inspection-001") is context
    assert registry.exists("inspection-001") is True
    assert registry.count() == 1


def test_registry_list_returns_contexts() -> None:
    registry = InspectionContextRegistry()

    first = make_context("inspection-001")
    second = make_context("inspection-002")

    registry.add(first)
    registry.add(second)

    assert registry.list() == [first, second]


def test_registry_update_replaces_existing_context() -> None:
    registry = InspectionContextRegistry()
    context = make_context()

    registry.add(context)

    updated = InspectionContext(
        inspection_id="inspection-001",
        subject="Updated subject",
        scope="Updated scope",
        objective="Updated objective",
        operator="Updated operator",
        status="ACTIVE",
    )

    registry.update(updated)

    assert registry.get("inspection-001") is updated
    assert registry.get("inspection-001").status == "ACTIVE"


def test_registry_remove_returns_context() -> None:
    registry = InspectionContextRegistry()
    context = make_context()

    registry.add(context)

    removed = registry.remove("inspection-001")

    assert removed is context
    assert registry.exists("inspection-001") is False
    assert registry.count() == 0


def test_registry_rejects_duplicate_identifier() -> None:
    registry = InspectionContextRegistry()

    registry.add(make_context("inspection-001"))

    with pytest.raises(ValueError):
        registry.add(make_context("inspection-001"))


def test_registry_missing_get_raises_key_error() -> None:
    registry = InspectionContextRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_missing_update_raises_key_error() -> None:
    registry = InspectionContextRegistry()

    with pytest.raises(KeyError):
        registry.update(make_context("missing"))


def test_registry_missing_remove_raises_key_error() -> None:
    registry = InspectionContextRegistry()

    with pytest.raises(KeyError):
        registry.remove("missing")