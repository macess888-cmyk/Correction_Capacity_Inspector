from models.relationship import Relationship


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