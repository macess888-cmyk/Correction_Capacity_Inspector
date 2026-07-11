from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)


class ExecutionInspectionService:
    """
    Interprets execution divergence without mutating
    execution, reconstruction, divergence, or evidence.

    Inspection is descriptive only.
    """

    def inspect(
        self,
        divergence: ExecutionDivergence,
    ) -> ExecutionInspection:

        if divergence.status == ExecutionDivergenceStatus.IDENTICAL:
            return ExecutionInspection(
                execution_id=divergence.execution_id,
                divergence=divergence,
                status=ExecutionInspectionStatus.CONSISTENT,
                observations=(),
                requires_attention=False,
            )

        if divergence.status == ExecutionDivergenceStatus.DIVERGED:
            return ExecutionInspection(
                execution_id=divergence.execution_id,
                divergence=divergence,
                status=ExecutionInspectionStatus.INCONSISTENT,
                observations=(
                    "Runtime state differs from reconstructed execution state.",
                ),
                requires_attention=True,
            )

        if divergence.status == ExecutionDivergenceStatus.PARTIAL:
            return ExecutionInspection(
                execution_id=divergence.execution_id,
                divergence=divergence,
                status=ExecutionInspectionStatus.PARTIAL,
                observations=(
                    "Runtime execution state is unavailable.",
                ),
                requires_attention=True,
            )

        if (
            divergence.status
            == ExecutionDivergenceStatus.INSUFFICIENT_EVIDENCE
        ):
            return ExecutionInspection(
                execution_id=divergence.execution_id,
                divergence=divergence,
                status=ExecutionInspectionStatus.INSUFFICIENT_EVIDENCE,
                observations=(
                    "Reconstructed execution evidence is insufficient.",
                ),
                requires_attention=True,
            )

        return ExecutionInspection(
            execution_id=divergence.execution_id,
            divergence=divergence,
            status=ExecutionInspectionStatus.UNKNOWN,
            observations=(
                "Execution divergence could not be fully interpreted.",
            ),
            requires_attention=True,
        )