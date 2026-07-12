from datetime import datetime, timezone

from models.execution_admissibility import ExecutionAdmissibility
from models.execution_admissibility_status import (
    ExecutionAdmissibilityStatus,
)
from models.execution_receipt import ExecutionReceipt
from models.execution_receipt_status import ExecutionReceiptStatus


class ExecutionReceiptService:
    """
    Records immutable evidence for execution attempts and non-attempts.

    Receipt creation performs no execution and mutates no governance state.
    """

    def record_non_attempt(
        self,
        admissibility: ExecutionAdmissibility,
        *,
        operation: str,
    ) -> ExecutionReceipt:

        if (
            admissibility.status
            == ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
        ):
            observations = (
                "Execution was not admissible.",
            )

        elif (
            admissibility.status
            == ExecutionAdmissibilityStatus.INDETERMINATE
        ):
            observations = (
                "Execution admissibility was indeterminate.",
            )

        elif (
            admissibility.status
            == ExecutionAdmissibilityStatus.UNKNOWN
        ):
            observations = (
                "Execution admissibility was unknown.",
            )

        else:
            observations = (
                "Admissible execution was not attempted.",
            )

        return ExecutionReceipt(
            execution_id=admissibility.execution_id,
            admissibility=admissibility,
            status=ExecutionReceiptStatus.NOT_ATTEMPTED,
            recorded_at=datetime.now(timezone.utc),
            operation=operation,
            outcome="Execution was not attempted.",
            observations=observations,
        )

    def record_completion(
        self,
        admissibility: ExecutionAdmissibility,
        *,
        operation: str,
        outcome: str,
    ) -> ExecutionReceipt:

        return ExecutionReceipt(
            execution_id=admissibility.execution_id,
            admissibility=admissibility,
            status=ExecutionReceiptStatus.COMPLETED,
            recorded_at=datetime.now(timezone.utc),
            operation=operation,
            outcome=outcome,
            observations=(),
        )

    def record_failure(
        self,
        admissibility: ExecutionAdmissibility,
        *,
        operation: str,
        outcome: str,
        observations: tuple[str, ...] = (),
    ) -> ExecutionReceipt:

        return ExecutionReceipt(
            execution_id=admissibility.execution_id,
            admissibility=admissibility,
            status=ExecutionReceiptStatus.FAILED,
            recorded_at=datetime.now(timezone.utc),
            operation=operation,
            outcome=outcome,
            observations=observations,
        )

    def record_refusal(
        self,
        admissibility: ExecutionAdmissibility,
        *,
        operation: str,
        outcome: str,
    ) -> ExecutionReceipt:

        return ExecutionReceipt(
            execution_id=admissibility.execution_id,
            admissibility=admissibility,
            status=ExecutionReceiptStatus.REFUSED,
            recorded_at=datetime.now(timezone.utc),
            operation=operation,
            outcome=outcome,
            observations=(
                "Execution refusal was preserved as evidence.",
            ),
        )