from __future__ import annotations

from typing import Any

from gemini_client import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from models import BrandData, BrandInfo, CandidatesResponse, InterviewResponseSchema
from prompts import get_O_interview_prompt, get_O_mvb_prompt
from utils import normalize_candidates

VIBE_EN_MAP = {
    "모던": "modern, clean geometric, crisp lines, contemporary sans-serif",
    "미니멀": "minimal, lots of whitespace, monochrome, restrained, simple icon",
    "따뜻함": "warm cozy, soft rounded shapes, cream/beige/brown, friendly",
    "프리미엄": "premium sophisticated, dark palette with gold accents, refined serif",
    "자연": "natural organic, earthy greens and browns, leaf motifs, handmade texture",
    "테크": "tech futuristic, bold gradients, geometric, neon accent, digital",
    "클래식": "classic timeless, navy and gold, traditional serif, trustworthy",
    "캐주얼": "casual relaxed, approachable rounded sans-serif, bright everyday colors",
    "에너지틱": "energetic dynamic, vivid pop colors, motion shapes, bold and lively",
    "빈티지": "vintage retro, mustard/teal/orange, chunky typography, film grain",
    "힐링": "healing serene, spa-like, sage green and soft beige, peaceful breathing room",
    "아티스틱": "artistic creative, painterly illustration, hand-drawn texture, unique",
    "플레이풀": "playful cute, cartoon shapes, cheerful pastel pop, youthful fun",
    "다크": "dark intense, black and high contrast, grunge or sharp lettering",
    "스트릿": "street hip urban, graffiti influence, bold condensed type, city vibe",
    "한국·전통": "korean traditional, hanok architecture, dancheong colors, oriental calligraphy",
}

def build_base_prompt(brand_data: BrandData, core_prompt: str, brand_name: str = "브랜드명 미정") -> str:
    combined_vibes = []
    for vibe in brand_data.vibes:
        en_desc = VIBE_EN_MAP.get(vibe, "")
        if en_desc:
            combined_vibes.append(f"{vibe}({en_desc})")
        else:
            combined_vibes.append(vibe)
            
    vibe_str = ", ".join(combined_vibes) if combined_vibes else "없음"

    return f"""
[기본 입력 정보]
- 업종/서비스: {brand_data.business_type}
- 브랜드 감성: {vibe_str}
- 타겟 고객: {brand_data.target}
- 확정된 브랜드명: {brand_name}
- 추가 키워드: {brand_data.keywords or '없음'}
""" + core_prompt


def generate_o_interview_questions(brand_data: BrandData) -> dict[str, Any]:
	_ = brand_data
	return request_gemini_with_schema(get_O_interview_prompt(), schema=InterviewResponseSchema)


def generate_o_candidates(brand_data: BrandData, interview_text: str) -> dict[str, Any]:
	prompt = build_base_prompt(brand_data, get_O_mvb_prompt(interview_text))
	return request_gemini_text(prompt)


def apply_candidate_mix(candidates: list[dict[str, Any]], selection_map: dict[str, int]) -> BrandInfo:
	if len(candidates) < 4:
		raise ValueError("At least 4 candidates are required for mix-and-match.")

	name_idx = selection_map.get("name")
	meaning_idx = selection_map.get("meaning")
	slogan_idx = selection_map.get("slogan")
	story_idx = selection_map.get("story")
	color_idx = selection_map.get("color")

	if None in [name_idx, meaning_idx, slogan_idx, story_idx, color_idx]:
		raise ValueError("All selection keys (name/meaning/slogan/story/color) are required.")

	return BrandInfo(
		brand_name=candidates[name_idx]["brand_name"],
		brand_name_en=candidates[name_idx].get("brand_name_en", ""),
		name_meaning=candidates[meaning_idx]["name_meaning"],
		slogan=candidates[slogan_idx]["slogan"],
		story_summary=candidates[story_idx]["story_summary"],
		seed_color=candidates[color_idx]["seed_color"],
		seed_color_reason=candidates[color_idx]["seed_color_reason"],
	)


def regenerate_o_field(brand_data: BrandData, context: dict[str, Any], target: str) -> dict[str, Any]:
	prompt = (
		f"Produce 3 alternative short values for `{target}` based on brand info {brand_data.model_dump()} "
		f"and context {context}. Return JSON only: {{\"candidates\": [..]}}"
	)
	result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_o.re-generate", "target": target})
	try:
		candidates = normalize_candidates(result)
		validated = CandidatesResponse(candidates=candidates)
		return {"target": target, "result": validated.model_dump()}
	except Exception:
		return {"target": target, "result": {"candidates": []}}

