from enum import Enum


class ExecutionInspectionStatus(str, Enum):
    """
    Describes the interpreted inspection result
    for an execution divergence.

    Inspection is observational only.
    """

    CONSISTENT = "CONSISTENT"

    INCONSISTENT = "INCONSISTENT"

    PARTIAL = "PARTIAL"

    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

    UNKNOWN = "UNKNOWN"