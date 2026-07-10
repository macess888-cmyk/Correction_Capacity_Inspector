from models.evidence import Evidence


def test_evidence_creation():

    evidence = Evidence(
        evidence_id="evd-001",
        title="Example Evidence",
        description="Example observation.",
        source="Inspection Session",
    )

    assert evidence.evidence_id == "evd-001"
    assert evidence.title == "Example Evidence"
    assert evidence.status == "Candidate"