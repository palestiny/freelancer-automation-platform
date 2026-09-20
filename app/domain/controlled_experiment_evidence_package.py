from dataclasses import dataclass
from enum import Enum


class ExperimentEvidencePackageStatus(str, Enum):
    REVIEW_READY = "review_ready"
    NOT_REVIEW_READY = "not_review_ready"


@dataclass(frozen=True)
class ControlledExperimentEvidencePackage:
    experiment_id: str
    metric_name: str
    unit: str
    first_variant_id: str
    second_variant_id: str
    status: ExperimentEvidencePackageStatus
    descriptive_difference: float
    statistical_difference_detected: bool | None
    observation_ids: tuple[str, ...]
    selected_variant_id: None = None

    def __post_init__(self) -> None:
        for name in (
            "experiment_id",
            "metric_name",
            "unit",
            "first_variant_id",
            "second_variant_id",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.first_variant_id == self.second_variant_id:
            raise ValueError("variant ids must be distinct")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if self.selected_variant_id is not None:
            raise ValueError("evidence package cannot select a variant")


def build_experiment_evidence_package(
    *,
    experiment_id: str,
    metric_name: str,
    unit: str,
    first_variant_id: str,
    second_variant_id: str,
    readiness_status: str,
    descriptive_difference: float,
    statistical_status: str,
    rejects_null: bool | None,
    observation_ids: tuple[str, ...],
) -> ControlledExperimentEvidencePackage:
    if statistical_status == "applicable" and not isinstance(rejects_null, bool):
        raise ValueError("applicable statistical result requires rejects_null")
    if statistical_status != "applicable" and rejects_null is not None:
        raise ValueError("non-applicable statistical result cannot carry rejects_null")

    statistical_difference = rejects_null if statistical_status == "applicable" else None

    return ControlledExperimentEvidencePackage(
        experiment_id=experiment_id,
        metric_name=metric_name,
        unit=unit,
        first_variant_id=first_variant_id,
        second_variant_id=second_variant_id,
        status=(
            ExperimentEvidencePackageStatus.REVIEW_READY
            if readiness_status == "ready"
            else ExperimentEvidencePackageStatus.NOT_REVIEW_READY
        ),
        descriptive_difference=descriptive_difference,
        statistical_difference_detected=statistical_difference,
        observation_ids=observation_ids,
    )
