from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .action_authorization import ActionAuthorization, ActionAuthorizationStatus, ActionClass, AutonomyLevel


class ExecutionRequestStatus(str, Enum):
    PREPARED = "prepared"
    REJECTED = "rejected"


@dataclass(frozen=True)
class AuthorizedExecutionRequest:
    request_id: str
    idempotency_key: str
    action_class: ActionClass
    autonomy_level: AutonomyLevel
    policy_id: str
    policy_version: str
    status: ExecutionRequestStatus
    prepared_at: datetime | None = None
    current_observation_ids: tuple[str, ...] = ()
    baseline_observation_ids: tuple[str, ...] = ()
    statistical_observation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("request_id", "idempotency_key", "policy_id", "policy_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if self.status is ExecutionRequestStatus.PREPARED and not self.idempotency_key.strip():
            raise ValueError("prepared requests require an idempotency key")
        for name, ids in (("current_observation_ids", self.current_observation_ids), ("baseline_observation_ids", self.baseline_observation_ids), ("statistical_observation_ids", self.statistical_observation_ids)):
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")
            if any(not isinstance(value, str) or not value.strip() for value in ids):
                raise ValueError(f"{name} must contain non-empty strings")


def prepare_execution_request(*, request_id: str, idempotency_key: str,
                              authorization: ActionAuthorization) -> AuthorizedExecutionRequest:
    if not request_id.strip() or not idempotency_key.strip():
        raise ValueError("request_id and idempotency_key cannot be empty")
    status = (ExecutionRequestStatus.PREPARED
              if authorization.status is ActionAuthorizationStatus.AUTHORIZED
              else ExecutionRequestStatus.REJECTED)
    return AuthorizedExecutionRequest(
        request_id=request_id,
        idempotency_key=idempotency_key,
        action_class=authorization.action_class,
        autonomy_level=authorization.requested_autonomy,
        policy_id=authorization.policy_id,
        policy_version=authorization.policy_version,
        status=status,
        current_observation_ids=authorization.current_observation_ids,
        baseline_observation_ids=authorization.baseline_observation_ids,
        statistical_observation_ids=authorization.statistical_observation_ids,
    )
