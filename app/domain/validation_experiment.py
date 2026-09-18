from dataclasses import dataclass
from enum import Enum


class ExperimentStatus(Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ExperimentOutcome(Enum):
    VALIDATED = "VALIDATED"
    INVALIDATED = "INVALIDATED"
    INCONCLUSIVE = "INCONCLUSIVE"


class ExperimentDecision(Enum):
    PROMOTE = "PROMOTE"
    REJECT = "REJECT"
    CONTINUE_TESTING = "CONTINUE_TESTING"


@dataclass(frozen=True)
class ValidationExperiment:
    id: str
    hypothesis: str
    objective: str
    success_criterion: str
    variants: tuple[str, ...] = ()
    budget_limit: float = 0.0
    status: ExperimentStatus = ExperimentStatus.DRAFT

    def __post_init__(self) -> None:
        for field_name in ("id", "hypothesis", "objective", "success_criterion"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")

        if any(not variant.strip() for variant in self.variants):
            raise ValueError("variants cannot contain empty values")

        if len(set(self.variants)) != len(self.variants):
            raise ValueError("variants must be unique")

        if self.budget_limit < 0:
            raise ValueError("budget_limit cannot be negative")

    def plan(self) -> "ValidationExperiment":
        if self.status is not ExperimentStatus.DRAFT:
            raise ValueError("Experiment can only be planned from DRAFT")
        return self._with_status(ExperimentStatus.PLANNED)

    def start(self) -> "ValidationExperiment":
        if self.status is not ExperimentStatus.PLANNED:
            raise ValueError("Experiment can only be started from PLANNED")
        return self._with_status(ExperimentStatus.RUNNING)

    def complete(self) -> "ValidationExperiment":
        if self.status is not ExperimentStatus.RUNNING:
            raise ValueError("Experiment can only be completed from RUNNING")
        return self._with_status(ExperimentStatus.COMPLETED)

    def cancel(self) -> "ValidationExperiment":
        if self.status not in (ExperimentStatus.DRAFT, ExperimentStatus.PLANNED, ExperimentStatus.RUNNING):
            raise ValueError("Only active experiments can be cancelled")
        return self._with_status(ExperimentStatus.CANCELLED)

    def _with_status(self, status: ExperimentStatus) -> "ValidationExperiment":
        return ValidationExperiment(
            id=self.id,
            hypothesis=self.hypothesis,
            objective=self.objective,
            success_criterion=self.success_criterion,
            variants=self.variants,
            budget_limit=self.budget_limit,
            status=status,
        )


@dataclass(frozen=True)
class ExperimentResult:
    experiment_id: str
    outcome: ExperimentOutcome
    observed_measurement: str
    success_criterion_met: bool
    evidence_statement: str
    decision: ExperimentDecision

    def __post_init__(self) -> None:
        for field_name in ("experiment_id", "observed_measurement", "evidence_statement"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")

        if self.outcome is ExperimentOutcome.VALIDATED and not self.success_criterion_met:
            raise ValueError("VALIDATED result requires the success criterion to be met")

        if self.outcome is ExperimentOutcome.INVALIDATED and self.success_criterion_met:
            raise ValueError("INVALIDATED result cannot have the success criterion met")

        if self.outcome is ExperimentOutcome.INCONCLUSIVE and self.decision is not ExperimentDecision.CONTINUE_TESTING:
            raise ValueError("INCONCLUSIVE result must continue testing")
