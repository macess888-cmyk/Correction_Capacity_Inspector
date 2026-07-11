from enum import Enum


class ExecutionTemporalIntegrityStatus(str, Enum):
    """
    Describes whether an execution governance chain remains
    temporally admissible.

    Temporal integrity performs no execution.
    """

    CURRENT = "CURRENT"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"
    UNKNOWN = "UNKNOWN"