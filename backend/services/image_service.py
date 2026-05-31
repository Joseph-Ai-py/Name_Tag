from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from services.gemini_service import request_gemini_image

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"


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


def generate_logo_image(brand_name: str, de_section_data: dict) -> str | None:
    _log_image_request("logo", brand_name, de_section_data)
    concept = de_section_data.get("logo_identity", {}).get("concept", {})
    direction_text = concept.get("direction_text", "모던하고 심플한 워드마크 또는 심볼 형태")
    prompt = f"""당신은 세계적인 수준의 브랜드 아이덴티티(BI) 전문 디자이너입니다.
다음 지시사항에 따라 브랜드 로고를 완벽하게 디자인해 주세요.

[브랜드명]: {brand_name}
[디자인 핵심 방향성]: {direction_text}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 3D 효과, 그림자, 그라데이션, 광택이 전혀 없는 완벽하게 플랫(Flat)한 2D 벡터 스타일.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경. 투명도나 다른 배경 요소 절대 금지.
- 디테일: 복잡한 스케치나 스머지(번짐) 효과 없이, 선명하고 또렷한 가장자리(Crisp edges) 유지.
- 텍스트 제어: '{brand_name}' 외에 의미를 알 수 없는 이상한 AI 문자나 기호가 절대 포함되지 않도록 할 것.
- 목적: 전문 브랜딩 에이전시의 포트폴리오에 들어갈 법한 세련되고 미니멀한 마스터 로고."""

    image_data = request_gemini_image(prompt)
    if not image_data:
        print(f"[DEBUG] logo image generation failed - brand={brand_name}")
        return None
    saved_path = _save_image(image_data, "logos", "logo", brand_name)
    print(f"[DEBUG] logo image generation complete - brand={brand_name}, path={saved_path}")
    return saved_path


def generate_character_image(brand_name: str, de_section_data: dict) -> str | None:
    _log_image_request("character", brand_name, de_section_data)
    character_intro = de_section_data.get("character_guide", {}).get("intro", {})
    char_name = character_intro.get("name", "마스코트")
    char_appearance = character_intro.get("appearance", "브랜드 무드에 맞는 귀여운 마스코트")
    prompt = f"""당신은 세계적인 수준의 브랜드 캐릭터(마스코트) 전문 일러스트레이터입니다.
다음 지시사항에 따라 브랜드를 대변할 매력적인 캐릭터를 디자인해 주세요.

[브랜드명]: {brand_name}
[캐릭터 이름]: {char_name}
[캐릭터 외형 묘사]: {char_appearance}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 브랜드 로고와 시각적 일관성을 갖춘 깔끔한 2D 벡터 일러스트레이션.
- 구도: 캐릭터의 전신이나 상반신이 중앙에 명확하게 배치된 프로필 샷.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경.
- 텍스트 제어: 이미지 안에 어떤 텍스트나 글자도 포함하지 말 것."""

    image_data = request_gemini_image(prompt)
    if not image_data:
        print(f"[DEBUG] character image generation failed - brand={brand_name}")
        return None
    saved_path = _save_image(image_data, "characters", "char", brand_name)
    print(f"[DEBUG] character image generation complete - brand={brand_name}, path={saved_path}")
    return saved_path