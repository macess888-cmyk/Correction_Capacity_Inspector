from enum import Enum


class ExecutionPlanStatus(str, Enum):
    """
    Describes whether a correction plan can be formed
    from an execution recommendation.

    A plan carries no authority and performs no execution.
    """

    AVAILABLE = "AVAILABLE"
    INCOMPLETE = "INCOMPLETE"
    NOT_PLANNABLE = "NOT_PLANNABLE"
    UNKNOWN = "UNKNOWN"