from dataclasses import dataclass
from enum import Enum


class CampaignObjective(str, Enum):
    AWARENESS = "awareness"
    TRAFFIC = "traffic"
    LEAD_GENERATION = "lead_generation"
    CONVERSION = "conversion"
    RETENTION = "retention"


class CampaignChannel(str, Enum):
    ORGANIC_SOCIAL = "organic_social"
    PAID_SOCIAL = "paid_social"
    SEARCH_ADS = "search_ads"
    EMAIL = "email"
    CONTENT = "content"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignAuthorization(str, Enum):
    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    APPROVED = "approved"


@dataclass
class MarketingCampaign:
    """Provider-independent campaign planning and lifecycle state."""

    id: str
    objective: CampaignObjective
    channels: tuple[CampaignChannel, ...]
    budget_limit: float = 0.0
    authorization: CampaignAuthorization = CampaignAuthorization.NOT_REQUIRED
    status: CampaignStatus = CampaignStatus.DRAFT

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.channels:
            raise ValueError("at least one channel is required")
        if self.budget_limit < 0:
            raise ValueError("budget_limit cannot be negative")

    def plan(self) -> None:
        if self.status != CampaignStatus.DRAFT:
            raise ValueError("campaign can only be planned from DRAFT")
        self.status = CampaignStatus.PLANNED

    def approve(self) -> None:
        if self.authorization != CampaignAuthorization.REQUIRED:
            raise ValueError("campaign does not require approval")
        self.authorization = CampaignAuthorization.APPROVED

    def start(self) -> None:
        if self.status != CampaignStatus.PLANNED:
            raise ValueError("campaign can only start from PLANNED")
        if self.authorization == CampaignAuthorization.REQUIRED:
            raise ValueError("campaign requires approval before starting")
        self.status = CampaignStatus.RUNNING

    def pause(self) -> None:
        if self.status != CampaignStatus.RUNNING:
            raise ValueError("only RUNNING campaigns can be paused")
        self.status = CampaignStatus.PAUSED

    def resume(self) -> None:
        if self.status != CampaignStatus.PAUSED:
            raise ValueError("only PAUSED campaigns can be resumed")
        if self.authorization == CampaignAuthorization.REQUIRED:
            raise ValueError("campaign requires approval before starting")
        self.status = CampaignStatus.RUNNING

    def complete(self) -> None:
        if self.status not in (CampaignStatus.RUNNING, CampaignStatus.PAUSED):
            raise ValueError("only active campaigns can be completed")
        self.status = CampaignStatus.COMPLETED

    def cancel(self) -> None:
        if self.status in (CampaignStatus.COMPLETED, CampaignStatus.CANCELLED):
            raise ValueError("completed or cancelled campaigns cannot be cancelled")
        self.status = CampaignStatus.CANCELLED


@dataclass(frozen=True)
class CampaignPerformanceSnapshot:
    """Observed campaign performance for a defined measurement snapshot."""

    impressions: int = 0
    clicks: int = 0
    leads: int = 0
    conversions: int = 0
    spend: float = 0.0
    revenue: float = 0.0

    def __post_init__(self) -> None:
        integer_metrics = {
            "impressions": self.impressions,
            "clicks": self.clicks,
            "leads": self.leads,
            "conversions": self.conversions,
        }
        for name, value in integer_metrics.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} cannot be negative")

        if self.clicks > self.impressions:
            raise ValueError("clicks cannot exceed impressions")
        if self.conversions > self.leads:
            raise ValueError("conversions cannot exceed leads")
        if self.spend < 0:
            raise ValueError("spend cannot be negative")
        if self.revenue < 0:
            raise ValueError("revenue cannot be negative")

    @property
    def ctr(self) -> float | None:
        if self.impressions == 0:
            return None
        return self.clicks / self.impressions

    @property
    def conversion_rate(self) -> float | None:
        if self.leads == 0:
            return None
        return self.conversions / self.leads

    @property
    def customer_acquisition_cost(self) -> float | None:
        if self.conversions == 0:
            return None
        return self.spend / self.conversions

    @property
    def roas(self) -> float | None:
        if self.spend == 0:
            return None
        return self.revenue / self.spend
