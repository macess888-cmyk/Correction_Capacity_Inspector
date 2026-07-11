from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_readiness import ExecutionReadiness
from models.execution_readiness_status import (
    ExecutionReadinessStatus,
)


class ExecutionReadinessService:
    """
    Assesses whether an authorized execution plan is operationally ready.

    Readiness determines preparedness only.
    It grants no execution and performs no mutation.
    """

    def assess(
        self,
        authorization: ExecutionAuthorization,
    ) -> ExecutionReadiness:

        if authorization.status == ExecutionAuthorizationStatus.AUTHORIZED:
            return ExecutionReadiness(
                execution_id=authorization.execution_id,
                authorization=authorization,
                status=ExecutionReadinessStatus.READY,
                reason=(
                    "Execution authorization is present "
                    "and the plan is ready."
                ),
            )

        if authorization.status == ExecutionAuthorizationStatus.PENDING:
            return ExecutionReadiness(
                execution_id=authorization.execution_id,
                authorization=authorization,
                status=ExecutionReadinessStatus.NOT_READY,
                reason="Execution authorization is still pending.",
            )

        if (
            authorization.status
            == ExecutionAuthorizationStatus.NOT_AUTHORIZED
        ):
            return ExecutionReadiness(
                execution_id=authorization.execution_id,
                authorization=authorization,
                status=ExecutionReadinessStatus.BLOCKED,
                reason=(
                    "Execution is blocked because authorization "
                    "was not granted."
                ),
            )

        return ExecutionReadiness(
            execution_id=authorization.execution_id,
            authorization=authorization,
            status=ExecutionReadinessStatus.UNKNOWN,
            reason="Execution readiness could not be determined.",
        )