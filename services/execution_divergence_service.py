from models.execution_difference import ExecutionDifference
from models.execution_difference_type import ExecutionDifferenceType
from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import ExecutionDivergenceStatus


class ExecutionDivergenceService:
    """
    Compares mutable runtime state with independently reconstructed state.

    This service is observational only.
    It does not mutate execution, reconstruction, or evidence.
    """

    def inspect(
        self,
        execution_id: str,
        runtime_state: object,
        reconstructed_state: object,
    ) -> ExecutionDivergence:

        if runtime_state is None and reconstructed_state is None:
            return ExecutionDivergence(
                execution_id=execution_id,
                runtime_state=runtime_state,
                reconstructed_state=reconstructed_state,
                status=ExecutionDivergenceStatus.UNKNOWN,
                differences=(),
            )

        if runtime_state is None:
            difference = ExecutionDifference(
                field_name="state",
                runtime_value=None,
                reconstructed_value=reconstructed_state,
                difference_type=ExecutionDifferenceType.MISSING_RUNTIME,
            )

            return ExecutionDivergence(
                execution_id=execution_id,
                runtime_state=runtime_state,
                reconstructed_state=reconstructed_state,
                status=ExecutionDivergenceStatus.PARTIAL,
                differences=(difference,),
            )

        if reconstructed_state is None:
            difference = ExecutionDifference(
                field_name="state",
                runtime_value=runtime_state,
                reconstructed_value=None,
                difference_type=(
                    ExecutionDifferenceType.MISSING_RECONSTRUCTION
                ),
            )

            return ExecutionDivergence(
                execution_id=execution_id,
                runtime_state=runtime_state,
                reconstructed_state=reconstructed_state,
                status=(
                    ExecutionDivergenceStatus.INSUFFICIENT_EVIDENCE
                ),
                differences=(difference,),
            )

        if runtime_state == reconstructed_state:
            return ExecutionDivergence(
                execution_id=execution_id,
                runtime_state=runtime_state,
                reconstructed_state=reconstructed_state,
                status=ExecutionDivergenceStatus.IDENTICAL,
                differences=(),
            )

        difference = ExecutionDifference(
            field_name="state",
            runtime_value=runtime_state,
            reconstructed_value=reconstructed_state,
            difference_type=ExecutionDifferenceType.VALUE_DIFFERENCE,
        )

        return ExecutionDivergence(
            execution_id=execution_id,
            runtime_state=runtime_state,
            reconstructed_state=reconstructed_state,
            status=ExecutionDivergenceStatus.DIVERGED,
            differences=(difference,),
        )