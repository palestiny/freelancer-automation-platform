from app.domain.controlled_experiment_evidence_package import (
    ExperimentEvidencePackageStatus,
    build_experiment_evidence_package,
)


def test_ready_experiment_with_statistical_result_is_packaged_without_winner_selection():
    result = build_experiment_evidence_package(
        experiment_id="exp-1",
        metric_name="conversion_rate",
        unit="percent",
        first_variant_id="control",
        second_variant_id="treatment",
        readiness_status="ready",
        descriptive_difference=2.5,
        statistical_status="applicable",
        rejects_null=True,
        observation_ids=("a", "b", "c", "d"),
    )

    assert result.status is ExperimentEvidencePackageStatus.REVIEW_READY
    assert result.descriptive_difference == 2.5
    assert result.statistical_difference_detected is True
    assert result.observation_ids == ("a", "b", "c", "d")
    assert result.selected_variant_id is None


def test_incomplete_readiness_blocks_review_package():
    result = build_experiment_evidence_package(
        experiment_id="exp-1",
        metric_name="conversion_rate",
        unit="percent",
        first_variant_id="control",
        second_variant_id="treatment",
        readiness_status="not_ready",
        descriptive_difference=2.5,
        statistical_status="applicable",
        rejects_null=True,
        observation_ids=("a", "b", "c", "d"),
    )
    assert result.status is ExperimentEvidencePackageStatus.NOT_REVIEW_READY


def test_inapplicable_statistical_result_remains_explicit():
    result = build_experiment_evidence_package(
        experiment_id="exp-1",
        metric_name="conversion_rate",
        unit="percent",
        first_variant_id="control",
        second_variant_id="treatment",
        readiness_status="ready",
        descriptive_difference=2.5,
        statistical_status="inapplicable",
        rejects_null=None,
        observation_ids=("a", "b", "c", "d"),
    )
    assert result.status is ExperimentEvidencePackageStatus.REVIEW_READY
    assert result.statistical_difference_detected is None


def test_duplicate_observation_lineage_is_rejected():
    try:
        build_experiment_evidence_package(
            experiment_id="exp-1",
            metric_name="conversion_rate",
            unit="percent",
            first_variant_id="control",
            second_variant_id="treatment",
            readiness_status="ready",
            descriptive_difference=2.5,
            statistical_status="applicable",
            rejects_null=True,
            observation_ids=("a", "a", "b", "c"),
        )
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("expected duplicate lineage rejection")
