import pytest

from contracts import MutableRegistryContract
from models.relationship import Relationship
from registries.relationship_registry import RelationshipRegistry


def test_relationship_creation():

    relationship = Relationship(
        relationship_id="rel-001",
        source_id="object-a",
        target_id="object-b",
        relationship_type="connects_to",
    )

    assert relationship.relationship_id == "rel-001"
    assert relationship.source_id == "object-a"
    assert relationship.target_id == "object-b"
    assert relationship.relationship_type == "connects_to"
    assert relationship.status == "Candidate"


def test_relationship_registry_contract_and_mutation():

    registry = RelationshipRegistry()

    assert isinstance(registry, MutableRegistryContract)

    original = Relationship(
        relationship_id="rel-002",
        source_id="object-a",
        target_id="object-b",
        relationship_type="connects_to",
    )

    registry.add(original)

    assert registry.get_by_id("rel-002") == original
    assert registry.get_all() == [original]

    updated = Relationship(
        relationship_id="rel-002",
        source_id="object-a",
        target_id="object-c",
        relationship_type="supports",
    )

    registry.update(updated)

    assert registry.get_by_id("rel-002") == updated
    assert registry.get_all() == [updated]

    registry.remove("rel-002")

    assert registry.get_by_id("rel-002") is None
    assert registry.get_all() == []


def test_relationship_registry_queries():

    registry = RelationshipRegistry()

    relationship_one = Relationship(
        relationship_id="rel-003",
        source_id="object-a",
        target_id="object-b",
        relationship_type="supports",
    )

    relationship_two = Relationship(
        relationship_id="rel-004",
        source_id="object-c",
        target_id="object-b",
        relationship_type="challenges",
    )

    registry.add(relationship_one)
    registry.add(relationship_two)

    assert registry.by_source("object-a") == [relationship_one]

    assert registry.by_target("object-b") == [
        relationship_one,
        relationship_two,
    ]

    assert registry.by_type("supports") == [relationship_one]


def test_relationship_registry_rejects_missing_update_and_remove():

    registry = RelationshipRegistry()

    missing = Relationship(
        relationship_id="missing",
        source_id="object-a",
        target_id="object-b",
        relationship_type="connects_to",
    )

    with pytest.raises(KeyError):
        registry.update(missing)

    with pytest.raises(KeyError):
        registry.remove("missing")


def test_relationship_registry_rejects_duplicate_identifiers():

    registry = RelationshipRegistry()

    relationship = Relationship(
        relationship_id="rel-duplicate",
        source_id="object-a",
        target_id="object-b",
        relationship_type="supports",
    )

    registry.add(relationship)

    with pytest.raises(ValueError):
        registry.add(relationship)