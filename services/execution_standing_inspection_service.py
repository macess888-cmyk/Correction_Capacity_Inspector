from __future__ import annotations

from datetime import datetime
from typing import Iterable

from models.execution_attestation import ExecutionAttestation
from models.execution_certification import ExecutionCertification
from models.execution_revocation import ExecutionRevocation
from models.execution_revocation_status import (
    ExecutionRevocationStatus,
)
from models.execution_standing_inspection import (
    ExecutionStandingInspection,
)
from models.execution_standing_status import ExecutionStandingStatus


class ExecutionStandingInspectionService:
    """Inspects current standing without modifying historical records."""

    def inspect_attestation(
        self,
        *,
        execution_standing_inspection_id: str,
        attestation: ExecutionAttestation,
        revocations: Iterable[ExecutionRevocation],
        inspected_at: datetime,
    ) -> ExecutionStandingInspection:
        if not isinstance(attestation, ExecutionAttestation):
            raise TypeError(
                "attestation must be an ExecutionAttestation"
            )

        return self._inspect(
            execution_standing_inspection_id=(
                execution_standing_inspection_id
            ),
            subject_id=attestation.execution_attestation_id,
            subject_type="EXECUTION_ATTESTATION",
            revocations=revocations,
            inspected_at=inspected_at,
        )

    def inspect_certification(
        self,
        *,
        execution_standing_inspection_id: str,
        certification: ExecutionCertification,
        revocations: Iterable[ExecutionRevocation],
        inspected_at: datetime,
    ) -> ExecutionStandingInspection:
        if not isinstance(certification, ExecutionCertification):
            raise TypeError(
                "certification must be an ExecutionCertification"
            )

        return self._inspect(
            execution_standing_inspection_id=(
                execution_standing_inspection_id
            ),
            subject_id=certification.execution_certification_id,
            subject_type="EXECUTION_CERTIFICATION",
            revocations=revocations,
            inspected_at=inspected_at,
        )

    def _inspect(
        self,
        *,
        execution_standing_inspection_id: str,
        subject_id: str,
        subject_type: str,
        revocations: Iterable[ExecutionRevocation],
        inspected_at: datetime,
    ) -> ExecutionStandingInspection:
        revocation_records = tuple(revocations)

        for revocation in revocation_records:
            if not isinstance(revocation, ExecutionRevocation):
                raise TypeError(
                    "revocations must contain only "
                    "ExecutionRevocation records"
                )

        subject_records = tuple(
            revocation
            for revocation in revocation_records
            if revocation.subject_id == subject_id
        )

        mismatched_records = tuple(
            revocation
            for revocation in subject_records
            if revocation.subject_type != subject_type
        )

        if mismatched_records:
            governing_record = max(
                mismatched_records,
                key=lambda revocation: revocation.revoked_at,
            )

            return ExecutionStandingInspection(
                execution_standing_inspection_id=(
                    execution_standing_inspection_id
                ),
                subject_id=subject_id,
                subject_type=subject_type,
                status=ExecutionStandingStatus.INDETERMINATE,
                inspected_at=inspected_at,
                reason=(
                    "a revocation references the subject with an "
                    "incompatible subject type"
                ),
                governing_record_id=(
                    governing_record.execution_revocation_id
                ),
                evidence_references=(
                    subject_id,
                    governing_record.execution_revocation_id,
                ),
                findings={
                    "revocation_count": len(subject_records),
                    "subject_type_mismatch": True,
                },
            )

        applicable_records = tuple(
            revocation
            for revocation in subject_records
            if revocation.subject_type == subject_type
        )

        if not applicable_records:
            return ExecutionStandingInspection(
                execution_standing_inspection_id=(
                    execution_standing_inspection_id
                ),
                subject_id=subject_id,
                subject_type=subject_type,
                status=ExecutionStandingStatus.ACTIVE,
                inspected_at=inspected_at,
                reason="no later revocation record applies",
                governing_record_id=subject_id,
                evidence_references=(subject_id,),
                findings={
                    "revocation_count": 0,
                    "subject_type_mismatch": False,
                },
            )

        governing_record = max(
            applicable_records,
            key=lambda revocation: revocation.revoked_at,
        )

        status = self._map_revocation_status(
            governing_record.status
        )

        return ExecutionStandingInspection(
            execution_standing_inspection_id=(
                execution_standing_inspection_id
            ),
            subject_id=subject_id,
            subject_type=subject_type,
            status=status,
            inspected_at=inspected_at,
            reason=governing_record.reason,
            governing_record_id=(
                governing_record.execution_revocation_id
            ),
            evidence_references=(
                subject_id,
                governing_record.execution_revocation_id,
            ),
            findings={
                "revocation_count": len(applicable_records),
                "subject_type_mismatch": False,
            },
        )

    @staticmethod
    def _map_revocation_status(
        status: ExecutionRevocationStatus,
    ) -> ExecutionStandingStatus:
        mapping = {
            ExecutionRevocationStatus.REVOKED: (
                ExecutionStandingStatus.REVOKED
            ),
            ExecutionRevocationStatus.SUSPENDED: (
                ExecutionStandingStatus.SUSPENDED
            ),
            ExecutionRevocationStatus.WITHDRAWN: (
                ExecutionStandingStatus.WITHDRAWN
            ),
        }

        return mapping[status]