from __future__ import annotations

from dataclasses import dataclass

from models.execution_authorization import ExecutionAuthorization
from models.execution_readiness_status import (
    ExecutionReadinessStatus,
)


@dataclass(frozen=True)
class ExecutionReadiness:
    """
    Represents the operational readiness of an authorized execution plan.

    Readiness determines preparedness.

    It grants no execution and performs no mutation.
    """

    execution_id: str

    authorization: ExecutionAuthorization

    status: ExecutionReadinessStatus

    reason: str