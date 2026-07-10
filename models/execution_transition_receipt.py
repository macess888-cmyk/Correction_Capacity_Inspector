from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)


@dataclass(frozen=True, slots=True)
class ExecutionTransitionReceipt:
    """
    Immutable outcome record for one attempted transition.

    A receipt describes whether execution state and event history
    remained consistent across the transition boundary.

    It does not establish inspection truth or authority.
    """

    receipt_id: str
    transition_id: str
    execution_id: str

    state_updated: bool
    event_recorded: bool

    consistency_status: ExecutionConsistencyStatus

    failure_stage: str = ""
    failure_reason: str = ""

    completed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )