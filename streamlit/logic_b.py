from __future__ import annotations

from typing import Any

from gemini_client import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from models import BrandInfo, CandidatesResponse, InterviewResponseSchema
from prompts import get_B1_persona_prompt, get_B2_journey_prompt, get_B_interview_prompt
from utils import normalize_candidates


def generate_b_interview_questions(brand_info: BrandInfo) -> dict[str, Any]:
	return request_gemini_with_schema(
		get_B_interview_prompt(brand_info.model_dump()),
		schema=InterviewResponseSchema,
	)


def generate_section_b(brand_info: BrandInfo, interview_data_a: str, interview_data_b: str) -> dict[str, Any]:
	brand = brand_info.model_dump()
	b1 = request_gemini_text(get_B1_persona_prompt(brand, interview_data_a, interview_data_b))
	b2 = request_gemini_text(get_B2_journey_prompt(brand, interview_data_a, interview_data_b))

	merged: dict[str, Any] = {}
	for part in [b1, b2]:
		if isinstance(part, dict):
			merged.update(part)
	return {"data_b": merged}


def regenerate_b_field(brand_info: BrandInfo, context: dict[str, Any], target: str) -> dict[str, Any]:
	prompt = (
		f"Produce 3 alternative short values for `{target}` based on brand info {brand_info.model_dump()} "
		f"and context {context}. Return JSON only: {{\"candidates\": [..]}}"
	)
	result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_b.re-generate", "target": target})
	try:
		candidates = normalize_candidates(result)
		validated = CandidatesResponse(candidates=candidates)
		return {"target": target, "result": validated.model_dump()}
	except Exception:
		return {"target": target, "result": {"candidates": []}}

