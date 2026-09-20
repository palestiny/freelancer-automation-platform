from app.application.execution_status_port import (
    ProviderExecutionStatusQuery,
    observe_provider_execution_status,
)
from app.application.retry_status_assessment_application import RetryStatusAssessmentApplication
from app.domain.execution_retry import RetryCommandState
from app.domain.retry_status_reconciliation import (
    RetryRecoveryAssessmentStatus,
    assess_retry_status_reconciliation,
)


class RetryStatusReconciliationCoordinator:
    def __init__(self, *, store, status_port, assessment_application: RetryStatusAssessmentApplication):
        self._store = store
        self._status_port = status_port
        self._assessment_application = assessment_application

    def reconcile(self, *, command_id: str, expected_state: RetryCommandState):
        command = self._store.get(command_id)
        if command is None:
            raise KeyError(command_id)
        if command.state is not expected_state:
            raise RuntimeError("retry command state changed before reconciliation")

        if command.state is not RetryCommandState.EXECUTION_IN_PROGRESS:
            return command

        query = ProviderExecutionStatusQuery(
            request_id=command.request_id,
            idempotency_key=command.idempotency_key,
        )
        status = observe_provider_execution_status(
            port=self._status_port,
            query=query,
        )
        assessment = assess_retry_status_reconciliation(
            command=command,
            provider_status=status,
        )

        if assessment.status in {
            RetryRecoveryAssessmentStatus.REMAINS_AMBIGUOUS,
            RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED,
        }:
            return command

        return self._assessment_application.apply(
            command_id=command_id,
            assessment=assessment,
            expected_state=expected_state,
        )
