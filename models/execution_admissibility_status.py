from enum import Enum


class ExecutionAdmissibilityStatus(str, Enum):
    """
    Describes whether execution is constitutionally admissible.

    Admissibility grants no execution and performs no mutation.
    """

    ADMISSIBLE = "ADMISSIBLE"
    NOT_ADMISSIBLE = "NOT_ADMISSIBLE"
    INDETERMINATE = "INDETERMINATE"
    UNKNOWN = "UNKNOWN"