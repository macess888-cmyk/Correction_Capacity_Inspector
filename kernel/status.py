from enum import Enum


class ResearchStatus(str, Enum):
    OBSERVED = "Observed"
    RECORDED = "Recorded"
    CANDIDATE = "Candidate"
    HYPOTHESIS = "Hypothesis"
    SUPPORTED = "Supported"
    COMPETING = "Competing"
    NEEDS_INVESTIGATION = "Needs Investigation"
    COUNTEREXAMPLE_FOUND = "Counterexample Found"
    DEPRECATED = "Deprecated"
    REJECTED = "Rejected"
    FROZEN = "Frozen"


VALID_RESEARCH_STATUSES = {status.value for status in ResearchStatus}


def is_valid_status(status: str) -> bool:
    return status in VALID_RESEARCH_STATUSES