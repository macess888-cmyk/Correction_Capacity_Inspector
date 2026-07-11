from enum import Enum


class ExecutionRefusalStatus(str, Enum):
    """
    Describes whether an execution refusal has been established.
    """

    REFUSED = "REFUSED"
    NOT_REFUSED = "NOT_REFUSED"
    INDETERMINATE = "INDETERMINATE"
    UNKNOWN = "UNKNOWN"