from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, Mapping

from models.execution_attestation import ExecutionAttestation
from models.execution_attestation_status import (
    ExecutionAttestationStatus,
)
from models.execution_certification import ExecutionCertification


class ExecutionAttestationService:
    """Creates attestations from bounded certification evidence."""

    def attest(
        self,
        *,
        execution_attestation_id: str,
        certification: ExecutionCertification,
        status: ExecutionAttestationStatus,
        statement: str,
        attested_at: datetime,
        attested_by: str,
        evidence_references: Iterable[str],
        metadata: Mapping[str, Any],
    ) -> ExecutionAttestation:
        if not isinstance(certification, ExecutionCertification):
            raise TypeError(
                "certification must be an ExecutionCertification"
            )

        references = tuple(evidence_references)

        if (
            certification.execution_certification_id
            not in references
        ):
            raise ValueError(
                "evidence_references must include the "
                "certification reference"
            )

        return ExecutionAttestation(
            execution_attestation_id=execution_attestation_id,
            subject_id=certification.subject_id,
            certification_id=(
                certification.execution_certification_id
            ),
            status=status,
            statement=statement,
            attested_at=attested_at,
            attested_by=attested_by,
            evidence_references=references,
            metadata=metadata,
        )