from __future__ import annotations

from typing import Any

from gemini_client import request_gemini_text_flash_lite, request_gemini_with_schema
from models import BrandInfo, CResponseSchema, CandidatesResponse, InterviewResponseSchema
from prompts import get_C0_visual_interview_prompt, get_C1_visual_identity_prompt
from utils import normalize_candidates


def generate_c_interview_questions(brand_info: BrandInfo) -> dict[str, Any]:
	return request_gemini_with_schema(
		get_C0_visual_interview_prompt(brand_info.model_dump()),
		schema=InterviewResponseSchema,
	)


def generate_section_c(
	brand_info: BrandInfo,
	interview_data_a: str,
	interview_data_b: str,
	interview_data_c: str,
) -> dict[str, Any]:
	brand = brand_info.model_dump()
	previous_context = f"{interview_data_a} + {interview_data_b}"
	result = request_gemini_with_schema(
		get_C1_visual_identity_prompt(brand, previous_context, interview_data_c),
		schema=CResponseSchema,
	)
	return {"data_c": result}


def regenerate_c_field(brand_info: BrandInfo, context: dict[str, Any], target: str) -> dict[str, Any]:
	prompt = (
		f"Produce 3 alternative short values for `{target}` based on brand info {brand_info.model_dump()} "
		f"and context {context}. Return JSON only: {{\"candidates\": [..]}}"
	)
	result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_c.re-generate", "target": target})
	try:
		candidates = normalize_candidates(result)
		validated = CandidatesResponse(candidates=candidates)
		return {"target": target, "result": validated.model_dump()}
	except Exception:
		return {"target": target, "result": {"candidates": []}}

