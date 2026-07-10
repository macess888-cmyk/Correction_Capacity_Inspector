from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class Evidence:
    """
    Represents an individual piece of evidence.

    Evidence records observations or supporting artifacts.

    Evidence does not establish proof by itself.
    """

    evidence_id: str

    title: str

    description: str

    source: str

    status: str = "Candidate"

    created: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    notes: List[str] = field(default_factory=list)