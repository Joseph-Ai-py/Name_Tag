from __future__ import annotations

from typing import Any

from gemini_client import request_gemini_text_flash_lite, request_gemini_with_schema
from image_service import generate_character_image, generate_logo_image
from models import BrandInfo, CResponseSchema, CandidatesResponse, DEResponseSchema, InterviewResponseSchema
from prompts import get_DE_identity_prompt, get_DE_interview_prompt
from utils import normalize_candidates


def generate_de_interview_questions(brand_info: BrandInfo, interview_data_c: str) -> dict[str, Any]:
	return request_gemini_with_schema(
		get_DE_interview_prompt(brand_info.model_dump(), interview_data_c),
		schema=InterviewResponseSchema,
	)


def generate_section_de(
	brand_info: BrandInfo,
	data_c: dict[str, Any],
	interview_data_a: str,
	interview_data_b: str,
	interview_data_c: str,
	interview_data_de: str,
) -> dict[str, Any]:
	_ = CResponseSchema(**data_c)
	brand = brand_info.model_dump()
	previous_context = f"{interview_data_a} + {interview_data_b} + {interview_data_c}"

	result = request_gemini_with_schema(
		get_DE_identity_prompt(brand, data_c, previous_context, interview_data_de),
		schema=DEResponseSchema,
	)

	logo_path = generate_logo_image(
		brand_name=brand["brand_name"],
		de_section_data=result,
		brand_info=brand,
		data_c=data_c,
		deepdive_answers_text=interview_data_de,
	)
	char_path = generate_character_image(
		brand_name=brand["brand_name"],
		de_section_data=result,
		brand_info=brand,
		data_c=data_c,
		deepdive_answers_text=interview_data_de,
	)

	result["logo_path"] = logo_path
	result["char_path"] = char_path
	return {"data_de": result}


def generate_logo_only(
	brand_info: BrandInfo,
	data_c: dict[str, Any],
	interview_data_a: str,
	interview_data_b: str,
	interview_data_c: str,
	interview_data_de: str,
) -> dict[str, Any]:
	_ = CResponseSchema(**data_c)
	brand = brand_info.model_dump()
	previous_context = f"{interview_data_a} + {interview_data_b} + {interview_data_c}"
	result = request_gemini_with_schema(
		get_DE_identity_prompt(brand, data_c, previous_context, interview_data_de),
		schema=DEResponseSchema,	
	)

	logo_path = generate_logo_image(
		brand_name=brand["brand_name"],
		de_section_data=result,
		brand_info=brand,
		data_c=data_c,
		deepdive_answers_text=interview_data_de,
	)
	result["logo_path"] = logo_path
	return {"logo_path": logo_path, "data_de": result}


def generate_character_only(
	brand_info: BrandInfo,
	data_c: dict[str, Any],
	interview_data_a: str,
	interview_data_b: str,
	interview_data_c: str,
	interview_data_de: str,
) -> dict[str, Any]:
	_ = CResponseSchema(**data_c)
	brand = brand_info.model_dump()
	previous_context = f"{interview_data_a} + {interview_data_b} + {interview_data_c}"
	result = request_gemini_with_schema(
		get_DE_identity_prompt(brand, data_c, previous_context, interview_data_de),
		schema=DEResponseSchema,
	)

	char_path = generate_character_image(
		brand_name=brand["brand_name"],
		de_section_data=result,
		brand_info=brand,
		data_c=data_c,
		deepdive_answers_text=interview_data_de,
	)
	result["char_path"] = char_path
	return {"char_path": char_path, "data_de": result}


def regenerate_de_field(brand_info: BrandInfo, context: dict[str, Any], target: str) -> dict[str, Any]:
	prompt = (
		f"Produce 3 alternative short values for `{target}` based on brand info {brand_info.model_dump()} "
		f"and context {context}. Return JSON only: {{\"candidates\": [..]}}"
	)
	result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_de.re-generate", "target": target})
	try:
		candidates = normalize_candidates(result)
		validated = CandidatesResponse(candidates=candidates)
		return {"target": target, "result": validated.model_dump()}
	except Exception:
		return {"target": target, "result": {"candidates": []}}

