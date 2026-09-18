import pytest

from app.domain.marketing_campaign import (
    CampaignAuthorization,
    CampaignChannel,
    CampaignObjective,
    CampaignPerformanceSnapshot,
    CampaignStatus,
    MarketingCampaign,
)


def make_campaign(**overrides):
    values = {
        "id": "campaign-1",
        "objective": CampaignObjective.CONVERSION,
        "channels": (CampaignChannel.PAID_SOCIAL,),
    }
    values.update(overrides)
    return MarketingCampaign(**values)


def test_campaign_can_move_from_draft_to_planned_to_running():
    campaign = make_campaign()

    campaign.plan()
    campaign.start()

    assert campaign.status == CampaignStatus.RUNNING


def test_campaign_requiring_approval_cannot_start_before_approval():
    campaign = make_campaign(authorization=CampaignAuthorization.REQUIRED)

    campaign.plan()

    with pytest.raises(ValueError):
        campaign.start()

    campaign.approve()
    campaign.start()

    assert campaign.status == CampaignStatus.RUNNING


def test_campaign_supports_pause_and_resume():
    campaign = make_campaign()
    campaign.plan()
    campaign.start()

    campaign.pause()
    assert campaign.status == CampaignStatus.PAUSED

    campaign.resume()
    assert campaign.status == CampaignStatus.RUNNING


def test_campaign_can_be_completed_or_cancelled():
    campaign = make_campaign()
    campaign.plan()
    campaign.start()
    campaign.complete()

    assert campaign.status == CampaignStatus.COMPLETED

    cancelled = make_campaign(id="campaign-2")
    cancelled.cancel()

    assert cancelled.status == CampaignStatus.CANCELLED


def test_campaign_requires_a_channel_and_non_negative_budget():
    with pytest.raises(ValueError):
        make_campaign(channels=())

    with pytest.raises(ValueError):
        make_campaign(budget_limit=-1)


def test_performance_snapshot_derives_marketing_metrics():
    snapshot = CampaignPerformanceSnapshot(
        impressions=1000,
        clicks=100,
        leads=20,
        conversions=5,
        spend=50,
        revenue=250,
    )

    assert snapshot.ctr == pytest.approx(0.10)
    assert snapshot.conversion_rate == pytest.approx(0.25)
    assert snapshot.customer_acquisition_cost == pytest.approx(10)
    assert snapshot.roas == pytest.approx(5)


def test_performance_metrics_are_undefined_when_denominators_are_zero():
    snapshot = CampaignPerformanceSnapshot()

    assert snapshot.ctr is None
    assert snapshot.conversion_rate is None
    assert snapshot.customer_acquisition_cost is None
    assert snapshot.roas is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("impressions", -1),
        ("clicks", -1),
        ("leads", -1),
        ("conversions", -1),
        ("spend", -1),
        ("revenue", -1),
    ],
)
def test_performance_snapshot_rejects_negative_metrics(field, value):
    values = {}
    values[field] = value

    with pytest.raises(ValueError):
        CampaignPerformanceSnapshot(**values)


def test_clicks_cannot_exceed_impressions():
    with pytest.raises(ValueError):
        CampaignPerformanceSnapshot(impressions=10, clicks=11)


def test_conversions_cannot_exceed_leads():
    with pytest.raises(ValueError):
        CampaignPerformanceSnapshot(leads=2, conversions=3)
