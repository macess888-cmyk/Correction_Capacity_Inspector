from __future__ import annotations

from enum import StrEnum


class ExecutionConsistencyStatus(StrEnum):
    """
    Closed vocabulary describing the consistency outcome
    of one attempted execution transition.

    These states describe runtime consistency only.
    They do not establish inspection truth or authority.
    """

    PENDING = "PENDING"
    CONSISTENT = "CONSISTENT"
    STATE_NOT_UPDATED = "STATE_NOT_UPDATED"
    EVENT_NOT_RECORDED = "EVENT_NOT_RECORDED"
    COMPENSATED = "COMPENSATED"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"