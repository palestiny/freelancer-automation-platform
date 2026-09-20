import pytest
from app.domain.performance_evidence_decision_support import DescriptiveDirection
from app.domain.metric_direction_policy import MetricDirectionInterpretation, MetricDirectionPolicy, MetricPolarity, interpret_metric_direction

def test_higher_is_favorable_interprets_increase():
    assert interpret_metric_direction(direction=DescriptiveDirection.INCREASED, policy=MetricDirectionPolicy(polarity=MetricPolarity.HIGHER_IS_FAVORABLE)) is MetricDirectionInterpretation.FAVORABLE

def test_higher_is_favorable_interprets_decrease_as_unfavorable():
    assert interpret_metric_direction(direction=DescriptiveDirection.DECREASED, policy=MetricDirectionPolicy(polarity=MetricPolarity.HIGHER_IS_FAVORABLE)) is MetricDirectionInterpretation.UNFAVORABLE

def test_lower_is_favorable_reverses_direction():
    assert interpret_metric_direction(direction=DescriptiveDirection.INCREASED, policy=MetricDirectionPolicy(polarity=MetricPolarity.LOWER_IS_FAVORABLE)) is MetricDirectionInterpretation.UNFAVORABLE

def test_neutral_polarity_does_not_infer_preference():
    assert interpret_metric_direction(direction=DescriptiveDirection.INCREASED, policy=MetricDirectionPolicy(polarity=MetricPolarity.DIRECTION_NEUTRAL)) is MetricDirectionInterpretation.NEUTRAL

def test_no_policy_is_not_interpretable():
    assert interpret_metric_direction(direction=DescriptiveDirection.INCREASED, policy=None) is MetricDirectionInterpretation.NOT_INTERPRETABLE

def test_no_change_is_neutral_for_any_policy():
    for polarity in MetricPolarity:
        assert interpret_metric_direction(direction=DescriptiveDirection.NO_CHANGE, policy=MetricDirectionPolicy(polarity=polarity)) is MetricDirectionInterpretation.NEUTRAL

def test_policy_rejects_invalid_polarity():
    with pytest.raises(TypeError):
        MetricDirectionPolicy(polarity="higher_is_favorable")
