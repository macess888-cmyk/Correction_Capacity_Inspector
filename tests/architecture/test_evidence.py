import pytest

from contracts import MutableRegistryContract
from models.evidence import Evidence
from registries.evidence_registry import EvidenceRegistry
from services.evidence_service import EvidenceService


def make_evidence(
    evidence_id: str,
    title: str = "Example Evidence",
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        title=title,
        description="Example observation.",
        source="Inspection Session",
    )


def test_evidence_creation():

    evidence = make_evidence("evd-001")

    assert evidence.evidence_id == "evd-001"
    assert evidence.title == "Example Evidence"
    assert evidence.status == "Candidate"


def test_evidence_registry_contract_and_mutation():

    registry = EvidenceRegistry()

    assert isinstance(registry, MutableRegistryContract)

    original = make_evidence("evd-002")

    registry.add(original)

    assert registry.get_by_id("evd-002") == original
    assert registry.get_all() == [original]

    updated = make_evidence(
        "evd-002",
        title="Updated Evidence",
    )

    registry.update(updated)

    assert registry.get_by_id("evd-002") == updated
    assert registry.get_all() == [updated]

    registry.remove("evd-002")

    assert registry.get_by_id("evd-002") is None
    assert registry.get_all() == []


def test_evidence_registry_rejects_missing_update_and_remove():

    registry = EvidenceRegistry()
    missing = make_evidence("missing")

    with pytest.raises(KeyError):
        registry.update(missing)

    with pytest.raises(KeyError):
        registry.remove("missing")


def test_evidence_service_uses_registry():

    registry = EvidenceRegistry()
    service = EvidenceService(registry)

    evidence = make_evidence("evd-003")

    service.add_evidence(evidence)

    assert service.get_evidence("evd-003") == evidence
    assert service.get_all_evidence() == [evidence]


def test_evidence_registry_rejects_duplicate_identifiers():

    registry = EvidenceRegistry()

    evidence = make_evidence("evd-duplicate")

    registry.add(evidence)

    with pytest.raises(ValueError):
        registry.add(evidence)