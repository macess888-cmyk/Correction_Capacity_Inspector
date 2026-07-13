from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, Mapping

from models.execution_attestation import ExecutionAttestation
from models.execution_certification import ExecutionCertification
from models.execution_revocation import ExecutionRevocation
from models.execution_revocation_status import (
    ExecutionRevocationStatus,
)


class ExecutionRevocationService:
    """Creates immutable revocations without altering source records."""

    def revoke_attestation(
        self,
        *,
        execution_revocation_id: str,
        attestation: ExecutionAttestation,
        status: ExecutionRevocationStatus,
        reason: str,
        revoked_at: datetime,
        revoked_by: str,
        evidence_references: Iterable[str],
        metadata: Mapping[str, Any],
    ) -> ExecutionRevocation:
        if not isinstance(attestation, ExecutionAttestation):
            raise TypeError(
                "attestation must be an ExecutionAttestation"
            )

        references = tuple(evidence_references)

        if attestation.execution_attestation_id not in references:
            raise ValueError(
                "evidence_references must include the "
                "attestation reference"
            )

        return ExecutionRevocation(
            execution_revocation_id=execution_revocation_id,
            subject_id=attestation.execution_attestation_id,
            subject_type="EXECUTION_ATTESTATION",
            status=status,
            reason=reason,
            revoked_at=revoked_at,
            revoked_by=revoked_by,
            evidence_references=references,
            metadata=metadata,
        )

    def revoke_certification(
        self,
        *,
        execution_revocation_id: str,
        certification: ExecutionCertification,
        status: ExecutionRevocationStatus,
        reason: str,
        revoked_at: datetime,
        revoked_by: str,
        evidence_references: Iterable[str],
        metadata: Mapping[str, Any],
    ) -> ExecutionRevocation:
        if not isinstance(certification, ExecutionCertification):
            raise TypeError(
                "certification must be an ExecutionCertification"
            )

        references = tuple(evidence_references)

        if certification.execution_certification_id not in references:
            raise ValueError(
                "evidence_references must include the "
                "certification reference"
            )

        return ExecutionRevocation(
            execution_revocation_id=execution_revocation_id,
            subject_id=certification.execution_certification_id,
            subject_type="EXECUTION_CERTIFICATION",
            status=status,
            reason=reason,
            revoked_at=revoked_at,
            revoked_by=revoked_by,
            evidence_references=references,
            metadata=metadata,
        )