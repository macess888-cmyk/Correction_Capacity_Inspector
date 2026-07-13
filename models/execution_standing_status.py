from enum import Enum


class ExecutionStandingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    WITHDRAWN = "WITHDRAWN"
    INDETERMINATE = "INDETERMINATE"