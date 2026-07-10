from typing import List, Optional

from models.evidence import Evidence


class EvidenceRegistry:
    """
    Registry responsible for storing Evidence objects.
    """

    def __init__(self):
        self._evidence: List[Evidence] = []

    def add(self, evidence: Evidence) -> None:
        self._evidence.append(evidence)

    def get_all(self) -> List[Evidence]:
        return self._evidence

    def get_by_id(
        self,
        evidence_id: str,
    ) -> Optional[Evidence]:

        for evidence in self._evidence:
            if evidence.evidence_id == evidence_id:
                return evidence

        return None