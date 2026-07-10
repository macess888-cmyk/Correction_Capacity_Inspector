from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class InspectionContext:
    """
    Shared execution context for an inspection runtime.

    Provides execution metadata only.

    Contains no inspection conclusions,
    decision logic, or authority.
    """

    inspection_id: str
    subject: str
    scope: str
    objective: str
    operator: str

    status: str = "CREATED"

    started: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    completed: datetime | None = None

    notes: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)