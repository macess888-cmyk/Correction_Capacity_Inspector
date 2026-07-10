import pytest

from models.inspection_execution import InspectionExecution
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)


def make_execution(
    execution_id: str = "execution-001",
) -> InspectionExecution:
    return InspectionExecution(
        execution_id=execution_id,
        inspection_id="inspection-001",
    )


def test_registry_add_get_exists_and_count() -> None:
    registry = InspectionExecutionRegistry()
    execution = make_execution()

    registry.add(execution)

    assert registry.get("execution-001") is execution
    assert registry.exists("execution-001") is True
    assert registry.count() == 1


def test_registry_list_returns_executions() -> None:
    registry = InspectionExecutionRegistry()

    first = make_execution("execution-001")
    second = make_execution("execution-002")

    registry.add(first)
    registry.add(second)

    assert registry.list() == [first, second]


def test_registry_update_replaces_existing_execution() -> None:
    registry = InspectionExecutionRegistry()
    execution = make_execution()

    registry.add(execution)

    updated = InspectionExecution(
        execution_id="execution-001",
        inspection_id="inspection-001",
        current_stage="UPDATED",
    )

    registry.update(updated)

    assert registry.get("execution-001") is updated
    assert (
        registry.get("execution-001").current_stage
        == "UPDATED"
    )


def test_registry_remove_returns_execution() -> None:
    registry = InspectionExecutionRegistry()
    execution = make_execution()

    registry.add(execution)

    removed = registry.remove("execution-001")

    assert removed is execution
    assert registry.exists("execution-001") is False
    assert registry.count() == 0


def test_registry_rejects_duplicate_identifier() -> None:
    registry = InspectionExecutionRegistry()

    registry.add(make_execution("execution-001"))

    with pytest.raises(ValueError):
        registry.add(make_execution("execution-001"))


def test_registry_missing_get_raises_key_error() -> None:
    registry = InspectionExecutionRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_missing_update_raises_key_error() -> None:
    registry = InspectionExecutionRegistry()

    with pytest.raises(KeyError):
        registry.update(make_execution("missing"))


def test_registry_missing_remove_raises_key_error() -> None:
    registry = InspectionExecutionRegistry()

    with pytest.raises(KeyError):
        registry.remove("missing")