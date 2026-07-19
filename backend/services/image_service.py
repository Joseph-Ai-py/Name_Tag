from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from services.gemini_service import request_gemini_image
from prompts.nametag_prompts import get_logo_image_prompt, get_character_image_prompt

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"


def _save_image(image_data: bytes, subdir: str, filename_prefix: str, brand_name: str) -> str:
    target_dir = ASSETS_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_brand_name = brand_name.replace(" ", "_")
    file_path = target_dir / f"{filename_prefix}_{safe_brand_name}_{timestamp}.png"
    file_path.write_bytes(image_data)
    print(f"[DEBUG] image saved: {file_path.resolve()}")
    return str(file_path.resolve())


def _log_image_request(kind: str, brand_name: str, payload: dict[str, Any]) -> None:
    print(
        f"[DEBUG] {kind} image request - brand={brand_name}, keys={list(payload.keys())}, "
        f"concept_keys={list(payload.get('logo_identity', {}).get('concept', {}).keys()) if kind == 'logo' else list(payload.get('character_guide', {}).keys())}"
    )


def generate_logo_image(brand_name: str, de_section_data: dict, brand_info: dict, data_c: dict, deepdive_answers_text: str) -> str | None:
    # 로깅 및 로직 처리
    _log_image_request("logo", brand_name, de_section_data)
    
    # 로고 기획 데이터 추출
    concept = de_section_data.get("logo_identity", {}).get("concept", {})
    direction_text = concept.get("direction_text", "모던하고 심플한 워드마크 또는 심볼 형태")
    
    # 프롬프트 함수 호출
    prompt = get_logo_image_prompt(
        brand_name=brand_name,
        direction_text=direction_text,
        brand_info=brand_info,
        deepdive_answers_text=deepdive_answers_text,
        data_c=data_c
    )

    # 이미지 생성 요청
    image_data = request_gemini_image(prompt)
    if not image_data:
        print(f"[DEBUG] logo image generation failed - brand={brand_name}")
        return None
    saved_path = _save_image(image_data, "logos", "logo", brand_name)
    print(f"[DEBUG] logo image generation complete - brand={brand_name}, path={saved_path}")
    return saved_path


def generate_character_image(
    brand_name: str, 
    de_section_data: dict, 
    brand_info: dict, 
    data_c: dict, 
    deepdive_answers_text: str
) -> str | None:
    _log_image_request("character", brand_name, de_section_data)
    
    # 캐릭터 가이드 데이터 추출
    char_guide = de_section_data.get("character_guide", {})
    intro = char_guide.get("intro", {})
    reasoning = char_guide.get("reasoning", {})
    
    # 프롬프트 함수 호출
    prompt = get_character_image_prompt(
        brand_name=brand_name,
        char_name=intro.get("name", "마스코트"),
        char_appearance=intro.get("appearance", "매력적인 브랜드 캐릭터"),
        symbolic_value=intro.get("symbolic_value", "브랜드 상징"),
        emotional_connection=reasoning.get("emotional_connection", "고객과의 감정적 유대"),
        brand_info=brand_info,
        deepdive_answers_text=deepdive_answers_text,
        data_c=data_c
    )

    image_data = request_gemini_image(prompt)
    if not image_data:
        print(f"[DEBUG] character image generation failed - brand={brand_name}")
        return None
    saved_path = _save_image(image_data, "characters", "char", brand_name)
    print(f"[DEBUG] character image generation complete - brand={brand_name}, path={saved_path}")
    return saved_path