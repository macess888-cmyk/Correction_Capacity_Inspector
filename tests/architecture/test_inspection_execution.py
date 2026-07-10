from datetime import UTC, datetime

from models.inspection_execution import InspectionExecution
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


def test_inspection_execution_defaults() -> None:
    execution = InspectionExecution(
        execution_id="execution-001",
        inspection_id="inspection-001",
    )

    assert execution.execution_id == "execution-001"
    assert execution.inspection_id == "inspection-001"
    assert execution.status == InspectionExecutionStatus.CREATED
    assert execution.current_stage == "NOT_STARTED"
    assert execution.attempt == 1
    assert isinstance(execution.started, datetime)
    assert execution.started.tzinfo == UTC
    assert execution.completed is None
    assert execution.failure_reason == ""
    assert execution.metadata == {}


def test_inspection_execution_accepts_explicit_values() -> None:
    execution = InspectionExecution(
        execution_id="execution-002",
        inspection_id="inspection-001",
        status=InspectionExecutionStatus.RUNNING,
        current_stage="REPORT_CREATION",
        attempt=2,
        failure_reason="",
        metadata={
            "source": "architecture-test",
        },
    )

    assert execution.status == InspectionExecutionStatus.RUNNING
    assert execution.current_stage == "REPORT_CREATION"
    assert execution.attempt == 2
    assert execution.metadata == {
        "source": "architecture-test",
    }


def test_inspection_execution_metadata_is_independent() -> None:
    first = InspectionExecution(
        execution_id="execution-001",
        inspection_id="inspection-001",
    )
    second = InspectionExecution(
        execution_id="execution-002",
        inspection_id="inspection-002",
    )

    first.metadata["source"] = "first"

    assert second.metadata == {}