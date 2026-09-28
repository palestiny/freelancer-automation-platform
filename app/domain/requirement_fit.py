from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityRequirement:
    requirement_id: str
    capability_id: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id must not be empty")
        if not self.capability_id.strip():
            raise ValueError("capability_id must not be empty")
        if not self.evidence_refs:
            raise ValueError("capability requirement requires evidence references")
        if any(not isinstance(value, str) or not value.strip() for value in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty strings")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("evidence_refs must not contain duplicates")
