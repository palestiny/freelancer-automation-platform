from dataclasses import dataclass
from enum import Enum


class BusinessModelType(Enum):
    FREELANCE_SERVICE = "FREELANCE_SERVICE"
    PRODUCTIZED_SERVICE = "PRODUCTIZED_SERVICE"
    MANAGED_SERVICE = "MANAGED_SERVICE"
    SAAS = "SAAS"
    API = "API"
    DIGITAL_PRODUCT = "DIGITAL_PRODUCT"
    GAME = "GAME"
    WHITE_LABEL = "WHITE_LABEL"
    SUBSCRIPTION = "SUBSCRIPTION"
    PARTNERSHIP = "PARTNERSHIP"


@dataclass(frozen=True)
class BusinessModelHypothesis:
    name: str
    model_type: BusinessModelType
    target_customer: str
    value_proposition: str
    revenue_model: str
    recurring_revenue: bool = False
    automation_intensity: float = 0.0

    def __post_init__(self) -> None:
        for field_name in (
            "name",
            "target_customer",
            "value_proposition",
            "revenue_model",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")

        if not 0 <= self.automation_intensity <= 1:
            raise ValueError("automation_intensity must be between 0 and 1")
