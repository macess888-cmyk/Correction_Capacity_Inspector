from __future__ import annotations

from dataclasses import dataclass

from models.execution_difference_type import ExecutionDifferenceType


@dataclass(frozen=True)
class ExecutionDifference:
    """
    Describes one observed difference between
    runtime execution and reconstructed execution.
    """

    field_name: str

    runtime_value: object

    reconstructed_value: object

    difference_type: ExecutionDifferenceType