from typing import List, Optional

from models.evidence import Evidence
from registries.evidence_registry import EvidenceRegistry


class EvidenceService:
    """
    Coordinates evidence operations.
    """

    def __init__(self, registry: EvidenceRegistry):
        self._registry = registry

    def add_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        self._registry.add(evidence)

    def get_evidence(
        self,
        evidence_id: str,
    ) -> Optional[Evidence]:
        return self._registry.get_by_id(evidence_id)

    def get_all_evidence(self) -> List[Evidence]:
        return self._registry.get_all()