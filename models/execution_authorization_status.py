from enum import Enum


class ExecutionAuthorizationStatus(str, Enum):
    """
    Describes the authorization state of an execution plan.

    Authorization determines admissibility only.

    It performs no execution.
    """

    AUTHORIZED = "AUTHORIZED"

    NOT_AUTHORIZED = "NOT_AUTHORIZED"

    PENDING = "PENDING"

    UNKNOWN = "UNKNOWN"