from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.execution_admissibility import ExecutionAdmissibility
from models.execution_receipt_status import ExecutionReceiptStatus


@dataclass(frozen=True)
class ExecutionReceipt:
    """
    Represents immutable evidence of an execution attempt or non-attempt.

    A receipt records what occurred.

    It never modifies execution or governance state.
    """

    execution_id: str

    admissibility: ExecutionAdmissibility

    status: ExecutionReceiptStatus

    recorded_at: datetime

    operation: str

    outcome: str

    observations: tuple[str, ...] = field(default_factory=tuple)