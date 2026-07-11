from enum import Enum


class ExecutionRecommendationType(str, Enum):
    """
    Describes a candidate response derived from execution inspection.

    A recommendation carries no authority and performs no execution.
    """

    NO_ACTION = "NO_ACTION"
    CONTINUE_OBSERVATION = "CONTINUE_OBSERVATION"
    VERIFY_RUNTIME = "VERIFY_RUNTIME"
    REQUEST_EVIDENCE = "REQUEST_EVIDENCE"
    RECONSTRUCT = "RECONSTRUCT"
    ESCALATE = "ESCALATE"
    UNKNOWN = "UNKNOWN"