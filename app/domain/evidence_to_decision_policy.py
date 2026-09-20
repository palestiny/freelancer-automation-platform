from dataclasses import dataclass
from enum import Enum


class DecisionSupportOutcome(str, Enum):
    SUPPORTS = "supports"
    DOES_NOT_SUPPORT = "does_not_support"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    POLICY_INAPPLICABLE = "policy_inapplicable"


@dataclass(frozen=True)
class EvidenceToDecisionPolicy:
    policy_id: str
    version: str
    minimum_evidence_quality: float = 60
    require_statistical_difference: bool = False

    def __post_init__(self) -> None:
        if not self.policy_id.strip() or not self.version.strip():
            raise ValueError("policy_id and version cannot be empty")
        if not 0 <= self.minimum_evidence_quality <= 100:
            raise ValueError("minimum_evidence_quality must be between 0 and 100")
        if not isinstance(self.require_statistical_difference, bool):
            raise TypeError("require_statistical_difference must be a bool")


@dataclass(frozen=True)
class EvidenceDecisionSupport:
    outcome: DecisionSupportOutcome
    policy: EvidenceToDecisionPolicy

    @property
    def policy_id(self) -> str:
        return self.policy.policy_id

    @property
    def policy_version(self) -> str:
        return self.policy.version


def evaluate_evidence_to_decision(
    *,
    evidence_eligible: bool,
    evidence_quality: float,
    statistical_difference_detected: bool | None,
    policy: EvidenceToDecisionPolicy,
) -> EvidenceDecisionSupport:
    if not 0 <= evidence_quality <= 100:
        raise ValueError("evidence_quality must be between 0 and 100")
    if not isinstance(evidence_eligible, bool):
        raise TypeError("evidence_eligible must be a bool")
    if statistical_difference_detected is not None and not isinstance(
        statistical_difference_detected, bool
    ):
        raise TypeError("statistical_difference_detected must be a bool or None")

    if not evidence_eligible or evidence_quality < policy.minimum_evidence_quality:
        return EvidenceDecisionSupport(
            outcome=DecisionSupportOutcome.INSUFFICIENT_EVIDENCE,
            policy=policy,
        )

    if policy.require_statistical_difference:
        if statistical_difference_detected is None:
            return EvidenceDecisionSupport(
                outcome=DecisionSupportOutcome.POLICY_INAPPLICABLE,
                policy=policy,
            )
        if not statistical_difference_detected:
            return EvidenceDecisionSupport(
                outcome=DecisionSupportOutcome.DOES_NOT_SUPPORT,
                policy=policy,
            )

    return EvidenceDecisionSupport(
        outcome=DecisionSupportOutcome.SUPPORTS,
        policy=policy,
    )
