from app.application.retry_worker_dispatch import RetryWorkerDispatchStatus, dispatch_one_retry


def test_provider_failure_transitions_claimed_command_to_manual_review(worker_context):
    result = dispatch_one_retry(**worker_context(provider_raises=True))

    assert result.status is RetryWorkerDispatchStatus.PROVIDER_FAILURE
    assert result.command.state.value == "requires_manual_review"
    assert result.failure == "provider_execution_failed"


def test_provider_failure_persistence_failure_remains_explicit(worker_context):
    result = dispatch_one_retry(**worker_context(provider_raises=True, save_manual_review_raises=True))

    assert result.status is RetryWorkerDispatchStatus.PROVIDER_FAILURE
    assert result.command.state.value == "execution_in_progress"
    assert result.failure == "provider_failure_persistence_failed"