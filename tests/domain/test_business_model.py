import pytest

from app.domain.business_model import BusinessModelHypothesis, BusinessModelType


def test_business_model_can_represent_low_touch_recurring_revenue():
    model = BusinessModelHypothesis(
        name="Automated reporting service",
        model_type=BusinessModelType.SUBSCRIPTION,
        target_customer="small agencies",
        value_proposition="Recurring reports with minimal manual intervention",
        revenue_model="monthly subscription",
        recurring_revenue=True,
        automation_intensity=0.9,
    )

    assert model.recurring_revenue is True
    assert model.automation_intensity == 0.9


def test_business_model_rejects_invalid_automation_intensity():
    with pytest.raises(ValueError):
        BusinessModelHypothesis(
            name="Model",
            model_type=BusinessModelType.SAAS,
            target_customer="Customers",
            value_proposition="Value",
            revenue_model="Subscription",
            automation_intensity=1.1,
        )
