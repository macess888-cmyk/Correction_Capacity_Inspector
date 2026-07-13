from enum import Enum


class ExecutionRevocationStatus(str, Enum):
    REVOKED = "REVOKED"
    SUSPENDED = "SUSPENDED"
    WITHDRAWN = "WITHDRAWN"