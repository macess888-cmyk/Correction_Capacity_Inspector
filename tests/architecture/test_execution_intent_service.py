from datetime import datetime, timezone

import pytest

from models.execution_intent import ExecutionIntent
from services.execution_intent_service import ExecutionIntentService


def test_service_creates_execution_intent():
    service = ExecutionIntentService()

    intent = service.create_intent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters={
            "mode": "bounded",
        },
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )

    assert isinstance(intent, ExecutionIntent)
    assert intent.execution_intent_id == "INTENT-001"
    assert intent.action == "reconcile"
    assert intent.target == "system-state"


def test_service_preserves_traceability_fields():
    service = ExecutionIntentService()

    created_at = datetime.now(timezone.utc)

    intent = service.create_intent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters={},
        requested_by="AUTHORITY-001",
        created_at=created_at,
        admissibility_id="ADMISSIBILITY-001",
    )

    assert intent.requested_by == "AUTHORITY-001"
    assert intent.created_at == created_at
    assert intent.admissibility_id == "ADMISSIBILITY-001"


def test_service_does_not_add_execution_state():
    service = ExecutionIntentService()

    intent = service.create_intent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters={},
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )

    assert not hasattr(intent, "status")
    assert not hasattr(intent, "result")
    assert not hasattr(intent, "executed_at")
    assert not hasattr(intent, "receipt_id")


@pytest.mark.parametrize(
    "field_name, invalid_value",
    [
        ("execution_intent_id", ""),
        ("action", ""),
        ("target", ""),
        ("requested_by", ""),
        ("admissibility_id", ""),
    ],
)
def test_service_preserves_model_validation(
    field_name,
    invalid_value,
):
    service = ExecutionIntentService()

    values = {
        "execution_intent_id": "INTENT-001",
        "action": "reconcile",
        "target": "system-state",
        "parameters": {},
        "requested_by": "AUTHORITY-001",
        "created_at": datetime.now(timezone.utc),
        "admissibility_id": "ADMISSIBILITY-001",
    }

    values[field_name] = invalid_value

    with pytest.raises(ValueError):
        service.create_intent(**values)