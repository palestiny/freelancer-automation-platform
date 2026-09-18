from datetime import datetime, timezone

import pytest

from app.domain.revenue import (
    RecurringPeriod,
    RevenueContract,
    RevenueContractStatus,
    RevenueEvent,
    RevenueType,
)


def test_one_time_contract_does_not_require_recurring_period():
    contract = RevenueContract(
        id="rev-1",
        model_id="model-1",
        revenue_type=RevenueType.ONE_TIME,
        amount=500,
        currency="USD",
    )

    assert contract.recurring_period is None
    assert contract.status is RevenueContractStatus.PROPOSED


def test_recurring_contract_requires_explicit_period():
    contract = RevenueContract(
        id="rev-2",
        model_id="model-2",
        revenue_type=RevenueType.RECURRING,
        amount=49,
        currency="USD",
        recurring_period=RecurringPeriod.MONTHLY,
    )

    assert contract.recurring_period is RecurringPeriod.MONTHLY


def test_revenue_contract_rejects_inconsistent_recurring_data():
    with pytest.raises(ValueError, match="recurring_period"):
        RevenueContract(
            id="rev-1",
            model_id="model-1",
            revenue_type=RevenueType.RECURRING,
            amount=49,
            currency="USD",
        )

    with pytest.raises(ValueError, match="one-time"):
        RevenueContract(
            id="rev-1",
            model_id="model-1",
            revenue_type=RevenueType.ONE_TIME,
            amount=49,
            currency="USD",
            recurring_period=RecurringPeriod.MONTHLY,
        )


def test_contract_rejects_invalid_values():
    with pytest.raises(ValueError, match="amount"):
        RevenueContract(
            id="rev-1",
            model_id="model-1",
            revenue_type=RevenueType.ONE_TIME,
            amount=-1,
            currency="USD",
        )


def test_revenue_event_represents_realized_revenue():
    event = RevenueEvent(
        contract_id="rev-1",
        amount=49,
        currency="USD",
        recognized_at=datetime(2026, 9, 18, tzinfo=timezone.utc),
    )

    assert event.amount == 49
    assert event.currency == "USD"


def test_revenue_event_rejects_invalid_values():
    with pytest.raises(ValueError, match="amount"):
        RevenueEvent(
            contract_id="rev-1",
            amount=-1,
            currency="USD",
            recognized_at=datetime.now(timezone.utc),
        )

    with pytest.raises(ValueError, match="currency"):
        RevenueEvent(
            contract_id="rev-1",
            amount=10,
            currency=" ",
            recognized_at=datetime.now(timezone.utc),
        )
