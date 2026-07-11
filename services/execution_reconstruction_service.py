from __future__ import annotations

from collections.abc import Sequence

from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)
from models.execution_evidence_completeness import (
    ExecutionEvidenceCompleteness,
)
from models.execution_reconstruction import (
    ExecutionReconstruction,
)
from models.execution_reconstruction_integrity import (
    ExecutionReconstructionIntegrity,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)
from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


class ExecutionReconstructionService:
    """
    Derives an execution reconstruction from immutable evidence.

    This service does not read or mutate current execution state.

    It does not execute transitions, perform recovery,
    or establish historical truth.
    """

    def reconstruct(
        self,
        execution_id: str,
        grammar_version: str,
        intents: Sequence[ExecutionTransitionIntent],
        events: Sequence[InspectionExecutionEvent],
        receipts: Sequence[ExecutionTransitionReceipt],
        consistency_records: Sequence[
            ExecutionConsistencyRecord
        ],
    ) -> ExecutionReconstruction:
        execution_intents = tuple(
            intent
            for intent in intents
            if intent.execution_id == execution_id
        )

        execution_events = tuple(
            event
            for event in events
            if event.execution_id == execution_id
        )

        execution_receipts = tuple(
            receipt
            for receipt in receipts
            if receipt.execution_id == execution_id
        )

        execution_consistency_records = tuple(
            record
            for record in consistency_records
            if record.execution_id == execution_id
        )

        warnings: list[str] = []

        if not execution_events:
            return ExecutionReconstruction(
                execution_id=execution_id,
                grammar_version=grammar_version,
                reconstructed_status=(
                    InspectionExecutionStatus.CREATED
                ),
                reconstructed_stage="NOT_STARTED",
                evidence_processed=(
                    len(execution_intents)
                    + len(execution_receipts)
                    + len(execution_consistency_records)
                ),
                integrity=(
                    ExecutionReconstructionIntegrity.UNKNOWN
                ),
                completeness=(
                    ExecutionEvidenceCompleteness.INSUFFICIENT
                ),
                warnings=(
                    "No execution events were available.",
                ),
            )

        operations_applied = tuple(
            event.event_type.value
            for event in execution_events
            if event.previous_status
            != event.current_status
        )

        final_event = execution_events[-1]

        evidence_processed = (
            len(execution_intents)
            + len(execution_events)
            + len(execution_receipts)
            + len(execution_consistency_records)
        )

        if execution_consistency_records:
            integrity = (
                ExecutionReconstructionIntegrity.INCONSISTENT
            )
            warnings.append(
                "One or more consistency records were present."
            )
        else:
            integrity = (
                ExecutionReconstructionIntegrity.CONSISTENT
            )

        expected_receipt_count = len(
            [
                event
                for event in execution_events
                if event.previous_status
                != event.current_status
            ]
        )

        if (
            execution_intents
            and len(execution_receipts)
            >= expected_receipt_count
        ):
            completeness = (
                ExecutionEvidenceCompleteness.COMPLETE
            )
        elif execution_intents or execution_receipts:
            completeness = (
                ExecutionEvidenceCompleteness.PARTIAL
            )
            warnings.append(
                "Transition evidence was incomplete."
            )
        else:
            completeness = (
                ExecutionEvidenceCompleteness.INSUFFICIENT
            )
            warnings.append(
                "No transition intents or receipts were available."
            )

        return ExecutionReconstruction(
            execution_id=execution_id,
            grammar_version=grammar_version,
            reconstructed_status=final_event.current_status,
            reconstructed_stage=final_event.stage,
            operations_applied=operations_applied,
            evidence_processed=evidence_processed,
            integrity=integrity,
            completeness=completeness,
            warnings=tuple(warnings),
        )