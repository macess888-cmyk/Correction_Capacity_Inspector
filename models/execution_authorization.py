from __future__ import annotations

from dataclasses import dataclass

from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_plan import ExecutionPlan


@dataclass(frozen=True)
class ExecutionAuthorization:
    """
    Represents the authorization state of an execution plan.

    Authorization determines admissibility.

    It grants no execution and performs no mutation.
    """

    execution_id: str

    plan: ExecutionPlan

    status: ExecutionAuthorizationStatus

    reason: str