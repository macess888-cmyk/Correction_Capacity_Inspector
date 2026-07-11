from __future__ import annotations

from enum import StrEnum


class ExecutionEvidenceCompleteness(StrEnum):
    """
    Closed vocabulary for reconstruction evidence completeness.

    Completeness describes whether enough evidence was available,
    independently of whether that evidence was internally consistent.
    """

    UNKNOWN = "UNKNOWN"
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"