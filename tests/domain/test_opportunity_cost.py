import math
import pytest

from app.domain.opportunity_cost import (
    OpportunityCostEvidence,
    calculate_opportunity_cost,
)


def test_opportunity_cost_is_foregone_alternative_profit():
    result = calculate_opportunity_cost(
        quantity=10,
        selected_expected_profit=40,
        alternative_expected_profit=70,
    )
    assert result.opportunity_cost == 30
    assert result.quantity == 10


def test_selected_use_with_higher_profit_has_zero_opportunity_cost():
    result = calculate_opportunity_cost(
        quantity=10,
        selected_expected_profit=80,
        alternative_expected_profit=70,
    )
    assert result.opportunity_cost == 0


def test_result_preserves_expected_values():
    result = calculate_opportunity_cost(
        quantity=4,
        selected_expected_profit=20,
        alternative_expected_profit=25,
    )
    assert result.selected_expected_profit == 20
    assert result.alternative_expected_profit == 25


@pytest.mark.parametrize(
    "quantity,selected,alternative",
    [
        (0, 10, 20),
        (-1, 10, 20),
        (1, math.inf, 20),
        (1, 10, math.nan),
    ],
)
def test_invalid_numeric_inputs_are_rejected(quantity, selected, alternative):
    with pytest.raises(ValueError):
        calculate_opportunity_cost(
            quantity=quantity,
            selected_expected_profit=selected,
            alternative_expected_profit=alternative,
        )


def test_value_object_rejects_negative_opportunity_cost():
    with pytest.raises(ValueError):
        OpportunityCostEvidence(
            quantity=1,
            selected_expected_profit=20,
            alternative_expected_profit=10,
            opportunity_cost=-1,
        )
