from datetime import datetime, timezone

import pytest

from models.execution_provenance import ExecutionProvenance
from models.execution_provenance_relationship import (
    ExecutionProvenanceRelationship,
)
from services.execution_provenance_service import (
    ExecutionProvenanceService,
)


def test_service_records_provenance():
    service = ExecutionProvenanceService()

    provenance = service.record(
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

    assert isinstance(provenance, ExecutionProvenance)
    assert provenance.execution_provenance_id == "PROVENANCE-001"
    assert provenance.subject_id == "RESULT-001"
    assert provenance.source_id == "INTENT-001"


def test_service_returns_records_in_recorded_order():
    service = ExecutionProvenanceService()

    service.record(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={},
    )

    service.record(
        execution_provenance_id="PROVENANCE-002",
        subject_id="REPLAY-001",
        source_id="RESULT-001",
        relationship=ExecutionProvenanceRelationship.REPLAYED_FROM,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="REPLAY-SERVICE",
        metadata={},
    )

    records = service.records()

    assert isinstance(records, tuple)
    assert [
        record.execution_provenance_id
        for record in records
    ] == [
        "PROVENANCE-001",
        "PROVENANCE-002",
    ]


def test_service_filters_by_subject():
    service = ExecutionProvenanceService()

    service.record(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={},
    )

    service.record(
        execution_provenance_id="PROVENANCE-002",
        subject_id="RECEIPT-001",
        source_id="RESULT-001",
        relationship=ExecutionProvenanceRelationship.RECORDED_FROM,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="RECEIPT-SERVICE",
        metadata={},
    )

    records = service.records_for_subject("RESULT-001")

    assert len(records) == 1
    assert records[0].subject_id == "RESULT-001"


def test_service_filters_by_source():
    service = ExecutionProvenanceService()

    service.record(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={},
    )

    service.record(
        execution_provenance_id="PROVENANCE-002",
        subject_id="POLICY-EVAL-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.EVALUATED_FROM,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="POLICY-SERVICE",
        metadata={},
    )

    records = service.records_for_source("INTENT-001")

    assert len(records) == 2
    assert all(
        record.source_id == "INTENT-001"
        for record in records
    )


def test_service_rejects_duplicate_provenance_id():
    service = ExecutionProvenanceService()

    service.record(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={},
    )

    with pytest.raises(ValueError):
        service.record(
            execution_provenance_id="PROVENANCE-001",
            subject_id="RECEIPT-001",
            source_id="RESULT-001",
            relationship=(
                ExecutionProvenanceRelationship.RECORDED_FROM
            ),
            recorded_at=datetime.now(timezone.utc),
            recorded_by="RECEIPT-SERVICE",
            metadata={},
        )


def test_service_preserves_model_validation():
    service = ExecutionProvenanceService()

    with pytest.raises(ValueError):
        service.record(
            execution_provenance_id="",
            subject_id="RESULT-001",
            source_id="INTENT-001",
            relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
            recorded_at=datetime.now(timezone.utc),
            recorded_by="EXECUTION-ENGINE",
            metadata={},
        )


def test_service_rejects_empty_subject_filter():
    service = ExecutionProvenanceService()

    with pytest.raises(ValueError):
        service.records_for_subject("")


def test_service_rejects_empty_source_filter():
    service = ExecutionProvenanceService()

    with pytest.raises(ValueError):
        service.records_for_source("")


def test_service_does_not_expose_mutable_internal_storage():
    service = ExecutionProvenanceService()

    snapshot = service.records()

    service.record(
        execution_provenance_id="PROVENANCE-001",
        subject_id="RESULT-001",
        source_id="INTENT-001",
        relationship=ExecutionProvenanceRelationship.PRODUCED_BY,
        recorded_at=datetime.now(timezone.utc),
        recorded_by="EXECUTION-ENGINE",
        metadata={},
    )

    assert snapshot == ()
    assert len(service.records()) == 1