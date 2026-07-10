from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Relationship:
    """
    Represents an explicit relationship between two platform objects.

    Relationships describe connections.

    They do not imply causation, correctness, or authority.
    """

    relationship_id: str

    source_id: str
    target_id: str

    relationship_type: str

    description: str = ""

    status: str = "Candidate"

    created: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    confidence: Optional[str] = None

    notes: Optional[str] = None