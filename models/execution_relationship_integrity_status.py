from enum import Enum


class ExecutionRelationshipIntegrityStatus(str, Enum):
    """
    Describes whether the execution governance chain
    remains valid as a connected relationship.

    Relationship integrity performs no execution.
    """

    VALID = "VALID"
    DRIFTED = "DRIFTED"
    BROKEN = "BROKEN"
    INCOMPLETE = "INCOMPLETE"
    UNKNOWN = "UNKNOWN"