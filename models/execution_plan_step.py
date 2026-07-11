from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionPlanStep:
    """
    Represents one ordered, advisory step in an execution plan.

    A plan step does not perform execution.
    """

    order: int
    description: str
    required: bool = True