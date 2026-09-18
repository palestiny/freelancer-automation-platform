from dataclasses import dataclass
from enum import Enum

from .business_performance import PerformanceSourceType
from .performance_aggregation import PerformanceAggregate


class SourceReliabilityReason(str, Enum):
    ELIGIBLE = "eligible"
    INSUFFICIENT_RELIABILITY = "insufficient_reliability"
    MISSING_SOURCE_POLICY = "missing_source_policy"


@dataclass(frozen=True)
class PerformanceSourceReliabilityPolicy:
    minimum_reliability: int = 60
    reliability_by_source_type: tuple[tuple[PerformanceSourceType, int], ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.minimum_reliability <= 100:
            raise ValueError("minimum_reliability must be between 0 and 100")

        seen: set[PerformanceSourceType] = set()
        for source_type, reliability in self.reliability_by_source_type:
            if source_type in seen:
                raise ValueError("source types must be unique")
            seen.add(source_type)
            if not isinstance(reliability, int) or isinstance(reliability, bool):
                raise TypeError("source reliability must be an integer")
            if not 0 <= reliability <= 100:
                raise ValueError("source reliability must be between 0 and 100")

    def reliability_for(
        self,
        source_type: PerformanceSourceType,
    ) -> int | None:
        for configured_type, reliability in self.reliability_by_source_type:
            if configured_type is source_type:
                return reliability
        return None


@dataclass(frozen=True)
class SourceReliabilityAssessment:
    eligible: bool
    reason: SourceReliabilityReason
    minimum_reliability: int | None

    def __post_init__(self) -> None:
        if not isinstance(self.reason, SourceReliabilityReason):
            raise TypeError("reason must be a SourceReliabilityReason")
        if (self.eligible and self.reason is not SourceReliabilityReason.ELIGIBLE) or (
            not self.eligible and self.reason is SourceReliabilityReason.ELIGIBLE
        ):
            raise ValueError("eligible state must match reliability reason")
        if self.minimum_reliability is not None and not 0 <= self.minimum_reliability <= 100:
            raise ValueError("minimum_reliability must be between 0 and 100")


def assess_source_reliability(
    *,
    aggregate: PerformanceAggregate,
    policy: PerformanceSourceReliabilityPolicy,
) -> SourceReliabilityAssessment:
    reliabilities = tuple(
        policy.reliability_for(source_type)
        for source_type in aggregate.source_types
    )

    if any(reliability is None for reliability in reliabilities):
        return SourceReliabilityAssessment(
            eligible=False,
            reason=SourceReliabilityReason.MISSING_SOURCE_POLICY,
            minimum_reliability=None,
        )

    minimum_reliability = min(reliability for reliability in reliabilities if reliability is not None)

    if minimum_reliability < policy.minimum_reliability:
        return SourceReliabilityAssessment(
            eligible=False,
            reason=SourceReliabilityReason.INSUFFICIENT_RELIABILITY,
            minimum_reliability=minimum_reliability,
        )

    return SourceReliabilityAssessment(
        eligible=True,
        reason=SourceReliabilityReason.ELIGIBLE,
        minimum_reliability=minimum_reliability,
    )
