from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from datetime import datetime
from typing import Any

from models.execution_certification import ExecutionCertification
from models.execution_certification_status import (
    ExecutionCertificationStatus,
)


CertificationEvaluation = tuple[
    ExecutionCertificationStatus,
    str,
    Mapping[str, Any],
]

CertificationEvaluator = Callable[
    [tuple[str, ...]],
    CertificationEvaluation,
]


class ExecutionCertificationService:
    """Evaluates evidence references against registered profiles."""

    def __init__(self) -> None:
        self._profiles: dict[str, CertificationEvaluator] = {}

    def register_profile(
        self,
        *,
        certification_profile_id: str,
        evaluator: CertificationEvaluator,
    ) -> None:
        if not isinstance(certification_profile_id, str):
            raise TypeError(
                "certification_profile_id must be a string"
            )

        if not certification_profile_id.strip():
            raise ValueError(
                "certification_profile_id must not be empty"
            )

        if not callable(evaluator):
            raise TypeError("evaluator must be callable")

        if certification_profile_id in self._profiles:
            raise ValueError(
                "certification_profile_id is already registered"
            )

        self._profiles[certification_profile_id] = evaluator

    def evaluate(
        self,
        *,
        execution_certification_id: str,
        certification_profile_id: str,
        subject_id: str,
        evaluated_at: datetime,
        evaluated_by: str,
        evidence_references: Iterable[str],
    ) -> ExecutionCertification:
        evaluator = self._profiles.get(certification_profile_id)

        if evaluator is None:
            raise ValueError(
                f"no certification profile registered for: "
                f"{certification_profile_id}"
            )

        references = tuple(evidence_references)

        status, reason, findings = evaluator(references)

        if not isinstance(
            status,
            ExecutionCertificationStatus,
        ):
            raise TypeError(
                "profile evaluator status must be an "
                "ExecutionCertificationStatus"
            )

        if not isinstance(reason, str):
            raise TypeError(
                "profile evaluator reason must be a string"
            )

        if not reason.strip():
            raise ValueError(
                "profile evaluator reason must not be empty"
            )

        if not isinstance(findings, Mapping):
            raise TypeError(
                "profile evaluator findings must be a mapping"
            )

        return ExecutionCertification(
            execution_certification_id=(
                execution_certification_id
            ),
            certification_profile_id=certification_profile_id,
            subject_id=subject_id,
            status=status,
            evaluated_at=evaluated_at,
            evaluated_by=evaluated_by,
            reason=reason,
            evidence_references=references,
            findings=findings,
        )