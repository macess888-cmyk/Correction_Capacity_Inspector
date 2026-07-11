from enum import Enum


class ExecutionDivergenceStatus(str, Enum):

    IDENTICAL = "IDENTICAL"

    DIVERGED = "DIVERGED"

    PARTIAL = "PARTIAL"

    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

    UNKNOWN = "UNKNOWN"