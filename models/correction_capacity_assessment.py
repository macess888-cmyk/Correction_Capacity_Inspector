from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class CorrectionCapacityAssessment:
    """
    Represents a descriptive assessment produced during
    an inspection.

    This model records assessment information only.

    It performs no scoring, reasoning,
    decision-making, or execution.
    """

    assessment_id: str

    inspection_id: str

    status: str = "CREATED"

    summary: str = ""

    observations: list[str] = field(default_factory=list)

    limitations: list[str] = field(default_factory=list)

    created: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, Any] = field(default_factory=dict)