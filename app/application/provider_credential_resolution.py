from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class CredentialResolutionFailure(str, Enum):
    NOT_FOUND = "not_found"
    RESOLUTION_FAILED = "resolution_failed"


@dataclass(frozen=True)
class CredentialResolutionResult:
    success: bool
    provider_key: str | None = None
    credential_reference: str | None = None
    material: str | None = field(default=None, repr=False)
    failure_reason: CredentialResolutionFailure | None = None

    def __post_init__(self) -> None:
        if self.success:
            if not self.provider_key or not self.credential_reference:
                raise ValueError("successful resolution requires provider and reference")
            if self.material is None or not self.material:
                raise ValueError("successful resolution requires credential material")
            if self.failure_reason is not None:
                raise ValueError("successful resolution cannot contain failure")
        else:
            if self.material is not None:
                raise ValueError("failed resolution cannot carry credential material")
            if self.failure_reason is None:
                raise ValueError("failed resolution requires a failure reason")

    @classmethod
    def success(
        cls,
        *,
        provider_key: str,
        credential_reference: str,
        material: str,
    ) -> "CredentialResolutionResult":
        return cls(
            success=True,
            provider_key=provider_key,
            credential_reference=credential_reference,
            material=material,
        )

    @classmethod
    def failure(
        cls,
        failure: CredentialResolutionFailure,
    ) -> "CredentialResolutionResult":
        return cls(success=False, failure_reason=failure)


class ProviderCredentialResolver(Protocol):
    def resolve(
        self,
        *,
        provider_key: str,
        credential_reference: str,
    ) -> CredentialResolutionResult:
        ...


def resolve_provider_credential(
    *,
    resolver: ProviderCredentialResolver,
    provider_key: str,
    credential_reference: str,
) -> CredentialResolutionResult:
    if not provider_key.strip():
        raise ValueError("provider_key cannot be empty")
    if not credential_reference.strip():
        raise ValueError("credential_reference cannot be empty")

    result = resolver.resolve(
        provider_key=provider_key,
        credential_reference=credential_reference,
    )

    if not isinstance(result, CredentialResolutionResult):
        raise TypeError("resolver must return CredentialResolutionResult")

    if result.success and (
        result.provider_key != provider_key
        or result.credential_reference != credential_reference
    ):
        raise ValueError(
            "resolved credential must remain bound to provider and reference"
        )

    return result
