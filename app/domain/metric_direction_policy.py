from dataclasses import dataclass
from enum import Enum
from .performance_evidence_decision_support import DescriptiveDirection

class MetricPolarity(str, Enum):
    HIGHER_IS_FAVORABLE = "higher_is_favorable"
    LOWER_IS_FAVORABLE = "lower_is_favorable"
    DIRECTION_NEUTRAL = "direction_neutral"

class MetricDirectionInterpretation(str, Enum):
    FAVORABLE = "favorable"
    UNFAVORABLE = "unfavorable"
    NEUTRAL = "neutral"
    NOT_INTERPRETABLE = "not_interpretable"

@dataclass(frozen=True)
class MetricDirectionPolicy:
    polarity: MetricPolarity
    def __post_init__(self):
        if not isinstance(self.polarity, MetricPolarity): raise TypeError("polarity must be a MetricPolarity")

def interpret_metric_direction(*, direction: DescriptiveDirection, policy: MetricDirectionPolicy | None) -> MetricDirectionInterpretation:
    if direction is DescriptiveDirection.NO_CHANGE: return MetricDirectionInterpretation.NEUTRAL
    if direction is DescriptiveDirection.UNAVAILABLE or policy is None: return MetricDirectionInterpretation.NOT_INTERPRETABLE
    if policy.polarity is MetricPolarity.DIRECTION_NEUTRAL: return MetricDirectionInterpretation.NEUTRAL
    if policy.polarity is MetricPolarity.HIGHER_IS_FAVORABLE: return MetricDirectionInterpretation.FAVORABLE if direction is DescriptiveDirection.INCREASED else MetricDirectionInterpretation.UNFAVORABLE
    return MetricDirectionInterpretation.FAVORABLE if direction is DescriptiveDirection.DECREASED else MetricDirectionInterpretation.UNFAVORABLE
