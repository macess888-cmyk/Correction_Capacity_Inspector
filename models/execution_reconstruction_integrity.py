from __future__ import annotations

from enum import StrEnum


class ExecutionReconstructionIntegrity(StrEnum):
    """
    Closed vocabulary for reconstruction integrity.

    Integrity describes internal agreement among the
    processed evidence artifacts.
    """

    UNKNOWN = "UNKNOWN"
    CONSISTENT = "CONSISTENT"
    INCONSISTENT = "INCONSISTENT"