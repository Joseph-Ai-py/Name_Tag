from __future__ import annotations

from typing import Any
from uuid import uuid4

from models import BrandDNA, BrandIntegrityReport, DecisionTrace, IntegrityIssue


def _unwrap(data: Any, key: str) -> dict[str, Any]:
	if isinstance(data, dict) and isinstance(data.get(key), dict):
		return data[key]
	return data if isinstance(data, dict) else {}


def build_brand_dna(
	brand_info: dict[str, Any] | None,
	data_a: dict[str, Any] | None,
	data_b: dict[str, Any] | None,
	data_c: dict[str, Any] | None,
	data_de: dict[str, Any] | None,
	) -> dict[str, Any]:
	brand = brand_info or {}
	a = _unwrap(data_a, "data_a")
	b = _unwrap(data_b, "data_b")
	c = _unwrap(data_c, "data_c")
	de = _unwrap(data_de, "data_de")
	philosophy = a.get("brand_philosophy", {})
	essence = a.get("brand_essence", {})
	identity = a.get("core_identity", {})
	positioning = a.get("positioning", {})
	promise = a.get("unbreakable_brand_promise", {})
	persona = b.get("primary_persona", {})
	journey = b.get("customer_journey_map", [])
	visual_mood = c.get("visual_mood_guide", {})

	dna = BrandDNA(
		foundation={
			"brand_name": brand.get("brand_name", ""),
			"brand_name_en": brand.get("brand_name_en", ""),
			"meaning": brand.get("name_meaning", ""),
			"slogan": brand.get("slogan", ""),
		},
		why={
			"philosophy": philosophy,
			"essence": essence,
			"mission": identity.get("mission", ""),
			"vision": identity.get("vision", ""),
			"core_values": identity.get("core_values", []),
		},
		who={
			"target": b.get("core_target_group", {}),
			"persona": persona,
			"customer_journey": journey,
		},
		promise=promise,
		position=positioning,
		voice={
			"tone": visual_mood.get("mood_keywords", []),
			"language_rules": a.get("slogan_expansion", {}),
		},
		visual={
			"colors": c.get("color_palette", []),
			"typography": c.get("typography", {}),
			"mood": visual_mood,
			"design_principles": c.get("design_principles", {}),
			"logo": de.get("logo_identity", {}),
			"character": de.get("character_guide", {}),
		},
		behavior={
			"do": visual_mood.get("photography_do", []),
			"dont": visual_mood.get("photography_dont", []),
			"customer_experience_rules": promise.get("proof_of_promise", []),
		},
		business={
			"customer_swot": b.get("customer_swot", {}),
			"business_model": b.get("business_model", {}),
		},
	)
	return dna.model_dump()


def build_trace(
	stage: str,
	decision_type: str,
	user_input: str,
	ai_interpretation: str,
	brand_decision: str,
	rationale: str,
	question_ids: list[int] | None = None,
	status: str = "ai_derived",
) -> dict[str, Any]:
	return DecisionTrace(
		trace_id=str(uuid4()),
		stage=stage,
		decision_type=decision_type,
		user_input=user_input,
		ai_interpretation=ai_interpretation,
		brand_decision=brand_decision,
		rationale=rationale,
		source_question_ids=question_ids or [],
		status=status,
	).model_dump()


def check_brand_integrity(
	brand_info: dict[str, Any] | None,
	brand_dna: dict[str, Any] | None,
	outputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
	brand = brand_info or {}
	dna = brand_dna or {}
	issues: list[IntegrityIssue] = []
	brand_name = str(brand.get("brand_name", "")).strip()
	if brand_name and brand_name not in str(outputs or dna):
		issues.append(IntegrityIssue(
			severity="WARNING", category="brand_name", source_stage="integrity",
			field="foundation.brand_name", problematic_text=brand_name,
			reason="Canonical 결과에 확정 브랜드명이 충분히 나타나지 않습니다.",
			suggested_fix="해당 필드를 확정 브랜드명 기준으로 재검토하세요.",
		))

	contamination_terms = ["숲결", "폐플라스틱", "업사이클링", "자연 친화"]
	text = str(outputs or {})
	for term in contamination_terms:
		if term in text and term not in str(dna.get("foundation", {})):
			issues.append(IntegrityIssue(
				severity="FAIL", category="cross_brand_contamination", source_stage="integrity",
				field="outputs", problematic_text=term,
				reason="현재 Brand DNA에 근거하지 않은 오염 의심 문구입니다.",
				suggested_fix="문제가 발생한 필드만 현재 Brand DNA 기준으로 재생성하세요.",
			))

	status = "FAIL" if any(i.severity == "FAIL" for i in issues) else "WARNING" if issues else "PASS"
	return BrandIntegrityReport(status=status, issues=issues).model_dump()