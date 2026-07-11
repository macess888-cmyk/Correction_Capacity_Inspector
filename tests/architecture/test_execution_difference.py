from dataclasses import FrozenInstanceError

import pytest

from models.execution_difference import ExecutionDifference
from models.execution_difference_type import ExecutionDifferenceType


def test_execution_difference_model():

    difference = ExecutionDifference(
        field_name="state",
        runtime_value="RUNNING",
        reconstructed_value="STOPPED",
        difference_type=ExecutionDifferenceType.VALUE_DIFFERENCE,
    )

    assert difference.field_name == "state"
    assert difference.runtime_value == "RUNNING"
    assert difference.reconstructed_value == "STOPPED"
    assert (
        difference.difference_type
        == ExecutionDifferenceType.VALUE_DIFFERENCE
    )


def test_execution_difference_is_frozen():

    difference = ExecutionDifference(
        field_name="state",
        runtime_value="RUNNING",
        reconstructed_value="STOPPED",
        difference_type=ExecutionDifferenceType.VALUE_DIFFERENCE,
    )

    with pytest.raises(FrozenInstanceError):
        difference.field_name = "changed"