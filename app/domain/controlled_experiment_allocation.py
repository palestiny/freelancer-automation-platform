from dataclasses import dataclass
import hashlib


_ALLOCATION_BASIS_POINTS = 10_000


@dataclass(frozen=True)
class ExperimentAllocationPlan:
    experiment_id: str
    variants: tuple[str, ...]
    allocation_weights: tuple[int, ...]
    salt: str

    def __post_init__(self) -> None:
        if not self.experiment_id.strip():
            raise ValueError("experiment_id cannot be empty")
        if not self.salt.strip():
            raise ValueError("salt cannot be empty")
        if not self.variants:
            raise ValueError("variants cannot be empty")
        if len(self.variants) != len(self.allocation_weights):
            raise ValueError("variants and allocation_weights must have the same length")
        if any(not isinstance(v, str) or not v.strip() for v in self.variants):
            raise ValueError("variants cannot contain empty names")
        if len(set(self.variants)) != len(self.variants):
            raise ValueError("variants must be unique")
        if any(
            isinstance(weight, bool) or not isinstance(weight, int) or weight <= 0
            for weight in self.allocation_weights
        ):
            raise ValueError("allocation_weights must be positive integers")
        if sum(self.allocation_weights) != _ALLOCATION_BASIS_POINTS:
            raise ValueError("allocation_weights must sum to 10000")


def allocate_experiment_variant(
    *,
    plan: ExperimentAllocationPlan,
    subject_id: str,
) -> str:
    if not subject_id.strip():
        raise ValueError("subject_id cannot be empty")

    material = f"{plan.experiment_id}\x00{subject_id}\x00{plan.salt}".encode("utf-8")
    digest = hashlib.sha256(material).digest()
    bucket = int.from_bytes(digest[:8], "big") % _ALLOCATION_BASIS_POINTS

    cumulative = 0
    for variant, weight in zip(plan.variants, plan.allocation_weights):
        cumulative += weight
        if bucket < cumulative:
            return variant

    raise RuntimeError("allocation bucket fell outside the configured weights")
