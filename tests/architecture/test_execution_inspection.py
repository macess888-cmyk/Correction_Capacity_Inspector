from dataclasses import FrozenInstanceError

import pytest

from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)


def test_execution_inspection_defaults():

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    inspection = ExecutionInspection(
        execution_id="exec-001",
        divergence=divergence,
        status=ExecutionInspectionStatus.CONSISTENT,
    )

    assert inspection.execution_id == "exec-001"

    assert inspection.status == (
        ExecutionInspectionStatus.CONSISTENT
    )

    assert inspection.observations == ()

    assert inspection.requires_attention is False


def test_execution_inspection_is_frozen():

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    inspection = ExecutionInspection(
        execution_id="exec-001",
        divergence=divergence,
        status=ExecutionInspectionStatus.CONSISTENT,
    )

    with pytest.raises(FrozenInstanceError):
        inspection.execution_id = "changed"