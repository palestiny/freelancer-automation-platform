from dataclasses import dataclass
from enum import Enum


class CriterionId(Enum):
    ELIGIBILITY = "ELIGIBILITY"
    REQUIREMENT_FIT = "REQUIREMENT_FIT"
    ESTIMATED_EFFORT = "ESTIMATED_EFFORT"
    ECONOMIC_FIT = "ECONOMIC_FIT"
    CLIENT_PROJECT_RISK = "CLIENT_PROJECT_RISK"
    SUCCESS_CONFIDENCE = "SUCCESS_CONFIDENCE"


class CriterionOutcome(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class OverallOutcome(Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class EvaluationPolicy:
    policy_id: str
    policy_version: str
    required_criteria: tuple[CriterionId, ...]

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must not be empty")
        if not self.policy_version.strip():
            raise ValueError("policy_version must not be empty")
        if not self.required_criteria:
            raise ValueError("evaluation policy must define at least one criterion")
        if any(not isinstance(item, CriterionId) for item in self.required_criteria):
            raise TypeError("required_criteria must contain CriterionId values")
        if len(set(self.required_criteria)) != len(self.required_criteria):
            raise ValueError("required_criteria must not contain duplicates")


@dataclass(frozen=True)
class CriterionEvaluation:
    policy_id: str
    policy_version: str
    criterion_id: CriterionId
    outcome: CriterionOutcome
    evidence_refs: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    rationale: str | None = None

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must not be empty")
        if not self.policy_version.strip():
            raise ValueError("policy_version must not be empty")
        if not isinstance(self.criterion_id, CriterionId):
            raise TypeError("criterion_id must be a CriterionId")
        if not isinstance(self.outcome, CriterionOutcome):
            raise TypeError("outcome must be a CriterionOutcome")
        for name, values in (
            ("evidence_refs", self.evidence_refs),
            ("missing_evidence", self.missing_evidence),
            ("uncertainty", self.uncertainty),
        ):
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{name} must contain non-empty strings")
        if self.rationale is not None and not isinstance(self.rationale, str):
            raise TypeError("rationale must be a string or None")


@dataclass(frozen=True)
class OpportunityEvaluation:
    policy_id: str
    policy_version: str
    criteria: tuple[CriterionEvaluation, ...]
    overall_outcome: OverallOutcome

    def __post_init__(self) -> None:
        if not self.criteria:
            raise ValueError("opportunity evaluation must contain criterion results")
        if any(
            item.policy_id != self.policy_id
            or item.policy_version != self.policy_version
            for item in self.criteria
        ):
            raise ValueError("criterion result policy identity does not match evaluation")
        criterion_ids = [item.criterion_id for item in self.criteria]
        if len(set(criterion_ids)) != len(criterion_ids):
            raise ValueError("opportunity evaluation must not duplicate criteria")
        if not isinstance(self.overall_outcome, OverallOutcome):
            raise TypeError("overall_outcome must be an OverallOutcome")


def compose_overall_outcome(
    criteria: tuple[CriterionEvaluation, ...],
) -> OverallOutcome:
    if not criteria:
        raise ValueError("at least one criterion result is required")

    outcomes = {item.outcome for item in criteria}
    if CriterionOutcome.FAIL in outcomes:
        return OverallOutcome.NOT_QUALIFIED
    if CriterionOutcome.INSUFFICIENT_DATA in outcomes:
        return OverallOutcome.REVIEW_REQUIRED
    return OverallOutcome.QUALIFIED
