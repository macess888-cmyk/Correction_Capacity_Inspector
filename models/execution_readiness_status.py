from enum import Enum


class ExecutionReadinessStatus(str, Enum):
    """
    Describes the readiness state of an authorized execution plan.

    Readiness determines preparedness only.

    It performs no execution.
    """

    READY = "READY"

    NOT_READY = "NOT_READY"

    BLOCKED = "BLOCKED"

    UNKNOWN = "UNKNOWN"