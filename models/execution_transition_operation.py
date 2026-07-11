from __future__ import annotations

from enum import StrEnum


class ExecutionTransitionOperation(StrEnum):
    """
    Closed vocabulary of supported execution operations.

    Operations are architectural symbols only.

    They do not mutate state, validate transitions,
    record events, or establish authority.
    """

    INITIALIZE = "INITIALIZE"
    START = "START"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"
    CANCEL = "CANCEL"
    ARCHIVE = "ARCHIVE"