import os
from typing import Any

from google import genai
from google.genai import types

from utils.parser import extract_json

SYSTEM_PROMPT = """당신은 전문 브랜드 디렉터입니다.
사용자의 정보를 바탕으로 초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다.
반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."""


def build_user_prompt(business_type: str, vibes: list[str], target: str, keywords: str) -> str:
    return f"""업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

아래 JSON 형식으로만 응답하세요:

{{
  "brands": [
    {{
      "name": "브랜드명",
      "meaning": "이름의 의미와 어원 1-2문장",
      "story": "고객 감성을 자극하는 스토리 2-3문장",
      "slogan": "핵심 슬로건 10단어 이내"
    }},
    {{ "name": "두번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }},
    {{ "name": "세번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }}
  ],
  "typography": {{
    "korean": "추천 한글 폰트명 (나눔명조, 프리텐다드, 고도체 등)",
    "english": "추천 영문 폰트명 (Playfair Display, DM Sans 등)",
    "reason": "선택 이유 2문장"
  }},
  "character": {{
    "name": "캐릭터 이름",
    "concept": "컨셉 한 줄",
    "personality": "성격 특징 3가지, 쉼표로 구분",
    "visual": "외형 묘사 2-3문장"
  }}
}}"""


def _get_model() -> tuple[genai.Client, str]:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()
    client = genai.Client(api_key=api_key)
    return client, model_name


def generate_brand_identity(
    business_type: str,
    vibes: list[str],
    target: str,
    keywords: str = "",
) -> dict[str, Any]:
    client, model_name = _get_model()
    response = client.models.generate_content(
        model=model_name,
        contents=build_user_prompt(business_type, vibes, target, keywords),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    raw_text = response.text or ""

    result = extract_json(raw_text)
    if result is None:
        raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_text[:500]}")

    required_keys = {"brands", "typography", "character"}
    if not required_keys.issubset(result.keys()):
        missing = required_keys - set(result.keys())
        raise ValueError(f"응답에 필수 키가 없습니다: {missing}")

    return result
