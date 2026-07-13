from enum import Enum


class ExecutionRelianceDecisionType(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    HOLD = "HOLD"
    CONDITIONAL_ACCEPT = "CONDITIONAL_ACCEPT"