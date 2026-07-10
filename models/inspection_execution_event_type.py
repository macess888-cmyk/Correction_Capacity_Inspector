from __future__ import annotations

from enum import StrEnum


class InspectionExecutionEventType(StrEnum):
    """
    Closed vocabulary for recorded inspection execution events.

    Event types describe verified runtime behavior only.
    They do not establish truth, validity, or authority.
    """

    EXECUTION_CREATED = "EXECUTION_CREATED"
    EXECUTION_INITIALIZED = "EXECUTION_INITIALIZED"
    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_PAUSED = "EXECUTION_PAUSED"
    EXECUTION_RESUMED = "EXECUTION_RESUMED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"
    EXECUTION_ARCHIVED = "EXECUTION_ARCHIVED"