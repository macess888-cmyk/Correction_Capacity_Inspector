from enum import Enum


class ExecutionReceiptStatus(str, Enum):
    """
    Describes the recorded outcome of an execution attempt.

    A receipt is immutable evidence.
    """

    COMPLETED = "COMPLETED"
    REFUSED = "REFUSED"
    FAILED = "FAILED"
    NOT_ATTEMPTED = "NOT_ATTEMPTED"
    UNKNOWN = "UNKNOWN"