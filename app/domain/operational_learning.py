from dataclasses import dataclass
from .operational_measurement import LearningSignal, OperationalMeasurement


@dataclass(frozen=True)
class OperationalLearningPolicy:
    minimum_observations: int = 3
    minimum_average_relative_variance: float = 0.10

    def __post_init__(self) -> None:
        if self.minimum_observations <= 0:
            raise ValueError("minimum_observations must be greater than zero")
        if self.minimum_average_relative_variance < 0:
            raise ValueError("minimum_average_relative_variance cannot be negative")


def derive_learning_signal(
    measurements: tuple[OperationalMeasurement, ...],
    *,
    policy: OperationalLearningPolicy,
    signal_id: str,
    statement: str,
) -> LearningSignal | None:
    if not measurements:
        return None

    business_id = measurements[0].business_id
    if any(m.business_id != business_id for m in measurements):
        raise ValueError("all measurements must belong to the same business")

    if any(m.metric_name != measurements[0].metric_name or m.unit != measurements[0].unit for m in measurements):
        raise ValueError("all measurements must use the same metric and unit")

    if len(measurements) < policy.minimum_observations:
        return None

    relative_variances = [
        m.relative_variance
        for m in measurements
        if m.relative_variance is not None
    ]
    if not relative_variances:
        return None

    average_relative_variance = sum(relative_variances) / len(relative_variances)
    if abs(average_relative_variance) < policy.minimum_average_relative_variance:
        return None

    evidence_quality = round(sum(m.evidence_quality for m in measurements) / len(measurements))

    return LearningSignal(
        id=signal_id,
        business_id=business_id,
        source_measurement_ids=tuple(m.id for m in measurements),
        statement=statement,
        evidence_quality=evidence_quality,
    )
