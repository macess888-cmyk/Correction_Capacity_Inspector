from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_provenance import ExecutionProvenance
from models.execution_provenance_relationship import (
    ExecutionProvenanceRelationship,
)


def make_execution_provenance() -> ExecutionProvenance:
    return ExecutionProvenance(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={
            "action": "reconcile",
        },
    )


def test_execution_provenance_can_be_created():
    provenance = make_execution_provenance()

    assert provenance.execution_provenance_id == "PROVENANCE-001"
    assert provenance.subject_id == "RESULT-001"
    assert provenance.source_id == "INTENT-001"
    assert (
        provenance.relationship
        is ExecutionProvenanceRelationship.PRODUCED_BY
    )
    assert provenance.recorded_by == "EXECUTION-ENGINE"
    assert provenance.metadata["action"] == "reconcile"


def test_execution_provenance_is_immutable():
    provenance = make_execution_provenance()

    with pytest.raises(FrozenInstanceError):
        provenance.subject_id = "RESULT-002"


def test_execution_provenance_metadata_is_immutable():
    provenance = make_execution_provenance()

    with pytest.raises(TypeError):
        provenance.metadata["action"] = "stop"


def test_execution_provenance_defensively_copies_metadata():
    metadata = {
        "action": "reconcile",
    }

    provenance = ExecutionProvenance(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata=metadata,
    )

    metadata["action"] = "stop"

    assert provenance.metadata["action"] == "reconcile"


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_provenance_id",
        "subject_id",
        "source_id",
        "recorded_by",
    ],
)
def test_execution_provenance_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_provenance_id": "PROVENANCE-001",
        "subject_id": "RESULT-001",
        "source_id": "INTENT-001",
        "relationship": (
            ExecutionProvenanceRelationship.PRODUCED_BY
        ),
        "recorded_at": datetime.now(timezone.utc),
        "recorded_by": "EXECUTION-ENGINE",
        "metadata": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionProvenance(**values)


def test_execution_provenance_rejects_invalid_relationship():
    with pytest.raises(TypeError):
        ExecutionProvenance(
            execution_provenance_id="PROVENANCE-001",
            subject_id="RESULT-001",
            source_id="INTENT-001",
            relationship="PRODUCED_BY",
            recorded_at=datetime.now(timezone.utc),
            recorded_by="EXECUTION-ENGINE",
            metadata={},
        )


def test_execution_provenance_rejects_missing_recorded_at():
    with pytest.raises(ValueError):
        ExecutionProvenance(
            execution_provenance_id="PROVENANCE-001",
            subject_id="RESULT-001",
            source_id="INTENT-001",
            relationship=(
                ExecutionProvenanceRelationship.PRODUCED_BY
            ),
            recorded_at=None,
            recorded_by="EXECUTION-ENGINE",
            metadata={},
        )


def test_execution_provenance_rejects_non_mapping_metadata():
    with pytest.raises(TypeError):
        ExecutionProvenance(
            execution_provenance_id="PROVENANCE-001",
            subject_id="RESULT-001",
            source_id="INTENT-001",
            relationship=(
                ExecutionProvenanceRelationship.PRODUCED_BY
            ),
            recorded_at=datetime.now(timezone.utc),
            recorded_by="EXECUTION-ENGINE",
            metadata="invalid",
        )


def test_execution_provenance_rejects_self_reference():
    with pytest.raises(ValueError):
        ExecutionProvenance(
            execution_provenance_id="PROVENANCE-001",
            subject_id="RESULT-001",
            source_id="RESULT-001",
            relationship=(
                ExecutionProvenanceRelationship.DERIVED_FROM
            ),
            recorded_at=datetime.now(timezone.utc),
            recorded_by="EXECUTION-ENGINE",
            metadata={},
        )


def test_execution_provenance_contains_no_truth_claim():
    provenance = make_execution_provenance()

    assert not hasattr(provenance, "valid")
    assert not hasattr(provenance, "verified")
    assert not hasattr(provenance, "truth")


def test_execution_provenance_contains_no_governance_state():
    provenance = make_execution_provenance()

    assert not hasattr(provenance, "authorized")
    assert not hasattr(provenance, "admissible")
    assert not hasattr(provenance, "refused")