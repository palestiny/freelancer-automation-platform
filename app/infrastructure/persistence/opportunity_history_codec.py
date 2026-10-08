"""Versioned, fail-closed canonical serialization for opportunity history V1."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, TypeVar

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
from app.domain.client_project_risk import (
    RiskComparisonOperator,
    RiskConstraint,
    RiskScope,
)
from app.domain.economic_fit import (
    EconomicComparisonOperator,
    EconomicConstraint,
    EconomicMetric,
)
from app.domain.eligibility import EligibilityConstraint
from app.domain.estimated_effort import EffortConstraint
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluation,
    OverallOutcome,
)
from app.domain.opportunity_prioritization import (
    CriterionEvidenceSnapshot,
    OpportunityPriorityDecision,
    PrioritizationOutcome,
    PrioritizationPolicy,
    PriorityTierRule,
)
from app.domain.opportunity_type import OpportunityType
from app.domain.requirement_fit import CapabilityRequirement
from app.domain.success_confidence import (
    SuccessComparisonOperator,
    SuccessCondition,
    SuccessConditionScope,
)

T = TypeVar("T")


class UnsupportedCanonicalValue(ValueError):
    """Raised when a value cannot be represented under the V1 codec contract."""


# Explicit manifests are deliberately independent of dataclass reflection.
_RECORD_TYPES: dict[str, tuple[type, tuple[str, ...]]] = {
    "opportunity_decision_result": (OpportunityDecisionResult, (
        "opportunity_ref", "evaluation_ref", "evaluation", "priority_decision",
    )),
    "opportunity": (Opportunity, (
        "source_platform", "source_opportunity_id", "title", "description",
        "project_type", "required_capabilities", "budget_min", "budget_max",
        "budget_currency", "pricing_model", "status", "source_url",
        "client_external_id", "client_country", "opportunity_type",
    )),
    "evaluation_policy": (EvaluationPolicy, (
        "policy_id", "policy_version", "required_criteria",
        "eligibility_constraints", "requirement_fit_requirements",
        "estimated_effort_constraints", "economic_fit_constraints",
        "client_project_risk_constraints", "success_confidence_conditions",
    )),
    "criterion_evaluation": (CriterionEvaluation, (
        "policy_id", "policy_version", "criterion_id", "outcome",
        "evidence_refs", "missing_evidence", "uncertainty", "rationale",
    )),
    "opportunity_evaluation": (OpportunityEvaluation, (
        "policy_id", "policy_version", "criteria", "overall_outcome",
    )),
    "prioritization_policy": (PrioritizationPolicy, (
        "policy_id", "policy_version", "mandatory_evidence_refs", "tier_rules",
    )),
    "priority_tier_rule": (PriorityTierRule, (
        "rule_id", "tier_id", "required_evidence_refs",
    )),
    "criterion_evidence_snapshot": (CriterionEvidenceSnapshot, (
        "criterion_id", "outcome", "evidence_refs", "missing_evidence",
        "uncertainty", "rationale",
    )),
    "opportunity_priority_decision": (OpportunityPriorityDecision, (
        "opportunity_ref", "evaluation_ref", "evaluation_policy_id",
        "evaluation_policy_version", "prioritization_policy_id",
        "prioritization_policy_version", "outcome", "tier_id",
        "matched_rule_ids", "reasons", "evidence_refs", "criterion_snapshots",
        "evaluated_at",
    )),
    "eligibility_constraint": (EligibilityConstraint, (
        "constraint_id", "evidence_refs", "allowed_values",
    )),
    "capability_requirement": (CapabilityRequirement, (
        "requirement_id", "capability_id", "evidence_refs",
    )),
    "effort_constraint": (EffortConstraint, (
        "constraint_id", "maximum_value", "unit", "evidence_refs",
        "required_scope_refs",
    )),
    "economic_constraint": (EconomicConstraint, (
        "constraint_id", "metric", "operator", "threshold", "unit", "currency",
        "evidence_refs",
    )),
    "risk_constraint": (RiskConstraint, (
        "constraint_id", "scope", "signal", "operator", "expected_values",
        "evidence_refs",
    )),
    "success_condition": (SuccessCondition, (
        "condition_id", "scope", "signal", "operator", "expected_values",
        "evidence_refs",
    )),
}

_ENUM_TYPES: dict[str, type[Enum]] = {
    cls.__name__: cls
    for cls in (
        CriterionId,
        CriterionOutcome,
        OverallOutcome,
        PrioritizationOutcome,
        OpportunityType,
        EconomicMetric,
        EconomicComparisonOperator,
        RiskScope,
        RiskComparisonOperator,
        SuccessConditionScope,
        SuccessComparisonOperator,
    )
}
_TYPE_NAMES = {cls: name for name, (cls, _) in _RECORD_TYPES.items()}
_ENUM_NAMES = {cls: name for name, cls in _ENUM_TYPES.items()}


class OpportunityHistoryCodecV1:
    """Canonical UTF-8 JSON codec with explicit type and schema tags."""

    schema_version = 1

    def dumps(self, value: Any) -> bytes:
        encoded = self._encode(value)
        return json.dumps(
            encoded,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")

    def loads(
        self,
        payload: bytes | str,
        *,
        expected_type: type[T] | None = None,
        schema_version: int = 1,
    ) -> T | Any:
        if schema_version != self.schema_version:
            raise UnsupportedCanonicalValue(
                f"unsupported requested schema version: {schema_version}"
            )
        try:
            raw = json.loads(payload.decode("utf-8") if isinstance(payload, bytes) else payload)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
            raise UnsupportedCanonicalValue("invalid canonical JSON payload") from exc
        restored = self._decode(raw)
        if expected_type is not None and type(restored) is not expected_type:
            raise UnsupportedCanonicalValue(
                f"decoded type {type(restored).__name__} does not match "
                f"{expected_type.__name__}"
            )
        return restored

    def _encode(self, value: Any) -> dict[str, Any]:
        if value is None:
            return {"$type": "none"}
        if type(value) is bool:
            return {"$type": "bool", "value": value}
        if type(value) is int:
            return {"$type": "int", "value": str(value)}
        if type(value) is float:
            if not math.isfinite(value):
                raise UnsupportedCanonicalValue("non-finite floats are not supported")
            return {"$type": "float", "value": value.hex()}
        if isinstance(value, Enum):
            enum_name = _ENUM_NAMES.get(type(value))
            if enum_name is None:
                raise UnsupportedCanonicalValue(f"unregistered enum type: {type(value).__name__}")
            return {"$type": "enum", "enum": enum_name, "value": value.value}
        if isinstance(value, str):
            return {"$type": "str", "value": value}
        if isinstance(value, Decimal):
            if not value.is_finite():
                raise UnsupportedCanonicalValue("non-finite Decimal values are not supported")
            normalized = "0" if value == 0 else format(value.normalize(), "f")
            return {"$type": "decimal", "value": normalized}
        if isinstance(value, datetime):
            if value.tzinfo is None or value.utcoffset() is None:
                raise UnsupportedCanonicalValue("naive datetime is not supported")
            normalized = value.astimezone(timezone.utc).isoformat(timespec="microseconds")
            return {"$type": "datetime", "value": normalized.replace("+00:00", "Z")}
        if isinstance(value, tuple):
            return {"$type": "tuple", "items": [self._encode(item) for item in value]}
        if isinstance(value, list):
            return {"$type": "list", "items": [self._encode(item) for item in value]}
        if isinstance(value, frozenset):
            items = [self._encode(item) for item in value]
            items.sort(key=self._json_sort_key)
            return {"$type": "frozenset", "items": items}
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise UnsupportedCanonicalValue("mapping keys must be strings")
            return {
                "$type": "mapping",
                "items": [
                    [key, self._encode(value[key])] for key in sorted(value)
                ],
            }
        value_type = type(value)
        type_name = _TYPE_NAMES.get(value_type)
        if type_name is None:
            raise UnsupportedCanonicalValue(f"unregistered type: {value_type.__name__}")
        _, manifest = _RECORD_TYPES[type_name]
        return {
            "$type": "record",
            "record_type": type_name,
            "schema_version": self.schema_version,
            "fields": {name: self._encode(getattr(value, name)) for name in manifest},
        }

    def _decode(self, value: Any) -> Any:
        if not isinstance(value, dict) or not isinstance(value.get("$type"), str):
            raise UnsupportedCanonicalValue("invalid typed value envelope")
        tag = value["$type"]
        if tag == "none":
            return None
        if tag == "bool" and type(value.get("value")) is bool:
            return value["value"]
        if tag == "int":
            try:
                return int(value["value"])
            except (KeyError, TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid integer encoding") from exc
        if tag == "float":
            try:
                result = float.fromhex(value["value"])
            except (KeyError, TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid float encoding") from exc
            if not math.isfinite(result):
                raise UnsupportedCanonicalValue("non-finite float encoding")
            return result
        if tag == "str" and isinstance(value.get("value"), str):
            return value["value"]
        if tag == "decimal":
            try:
                result = Decimal(value["value"])
            except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid Decimal encoding") from exc
            if not result.is_finite():
                raise UnsupportedCanonicalValue("non-finite Decimal encoding")
            return result
        if tag == "datetime":
            try:
                encoded = value["value"]
                if not isinstance(encoded, str) or not encoded.endswith("Z"):
                    raise ValueError("datetime must end in Z")
                result = datetime.fromisoformat(encoded[:-1] + "+00:00")
            except (KeyError, TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid datetime encoding") from exc
            return result
        if tag == "enum":
            enum_type = _ENUM_TYPES.get(value.get("enum"))
            if enum_type is None:
                raise UnsupportedCanonicalValue("unknown enum type")
            try:
                return enum_type(value["value"])
            except (KeyError, TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid enum value") from exc
        if tag in ("tuple", "list", "frozenset"):
            items = value.get("items")
            if not isinstance(items, list):
                raise UnsupportedCanonicalValue("collection items must be a list")
            decoded = [self._decode(item) for item in items]
            if tag == "tuple":
                return tuple(decoded)
            if tag == "list":
                return decoded
            try:
                return frozenset(decoded)
            except TypeError as exc:
                raise UnsupportedCanonicalValue("unhashable frozenset member") from exc
        if tag == "mapping":
            items = value.get("items")
            if not isinstance(items, list):
                raise UnsupportedCanonicalValue("mapping items must be a list")
            result: dict[str, Any] = {}
            for pair in items:
                if not isinstance(pair, list) or len(pair) != 2 or not isinstance(pair[0], str):
                    raise UnsupportedCanonicalValue("invalid mapping entry")
                if pair[0] in result:
                    raise UnsupportedCanonicalValue("duplicate mapping key")
                result[pair[0]] = self._decode(pair[1])
            return result
        if tag == "record":
            type_name = value.get("record_type")
            entry = _RECORD_TYPES.get(type_name)
            if entry is None:
                raise UnsupportedCanonicalValue("unknown record type")
            if value.get("schema_version") != self.schema_version:
                raise UnsupportedCanonicalValue("unsupported record schema version")
            cls, manifest = entry
            fields = value.get("fields")
            if not isinstance(fields, dict) or set(fields) != set(manifest):
                raise UnsupportedCanonicalValue("record fields do not match V1 manifest")
            decoded = {name: self._decode(fields[name]) for name in manifest}
            try:
                return cls(**decoded)
            except (TypeError, ValueError) as exc:
                raise UnsupportedCanonicalValue("invalid domain record payload") from exc
        raise UnsupportedCanonicalValue(f"unknown canonical type tag: {tag}")

    @staticmethod
    def _json_sort_key(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
