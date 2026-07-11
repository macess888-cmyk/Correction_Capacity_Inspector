from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.execution_divergence_status import ExecutionDivergenceStatus
from models.execution_difference import ExecutionDifference


@dataclass(frozen=True)
class ExecutionDivergence:
    """
    Describes the relationship between live execution and
    independently reconstructed execution history.

    This model is observational only.

    It never performs correction.
    """

    execution_id: str

    runtime_state: Any

    reconstructed_state: Any

    status: ExecutionDivergenceStatus

    differences: tuple[ExecutionDifference, ...] = field(default_factory=tuple)