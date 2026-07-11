from enum import Enum


class ExecutionRecommendationStatus(str, Enum):
    """
    Describes whether a recommendation can be produced
    from the available inspection information.
    """

    AVAILABLE = "AVAILABLE"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"
    UNKNOWN = "UNKNOWN"