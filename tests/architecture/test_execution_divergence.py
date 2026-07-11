from dataclasses import FrozenInstanceError

import pytest

from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import ExecutionDivergenceStatus


def test_execution_divergence_defaults():

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    assert divergence.execution_id == "exec-001"

    assert divergence.runtime_state == "RUNNING"

    assert divergence.reconstructed_state == "RUNNING"

    assert divergence.status == ExecutionDivergenceStatus.IDENTICAL

    assert divergence.differences == ()


def test_execution_divergence_is_frozen():

    divergence = ExecutionDivergence(
        execution_id="exec",
        runtime_state="A",
        reconstructed_state="A",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    with pytest.raises(FrozenInstanceError):
        divergence.execution_id = "changed"