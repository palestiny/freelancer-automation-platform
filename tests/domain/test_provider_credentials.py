import pytest

from app.domain.provider_credentials import ProviderCredentialReference


def test_credential_reference_preserves_only_opaque_identity():
    reference = ProviderCredentialReference(provider_key="marketplace-a", credential_ref="credential-123")
    assert reference.provider_key == "marketplace-a"
    assert reference.credential_ref == "credential-123"


@pytest.mark.parametrize(("provider_key", "credential_ref"), [("", "credential-123"), ("marketplace-a", ""), ("   ", "credential-123"), ("marketplace-a", "   ")])
def test_credential_reference_rejects_empty_identity(provider_key, credential_ref):
    with pytest.raises(ValueError):
        ProviderCredentialReference(provider_key=provider_key, credential_ref=credential_ref)


def test_credential_reference_does_not_accept_secret_material_field():
    assert "secret" not in ProviderCredentialReference.__annotations__
    assert "token" not in ProviderCredentialReference.__annotations__