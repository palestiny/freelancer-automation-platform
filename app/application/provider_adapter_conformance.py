from app.domain.authorized_execution_request import AuthorizedExecutionRequest


from __future__ import annotations


def validate_provider_execution_result(
    request: AuthorizedExecutionRequest,
    result: object,
) -> None:
    from app.application.execution_port import ProviderExecutionResult

    if not isinstance(result, ProviderExecutionResult):
        raise TypeError("provider result must be a ProviderExecutionResult")

    if result.request_id != request.request_id:
        raise ValueError("provider result request_id does not match execution request")

    if result.idempotency_key != request.idempotency_key:
        raise ValueError(
            "provider result idempotency_key does not match execution request"
        )

    if result.observed_at.tzinfo is None or result.observed_at.utcoffset() is None:
        raise ValueError("provider result observed_at must be timezone-aware")
