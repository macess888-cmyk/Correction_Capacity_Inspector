from __future__ import annotations

from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)
from registries.execution_consistency_record_registry import (
    ExecutionConsistencyRecordRegistry,
)
from registries.execution_transition_intent_registry import (
    ExecutionTransitionIntentRegistry,
)
from registries.execution_transition_receipt_registry import (
    ExecutionTransitionReceiptRegistry,
)


class ExecutionConsistencyService:
    """
    Provides append-only access to transition intents,
    transition receipts, and consistency records.

    This service records runtime consistency artifacts only.

    It does not mutate execution state, perform compensation,
    or authorize transitions.
    """

    def __init__(
        self,
        intent_registry: ExecutionTransitionIntentRegistry,
        receipt_registry: ExecutionTransitionReceiptRegistry,
        consistency_registry: ExecutionConsistencyRecordRegistry,
    ) -> None:
        self._intent_registry = intent_registry
        self._receipt_registry = receipt_registry
        self._consistency_registry = consistency_registry

    def record_intent(
        self,
        intent: ExecutionTransitionIntent,
    ) -> None:
        self._intent_registry.add(intent)

    def get_intent(
        self,
        transition_id: str,
    ) -> ExecutionTransitionIntent:
        return self._intent_registry.get(transition_id)

    def intent_exists(
        self,
        transition_id: str,
    ) -> bool:
        return self._intent_registry.exists(transition_id)

    def list_intents(
        self,
    ) -> list[ExecutionTransitionIntent]:
        return self._intent_registry.list()

    def list_intents_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionTransitionIntent]:
        return self._intent_registry.list_for_execution(
            execution_id
        )

    def record_receipt(
        self,
        receipt: ExecutionTransitionReceipt,
    ) -> None:
        self._receipt_registry.add(receipt)

    def get_receipt(
        self,
        receipt_id: str,
    ) -> ExecutionTransitionReceipt:
        return self._receipt_registry.get(receipt_id)

    def receipt_exists(
        self,
        receipt_id: str,
    ) -> bool:
        return self._receipt_registry.exists(receipt_id)

    def list_receipts(
        self,
    ) -> list[ExecutionTransitionReceipt]:
        return self._receipt_registry.list()

    def list_receipts_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionTransitionReceipt]:
        return self._receipt_registry.list_for_execution(
            execution_id
        )

    def record_consistency_issue(
        self,
        record: ExecutionConsistencyRecord,
    ) -> None:
        self._consistency_registry.add(record)

    def get_consistency_issue(
        self,
        record_id: str,
    ) -> ExecutionConsistencyRecord:
        return self._consistency_registry.get(record_id)

    def consistency_issue_exists(
        self,
        record_id: str,
    ) -> bool:
        return self._consistency_registry.exists(record_id)

    def list_consistency_issues(
        self,
    ) -> list[ExecutionConsistencyRecord]:
        return self._consistency_registry.list()

    def list_consistency_issues_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionConsistencyRecord]:
        return self._consistency_registry.list_for_execution(
            execution_id
        )