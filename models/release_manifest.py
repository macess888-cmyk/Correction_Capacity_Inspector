from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class ReleaseManifest:
    """
    Represents a frozen snapshot of a platform release.
    """

    version: str
    release_name: str

    created: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    architecture_status: str = ""
    platform_status: str = ""
    research_status: str = ""

    completed_capabilities: List[str] = field(default_factory=list)
    outstanding_work: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)