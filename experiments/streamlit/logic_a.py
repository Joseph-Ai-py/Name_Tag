from __future__ import annotations

from typing import Any

from gemini_client import request_gemini_text_flash_lite, request_gemini_with_schema
from models import A1ResponseSchema, A2ResponseSchema, A3ResponseSchema, BrandInfo, CandidatesResponse, InterviewResponseSchema
from prompts import (
	get_A1_philosophy_prompt,
	get_A2_story_prompt,
	get_A3_positioning_prompt,
	get_A_field_regen_prompt,
	get_A_interview_prompt,
)
from utils import normalize_candidates


def generate_a_interview_questions(brand_info: BrandInfo) -> dict[str, Any]:
	return request_gemini_with_schema(
		get_A_interview_prompt(brand_info.model_dump()),
		schema=InterviewResponseSchema,
	)


def generate_section_a(brand_info: BrandInfo, interview_data_a: str) -> dict[str, Any]:
	brand = brand_info.model_dump()
	a1 = request_gemini_with_schema(get_A1_philosophy_prompt(brand, interview_data_a), schema=A1ResponseSchema)
	a2 = request_gemini_with_schema(get_A2_story_prompt(brand, interview_data_a), schema=A2ResponseSchema)
	a3 = request_gemini_with_schema(get_A3_positioning_prompt(brand, interview_data_a), schema=A3ResponseSchema)

	merged: dict[str, Any] = {}
	for part in [a1, a2, a3]:
		merged.update(part)
	return {"data_a": merged}


def regenerate_a_field(brand_info: BrandInfo, context: dict[str, Any] | None, target: str) -> dict[str, Any]:
	prompt = get_A_field_regen_prompt(brand_info.model_dump(), target, context or {})
	result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_a.re-generate", "target": target})
	try:
		candidates = normalize_candidates(result)
		validated = CandidatesResponse(candidates=candidates)
		return {"target": target, "result": validated.model_dump()}
	except Exception:
		return {"target": target, "result": {"candidates": []}}

