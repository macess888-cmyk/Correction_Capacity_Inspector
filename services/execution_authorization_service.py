from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_plan import ExecutionPlan
from models.execution_plan_status import ExecutionPlanStatus


class ExecutionAuthorizationService:
    """
    Determines the authorization state of an execution plan.

    Authorization determines admissibility only.
    It grants no execution and performs no mutation.
    """

    def authorize(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionAuthorization:

        if plan.status == ExecutionPlanStatus.AVAILABLE:
            return ExecutionAuthorization(
                execution_id=plan.execution_id,
                plan=plan,
                status=ExecutionAuthorizationStatus.PENDING,
                reason="Execution plan awaits authorization.",
            )

        if plan.status == ExecutionPlanStatus.INCOMPLETE:
            return ExecutionAuthorization(
                execution_id=plan.execution_id,
                plan=plan,
                status=ExecutionAuthorizationStatus.NOT_AUTHORIZED,
                reason="Incomplete execution plans cannot be authorized.",
            )

        if plan.status == ExecutionPlanStatus.NOT_PLANNABLE:
            return ExecutionAuthorization(
                execution_id=plan.execution_id,
                plan=plan,
                status=ExecutionAuthorizationStatus.NOT_AUTHORIZED,
                reason=(
                    "Non-plannable execution plans cannot be authorized."
                ),
            )

        return ExecutionAuthorization(
            execution_id=plan.execution_id,
            plan=plan,
            status=ExecutionAuthorizationStatus.UNKNOWN,
            reason="Authorization could not be determined.",
        )