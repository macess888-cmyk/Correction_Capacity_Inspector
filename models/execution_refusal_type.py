from enum import Enum


class ExecutionRefusalType(str, Enum):
    """
    Describes why an execution request must not proceed.

    Refusal performs no execution.
    """

    NOT_AUTHORIZED = "NOT_AUTHORIZED"
    NOT_READY = "NOT_READY"
    ENVELOPE_INCOMPLETE = "ENVELOPE_INCOMPLETE"
    ENVELOPE_INVALID = "ENVELOPE_INVALID"
    RELATIONSHIP_BROKEN = "RELATIONSHIP_BROKEN"
    TEMPORALLY_EXPIRED = "TEMPORALLY_EXPIRED"
    TEMPORALLY_UNKNOWN = "TEMPORALLY_UNKNOWN"
    UNKNOWN = "UNKNOWN"