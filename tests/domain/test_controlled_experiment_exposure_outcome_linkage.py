from datetime import datetime, timezone, timedelta

import pytest

from app.domain.controlled_experiment_exposure_outcome_linkage import (
    ExposureOutcomeLinkage,
)


def _times():
    exposed = datetime(2026, 9, 20, 10, tzinfo=timezone.utc)
    return exposed, exposed + timedelta(hours=2)


def test_valid_linkage_preserves_experiment_lineage():
    exposed, observed = _times()
    linkage = ExposureOutcomeLinkage(
        linkage_id="link-1",
        experiment_id="exp-1",
        assignment_id="assign-1",
        exposure_id="exposure-1",
        subject_id="subject-1",
        variant_id="variant-a",
        outcome_observation_id="outcome-1",
        exposed_at=exposed,
        observed_at=observed,
    )

    assert linkage.experiment_id == "exp-1"
    assert linkage.exposure_id == "exposure-1"
    assert linkage.outcome_observation_id == "outcome-1"


def test_outcome_cannot_precede_exposure():
    exposed, observed = _times()
    with pytest.raises(ValueError, match="observed_at"):
        ExposureOutcomeLinkage(
            linkage_id="link-1",
            experiment_id="exp-1",
            assignment_id="assign-1",
            exposure_id="exposure-1",
            subject_id="subject-1",
            variant_id="variant-a",
            outcome_observation_id="outcome-1",
            exposed_at=observed,
            observed_at=exposed,
        )


def test_naive_timestamps_are_rejected():
    exposed = datetime(2026, 9, 20, 10)
    observed = datetime(2026, 9, 20, 12)
    with pytest.raises(ValueError, match="timezone-aware"):
        ExposureOutcomeLinkage(
            linkage_id="link-1",
            experiment_id="exp-1",
            assignment_id="assign-1",
            exposure_id="exposure-1",
            subject_id="subject-1",
            variant_id="variant-a",
            outcome_observation_id="outcome-1",
            exposed_at=exposed,
            observed_at=observed,
        )
