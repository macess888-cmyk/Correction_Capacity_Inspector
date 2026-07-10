from __future__ import annotations

from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)


class ExecutionTransitionReceiptRegistry:
    """Append-only registry for transition receipts."""

    def __init__(self) -> None:
        self._receipts: dict[
            str,
            ExecutionTransitionReceipt,
        ] = {}

    def add(
        self,
        receipt: ExecutionTransitionReceipt,
    ) -> None:
        if receipt.receipt_id in self._receipts:
            raise ValueError(
                f"Transition receipt already exists: "
                f"{receipt.receipt_id}"
            )

        self._receipts[receipt.receipt_id] = receipt

    def get(
        self,
        receipt_id: str,
    ) -> ExecutionTransitionReceipt:
        if receipt_id not in self._receipts:
            raise KeyError(
                f"Transition receipt not found: {receipt_id}"
            )

        return self._receipts[receipt_id]

    def exists(self, receipt_id: str) -> bool:
        return receipt_id in self._receipts

    def list(self) -> list[ExecutionTransitionReceipt]:
        return list(self._receipts.values())

    def list_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionTransitionReceipt]:
        return [
            receipt
            for receipt in self._receipts.values()
            if receipt.execution_id == execution_id
        ]

    def count(self) -> int:
        return len(self._receipts)