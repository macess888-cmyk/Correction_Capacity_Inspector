from __future__ import annotations

from enum import StrEnum


class InspectionExecutionStatus(StrEnum):
    """
    Allowed lifecycle states for one inspection execution.

    These values describe runtime behavior only.
    They do not express inspection validity, truth, or authority.
    """

    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"