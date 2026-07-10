from datetime import datetime

from models.inspection_context import InspectionContext


def test_inspection_context_defaults() -> None:
    context = InspectionContext(
        inspection_id="inspection-001",
        subject="Example subject",
        scope="Example scope",
        objective="Example objective",
        operator="Example operator",
    )

    assert context.inspection_id == "inspection-001"
    assert context.status == "CREATED"
    assert isinstance(context.started, datetime)
    assert context.completed is None
    assert context.notes == ""
    assert context.metadata == {}


def test_inspection_context_accepts_optional_values() -> None:
    context = InspectionContext(
        inspection_id="inspection-002",
        subject="Example subject",
        scope="Example scope",
        objective="Example objective",
        operator="Example operator",
        status="ACTIVE",
        notes="Inspection started.",
        metadata={"source": "architecture-test"},
    )

    assert context.status == "ACTIVE"
    assert context.notes == "Inspection started."
    assert context.metadata == {
        "source": "architecture-test",
    }