from typing import List, Optional

from contracts import MutableRegistryContract
from models.evidence import Evidence


class EvidenceRegistry(MutableRegistryContract):
    """
    Stores and retrieves Evidence objects.
    """

    def __init__(self) -> None:
        self._evidence: List[Evidence] = []

    def add(self, evidence: Evidence) -> None:
        self._evidence.append(evidence)

    def get_all(self) -> List[Evidence]:
        return list(self._evidence)

    def get_by_id(
        self,
        evidence_id: str,
    ) -> Optional[Evidence]:
        for evidence in self._evidence:
            if evidence.evidence_id == evidence_id:
                return evidence

        return None

    def update(self, evidence: Evidence) -> None:
        for index, existing in enumerate(self._evidence):
            if existing.evidence_id == evidence.evidence_id:
                self._evidence[index] = evidence
                return

        raise KeyError(f"Evidence not found: {evidence.evidence_id}")

    def remove(self, evidence_id: str) -> None:
        for index, evidence in enumerate(self._evidence):
            if evidence.evidence_id == evidence_id:
                del self._evidence[index]
                return

        raise KeyError(f"Evidence not found: {evidence_id}")