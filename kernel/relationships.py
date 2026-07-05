from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from kernel.status import ResearchStatus


@dataclass
class Relationship:
    id: str
    source: str
    destination: str
    relationship_type: str
    description: str = ""
    status: str = ResearchStatus.CANDIDATE.value
    created: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    modified: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    references: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)