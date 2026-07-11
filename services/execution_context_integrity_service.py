from collections.abc import Mapping

from models.execution_context_integrity import ExecutionContextIntegrity
from models.execution_context_integrity_status import (
    ExecutionContextIntegrityStatus,
)
from models.execution_envelope import ExecutionEnvelope


class ExecutionContextIntegrityService:
    """
    Inspects whether observed execution context still corresponds
    to the context under which the governance chain was formed.

    Context inspection is observational only.
    It grants no authority and performs no execution.
    """

    def inspect(
        self,
        envelope: ExecutionEnvelope,
        *,
        expected_context: Mapping[str, object],
        observed_context: Mapping[str, object],
    ) -> ExecutionContextIntegrity:

        expected = dict(expected_context)
        observed = dict(observed_context)

        if not expected and not observed:
            return ExecutionContextIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                expected_context=expected,
                observed_context=observed,
                status=ExecutionContextIntegrityStatus.UNKNOWN,
                observations=(
                    "Execution context could not be established.",
                ),
            )

        if not expected:
            return ExecutionContextIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                expected_context=expected,
                observed_context=observed,
                status=ExecutionContextIntegrityStatus.INCOMPLETE,
                observations=(
                    "Expected execution context is incomplete.",
                ),
            )

        if not observed:
            return ExecutionContextIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                expected_context=expected,
                observed_context=observed,
                status=ExecutionContextIntegrityStatus.INCOMPLETE,
                observations=(
                    "Observed execution context is incomplete.",
                ),
            )

        if expected == observed:
            return ExecutionContextIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                expected_context=expected,
                observed_context=observed,
                status=ExecutionContextIntegrityStatus.CORRESPONDING,
                observations=(),
            )

        return ExecutionContextIntegrity(
            execution_id=envelope.execution_id,
            envelope=envelope,
            expected_context=expected,
            observed_context=observed,
            status=ExecutionContextIntegrityStatus.DRIFTED,
            observations=(
                "Observed context differs from expected context.",
            ),
        )