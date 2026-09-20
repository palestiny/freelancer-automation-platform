from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

    def __post_init__(self) -> None:
        if not isinstance(self.polarity, MetricPolarity):
            raise TypeError("polarity must be a MetricPolarity")


def interpret_metric_direction(
    *,
    direction: "DescriptiveDirection",
    policy: MetricDirectionPolicy | None,
) -> MetricDirectionInterpretation:
    if direction.value == "no_change":
        return MetricDirectionInterpretation.NEUTRAL
    if direction.value == "unavailable" or policy is None:
        return MetricDirectionInterpretation.NOT_INTERPRETABLE
    if policy.polarity is MetricPolarity.DIRECTION_NEUTRAL:
        return MetricDirectionInterpretation.NEUTRAL
    if policy.polarity is MetricPolarity.HIGHER_IS_FAVORABLE:
        return (
            MetricDirectionInterpretation.FAVORABLE
            if direction.value == "increased"
            else MetricDirectionInterpretation.UNFAVORABLE
        )
    return (
        MetricDirectionInterpretation.FAVORABLE
        if direction.value == "decreased"
        else MetricDirectionInterpretation.UNFAVORABLE
    )
