from enum import Enum


class ExecutionCertificationStatus(str, Enum):
    CERTIFIED = "CERTIFIED"
    NOT_CERTIFIED = "NOT_CERTIFIED"
    INDETERMINATE = "INDETERMINATE"