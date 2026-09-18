from datetime import datetime, timezone

import pytest

from app.domain.customer_communication import (
    IncomingMessage,
    MessageClassification,
    ResponseAuthorization,
    ResponseDraft,
    SentMessage,
    SocialPresence,
)


def test_social_presence_requires_identity():
    presence = SocialPresence(
        id="presence-1",
        channel="social",
        external_account_id="account-1",
    )

    assert presence.channel == "social"


def test_incoming_message_preserves_classification_and_content():
    message = IncomingMessage(
        id="msg-1",
        presence_id="presence-1",
        sender_reference="customer-1",
        content="Can you help me?",
        received_at=datetime(2026, 9, 18, tzinfo=timezone.utc),
        classification=MessageClassification.SUPPORT,
    )

    assert message.classification is MessageClassification.SUPPORT
    assert message.content == "Can you help me?"


def test_response_draft_requires_explicit_authorization_by_default():
    draft = ResponseDraft(
        id="draft-1",
        incoming_message_id="msg-1",
        content="Thanks for contacting us.",
    )

    assert draft.authorization is ResponseAuthorization.REQUIRED


def test_escalated_response_cannot_be_approved_for_automatic_sending():
    with pytest.raises(ValueError, match="Escalated"):
        ResponseDraft(
            id="draft-1",
            incoming_message_id="msg-1",
            content="We will investigate this complaint.",
            authorization=ResponseAuthorization.APPROVED,
            escalation_required=True,
        )


def test_sent_message_is_separate_from_response_draft():
    sent = SentMessage(
        id="sent-1",
        presence_id="presence-1",
        recipient_reference="customer-1",
        content="Your issue has been received.",
        sent_at=datetime(2026, 9, 18, tzinfo=timezone.utc),
        source_draft_id="draft-1",
    )

    assert sent.source_draft_id == "draft-1"


def test_domain_rejects_empty_communication_fields():
    with pytest.raises(ValueError, match="content"):
        ResponseDraft(
            id="draft-1",
            incoming_message_id="msg-1",
            content=" ",
        )

    with pytest.raises(ValueError, match="external_account_id"):
        SocialPresence(
            id="presence-1",
            channel="social",
            external_account_id=" ",
        )
