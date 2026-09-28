from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import CriterionId


class EvidenceKind(str, Enum):
    FACT = "FACT"
    OBSERVATION = "OBSERVATION"
    ESTIMATE = "ESTIMATE"
    ASSUMPTION = "ASSUMPTION"
    HYPOTHESIS = "HYPOTHESIS"
    FORECAST = "FORECAST"
    EXPERIMENT_RESULT = "EXPERIMENT_RESULT"


class EvidenceQuality(str, Enum):
    PRESENT_AND_USABLE = "PRESENT_AND_USABLE"
    PRESENT_BUT_AMBIGUOUS = "PRESENT_BUT_AMBIGUOUS"
    PRESENT_BUT_STALE = "PRESENT_BUT_STALE"
    PRESENT_BUT_LOW_QUALITY = "PRESENT_BUT_LOW_QUALITY"
    MISSING = "MISSING"


class CriterionApplicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    kind: EvidenceKind
    value: Any
    provenance: str
    observed_at: datetime | None
    quality: EvidenceQuality
    derivation_refs: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_id, str) or not self.evidence_id.strip():
            raise ValueError("evidence_id must not be empty")
        if not isinstance(self.kind, EvidenceKind):
            raise TypeError("kind must be an EvidenceKind")
        if not isinstance(self.provenance, str) or not self.provenance.strip():
            raise ValueError("provenance must not be empty")
        if self.observed_at is not None and (
            self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None
        ):
            raise ValueError("observed_at must be timezone-aware")
        if not isinstance(self.quality, EvidenceQuality):
            raise TypeError("quality must be an EvidenceQuality")

        for name, values in (
            ("derivation_refs", self.derivation_refs),
            ("uncertainty", self.uncertainty),
        ):
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{name} must contain non-empty strings")

        if len(set(self.derivation_refs)) != len(self.derivation_refs):
            raise ValueError("derivation_refs must contain unique references")


@dataclass(frozen=True)
class EvaluationContext:
    subject: Opportunity
    evidence: tuple[Evidence, ...]
    evaluation_time: datetime
    applicability: Mapping[CriterionId, CriterionApplicability] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.subject, Opportunity):
            raise TypeError("subject must be an Opportunity")
        if not isinstance(self.evidence, tuple):
            raise TypeError("evidence must be a tuple")
        if any(not isinstance(item, Evidence) for item in self.evidence):
            raise TypeError("evidence must contain Evidence values")
        evidence_ids = [item.evidence_id for item in self.evidence]
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("evidence identities must be unique")

        if self.evaluation_time.tzinfo is None or self.evaluation_time.utcoffset() is None:
            raise ValueError("evaluation_time must be timezone-aware")

        if not isinstance(self.applicability, Mapping):
            raise TypeError("applicability must be a mapping")
        normalized_applicability: dict[CriterionId, CriterionApplicability] = {}
        for criterion_id, status in self.applicability.items():
            if not isinstance(criterion_id, CriterionId):
                raise TypeError("applicability keys must be CriterionId values")
            if not isinstance(status, CriterionApplicability):
                raise TypeError(
                    "applicability values must be CriterionApplicability values"
                )
            normalized_applicability[criterion_id] = status

        object.__setattr__(
            self,
            "applicability",
            MappingProxyType(normalized_applicability),
        )
