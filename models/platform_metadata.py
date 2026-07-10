from dataclasses import dataclass, field
default_factory=lambda: datetime.utcnow().isoformat()
from typing import Optional


@dataclass
class PlatformMetadata:
    """
    Shared metadata for platform objects.

    This object provides common lifecycle information while
    preserving object independence through composition.
    """

    object_id: str
    name: str

    description: str = ""

    status: str = "Candidate"

    created: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    updated: Optional[str] = None