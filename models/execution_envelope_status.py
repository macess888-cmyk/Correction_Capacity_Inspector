from enum import Enum


class ExecutionEnvelopeStatus(str, Enum):
    """
    Describes the structural state of an execution envelope.

    An execution envelope packages governance outputs.

    It performs no execution.
    """

    COMPLETE = "COMPLETE"

    INCOMPLETE = "INCOMPLETE"

    INVALID = "INVALID"

    UNKNOWN = "UNKNOWN"