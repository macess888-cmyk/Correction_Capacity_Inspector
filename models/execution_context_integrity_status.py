from enum import Enum


class ExecutionContextIntegrityStatus(str, Enum):
    """
    Describes whether the execution context still corresponds
    to the context under which the governance chain was formed.

    Context integrity performs no execution.
    """

    CORRESPONDING = "CORRESPONDING"
    DRIFTED = "DRIFTED"
    BROKEN = "BROKEN"
    INCOMPLETE = "INCOMPLETE"
    UNKNOWN = "UNKNOWN"