from dataclasses import dataclass

import pytest

from app.application.provider_credential_resolution import (
    CredentialResolutionFailure,
    CredentialResolutionResult,
    ProviderCredentialResolver,
    resolve_provider_credential,
)


@dataclass(frozen=True)
class FakeResolver(ProviderCredentialResolver):
    provider_key: str
    credential_reference: str
    material: str | None

    def resolve(self, *, provider_key: str, credential_reference: str):
        if provider_key != self.provider_key or credential_reference != self.credential_reference:
            return CredentialResolutionResult.failure(
                CredentialResolutionFailure.NOT_FOUND
            )
        if self.material is None:
            return CredentialResolutionResult.failure(
                CredentialResolutionFailure.RESOLUTION_FAILED
            )
        return CredentialResolutionResult.success(
            provider_key=provider_key,
            credential_reference=credential_reference,
            material=self.material,
        )


def test_resolution_binds_provider_and_reference():
    result = resolve_provider_credential(
        resolver=FakeResolver("marketplace-a", "cred-1", "fake-secret"),
        provider_key="marketplace-a",
        credential_reference="cred-1",
    )
    assert result.success is True
    assert result.provider_key == "marketplace-a"
    assert result.credential_reference == "cred-1"
    assert result.material == "fake-secret"


def test_resolution_failure_is_explicit_without_fallback():
    result = resolve_provider_credential(
        resolver=FakeResolver("marketplace-a", "cred-1", "fake-secret"),
        provider_key="marketplace-b",
        credential_reference="cred-2",
    )
    assert result.success is False
    assert result.failure is CredentialResolutionFailure.NOT_FOUND
    assert result.material is None


def test_empty_provider_or_reference_is_rejected():
    resolver = FakeResolver("marketplace-a", "cred-1", "fake-secret")
    with pytest.raises(ValueError):
        resolve_provider_credential(
            resolver=resolver,
            provider_key="",
            credential_reference="cred-1",
        )
    with pytest.raises(ValueError):
        resolve_provider_credential(
            resolver=resolver,
            provider_key="marketplace-a",
            credential_reference="",
        )


def test_failed_resolution_cannot_carry_material():
    result = CredentialResolutionResult.failure(
        CredentialResolutionFailure.RESOLUTION_FAILED
    )
    assert result.success is False
    assert result.material is None
