from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class MessageClassification(Enum):
    INQUIRY = "INQUIRY"
    SUPPORT = "SUPPORT"
    FEEDBACK = "FEEDBACK"
    COMPLAINT = "COMPLAINT"
    SPAM = "SPAM"
    OTHER = "OTHER"


class ResponseAuthorization(Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    REQUIRED = "REQUIRED"
    APPROVED = "APPROVED"


@dataclass(frozen=True)
class SocialPresence:
    id: str
    channel: str
    external_account_id: str

    def __post_init__(self) -> None:
        for field_name in ("id", "channel", "external_account_id"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")


@dataclass(frozen=True)
class IncomingMessage:
    id: str
    presence_id: str
    sender_reference: str
    content: str
    received_at: datetime
    classification: MessageClassification = MessageClassification.OTHER

    def __post_init__(self) -> None:
        for field_name in ("id", "presence_id", "sender_reference", "content"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")


@dataclass(frozen=True)
class ResponseDraft:
    id: str
    incoming_message_id: str
    content: str
    authorization: ResponseAuthorization = ResponseAuthorization.REQUIRED
    escalation_required: bool = False

    def __post_init__(self) -> None:
        for field_name in ("id", "incoming_message_id", "content"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")

        if self.escalation_required and self.authorization is ResponseAuthorization.APPROVED:
            raise ValueError("Escalated responses cannot be approved for automated sending")


@dataclass(frozen=True)
class SentMessage:
    id: str
    presence_id: str
    recipient_reference: str
    content: str
    sent_at: datetime
    source_draft_id: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("id", "presence_id", "recipient_reference", "content"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")
