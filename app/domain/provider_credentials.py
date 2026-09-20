from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCredentialReference:
    """Opaque provider credential identity; never contains secret material."""

    provider_key: str
    credential_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.provider_key, str) or not self.provider_key.strip():
            raise ValueError("provider_key cannot be empty")
        if not isinstance(self.credential_ref, str) or not self.credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")