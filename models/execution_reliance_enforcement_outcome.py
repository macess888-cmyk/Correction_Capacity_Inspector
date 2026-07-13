from enum import Enum


class ExecutionRelianceEnforcementOutcome(str, Enum):
    PERMITTED = "PERMITTED"
    BLOCKED = "BLOCKED"
    HELD = "HELD"
    CONDITIONALLY_PERMITTED = "CONDITIONALLY_PERMITTED"