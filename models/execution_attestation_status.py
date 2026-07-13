from enum import Enum


class ExecutionAttestationStatus(str, Enum):
    AFFIRMED = "AFFIRMED"
    DECLINED = "DECLINED"
    WITHHELD = "WITHHELD"