import pytest

from app.domain.business_model import BusinessModelHypothesis, BusinessModelType
from app.domain.opportunity_type import OpportunityType
from app.domain.venture_pipeline import Venture, VentureStage


def test_venture_moves_through_validation_to_revenue_and_scale():
    venture = Venture(
        id="v-1",
        name="Automated reporting",
        opportunity_type=OpportunityType.SAAS,
        business_models=(
            BusinessModelHypothesis(
                name="Subscription SaaS",
                model_type=BusinessModelType.SAAS,
                target_customer="small agencies",
                value_proposition="Automated reports",
                revenue_model="monthly subscription",
                recurring_revenue=True,
                automation_intensity=0.9,
            ),
        ),
    )

    for stage in (
        VentureStage.RESEARCHING,
        VentureStage.THESIS_CREATED,
        VentureStage.ECONOMICALLY_EVALUATED,
        VentureStage.VALIDATION_REQUIRED,
        VentureStage.MVP,
        VentureStage.EARLY_REVENUE,
        VentureStage.PROVEN,
        VentureStage.SCALE,
    ):
        venture.advance_to(stage)

    assert venture.stage is VentureStage.SCALE


def test_killed_venture_is_terminal():
    venture = Venture("v-2", "Test", OpportunityType.GAME)

    venture.advance_to(VentureStage.KILLED)

    with pytest.raises(ValueError):
        venture.advance_to(VentureStage.RESEARCHING)
