from __future__ import annotations

from typing import Any, Iterable


SYSTEM_PROMPT = """당신은 10년 경력의 브랜드 디렉터입니다.
초기 창업자에게 최소 브랜드(MVB: Minimum Viable Brand)를 제공하는 것이 목표입니다.
반드시 JSON형식으로만 출력하고 마크다운 코드블록이나 설명 텍스트를 절대 포함하지 마세요.
각 후보는 서로 완전히 다른 방향성과 감성을 가져야 합니다.

[🚨 최고 수준의 엄격한 제약 사항 - 위반 시 시스템 오류 발생 🚨]
1. 반드시 완벽한 JSON 형식으로만 출력하세요. 마크다운(```json)이나 부가 설명은 절대 금지합니다.
2. 프롬프트에서 제시한 JSON의 '최상위 Key(예: brand_philosophy, naming_expansion, color_palette, character_guide 등)'를 절대 생략하거나 지우지 마세요.
3. 데이터 구조를 평탄화(Flatten)하지 마세요. 반드시 요청한 중첩(Nested) 구조를 100% 그대로 유지해야 합니다.
4. 요청한 항목 중 단 하나라도 빼먹거나 중간에 답변을 종료하지 마세요. 모든 항목의 값을 꽉 채워서 응답해야 합니다.
"""


def _join_lines(lines: Iterable[str]) -> str:
    return "\n".join(lines)


def _brand_context(brand_data: dict[str, Any], selected_brand_name: str = "브랜드명 미정") -> str:
    return _join_lines(
        [
            "[기본 입력 정보]",
            f"- 업종/서비스: {brand_data.get('business_type', '')}",
            f"- 브랜드 감성: {', '.join(brand_data.get('vibes', []))}",
            f"- 타겟 고객: {brand_data.get('target', '')}",
            f"- 추가 키워드: {brand_data.get('keywords', '') or '없음'}",
            f"- 확정된 브랜드명: {selected_brand_name}",
        ]
    )


def get_brand_gallery_prompt(brand_data: dict[str, Any]) -> str:
    return f"""{_brand_context(brand_data)}

이 정보를 바탕으로 브랜드 초안 후보 3개를 생성하세요.
각 후보는 서로 다른 톤과 사용 맥락을 가져야 합니다.

반드시 아래 JSON 형식으로만 응답하세요:

{{
  "brands": [
    {{
      "name": "브랜드명 1",
      "meaning": "브랜드명 1의 의미와 어감",
      "story": "브랜드명 1의 탄생/스토리",
      "slogan": "핵심 슬로건 1",
      "typography": {{
        "korean": "추천 한글 폰트",
        "english": "추천 영문 폰트",
        "reason": "이 조합이 어울리는 이유"
      }},
      "character": {{
        "name": "캐릭터 이름",
        "concept": "캐릭터 컨셉",
        "personality": "성격 3가지, 쉼표 구분",
        "visual": "외형 묘사"
      }},
      "logo_design": {{
        "brand_name": "브랜드명 1",
        "brand_topic": "사업 주제",
        "core_value": "핵심 가치",
        "target_mood": "브랜드 감성",
        "symbol_type": "심볼 스타일",
        "font_style": "서체 스타일",
        "font_reference": "서체 레퍼런스",
        "font_weight": "서체 굵기",
        "brand_color": "브랜드 컬러",
        "logo_type": "로고 구성 방식",
        "background": "배경"
      }}
    }},
    {{ "name": "브랜드명 2", "meaning": "...", "story": "...", "slogan": "...", "typography": {{ "korean": "...", "english": "...", "reason": "..." }}, "character": {{ "name": "...", "concept": "...", "personality": "...", "visual": "..." }}, "logo_design": {{ "brand_name": "...", "brand_topic": "...", "core_value": "...", "target_mood": "...", "symbol_type": "...", "font_style": "...", "font_reference": "...", "font_weight": "...", "brand_color": "...", "logo_type": "...", "background": "..." }} }},
    {{ "name": "브랜드명 3", "meaning": "...", "story": "...", "slogan": "...", "typography": {{ "korean": "...", "english": "...", "reason": "..." }}, "character": {{ "name": "...", "concept": "...", "personality": "...", "visual": "..." }}, "logo_design": {{ "brand_name": "...", "brand_topic": "...", "core_value": "...", "target_mood": "...", "symbol_type": "...", "font_style": "...", "font_reference": "...", "font_weight": "...", "brand_color": "...", "logo_type": "...", "background": "..." }} }}
  ]
}}"""


def get_O_interview_prompt() -> str:
    return """창업자가 브랜드의 초기 아이디어를 입력했습니다.
당신의 다음 임무는 이 답변들을 바탕으로, 서로 완전히 다른 4개의 [브랜드 초안 후보(MVB)]를 생성하는 것입니다.

[최종적으로 당신이 다음 단계에서 생성해야 할 4가지 초안 항목]
1. 브랜드명 및 의미: 타겟에 맞는 직관적이거나 감각적인 네이밍
2. 핵심 슬로건: 브랜드의 차별점을 보여주는 15자 이내의 한 줄 카피
3. 탄생 서사 요약: 타겟의 페인포인트(Pain-point)를 해결하는 100자 이내의 스토리
4. 시드 컬러(Seed Color): 브랜드의 감성을 대변하는 핵심 색상 (Hex Code)과 그 이유

위의 4가지 항목을 매력적이고 구체적으로 도출하기 위해, 현재 창업자의 입력값에서 가장 비어있는 구체적인 디테일을 파악하여 물어볼 핵심 질문 n개를 생성하세요.

[엄격한 제약 사항]
- 질문의 총 개수(n)는 반드시 5개 이상, 10개 이하여야 합니다.
- 모든 질문은 반드시 4지선다형 객관식이어야 하며, 각 선택지는 서로 완전히 다른 방향성을 제시해야 합니다.
- 마크다운이나 부가 설명 없이 오직 아래의 JSON 형식으로만 출력하세요.

{
  "required_question_count": n,
  "reasoning": "입력된 정보 중 어떤 부분이 모호하여, 이를 구체화하기 위해 어떤 내용의 질문 n개를 생성했습니다.",
  "questions": [
    {
      "question_id": 1,
      "question_text": "질문 내용",
      "options": [
        "1. 선택지 A",
        "2. 선택지 B",
        "3. 선택지 C",
        "4. 선택지 D"
      ]
    }
      ]
    }"""


def get_A_field_regen_prompt(brand_info: dict[str, Any], target: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    base = _join_lines([
        SYSTEM_PROMPT,
        "",
        "아래 제약을 반드시 지키세요:",
        "- 응답은 반드시 JSON만 출력하세요.",
        "- 형식: { \"candidates\": [\"...\", ...] }",
        "- 후보 수는 정확히 3개로 제한하세요.",
        "- 각 후보는 서로 다른 방향성과 어조를 갖게 하세요.",
    ])

    if target == "brand_name":
        return f"""{base}

브랜드 정보: {brand_info}
문맥(선택적): {ctx}

목표: 브랜드명이 필요합니다. 아래 제약을 지켜 3개의 후보를 생성하세요.
- 한글 기준 2~12자 권장
- 간결하고 발음하기 쉬운 이름
- 각 이름에 대해 짧은 1문장(20자 이내) 이유를 병기하되, 출력 형식은 단순한 문자열 후보 배열로 유지하세요.

반드시 JSON 형식으로만 응답하세요:
{{ "candidates": ["이름1", "이름2", "이름3"] }}
"""

    if target == "name_meaning":
        return f"""{base}

브랜드: {brand_info.get('brand_name')}
문맥: {ctx}

목표: 현재 선택된 브랜드명에 대해 서로 다른 해석/의미 설명 3가지를 생성하세요. 각 항목은 1문장(50자 이내)으로 간결하게 작성하세요.

반드시 JSON 형식으로만 응답하세요:
{{ "candidates": ["의미1", "의미2", "의미3"] }}
"""

    if target == "slogan":
        return f"""{base}

브랜드: {brand_info.get('brand_name')}
문맥: {ctx}

목표: 핵심 슬로건 3개를 생성하세요. 각 슬로건은 한국어 기준 15자 이내여야 합니다.

반드시 JSON 형식으로만 응답하세요:
{{ "candidates": ["슬로건1", "슬로건2", "슬로건3"] }}
"""

    if target == "story_summary":
        return f"""{base}

브랜드: {brand_info.get('brand_name')}
문맥: {ctx}

목표: 브랜드 탄생 서사 요약(스토리) 3가지 변주를 생성하세요. 각 항목은 최대 100자 이내로 작성하세요.

반드시 JSON 형식으로만 응답하세요:
{{ "candidates": ["스토리1", "스토리2", "스토리3"] }}
"""

    # fallback: generic short alternatives
    return f"""{base}

브랜드 정보: {brand_info}
문맥: {ctx}

목표: 필드 `{target}`에 대한 짧은 대체 후보 3개를 생성하세요.

반드시 JSON 형식으로만 응답하세요:
{{ "candidates": ["옵션1", "옵션2", "옵션3"] }}
"""


def get_O_mvb_prompt(interview_text: str) -> str:
    return f"""[심층 인터뷰 결과]
{interview_text}

아래 JSON 형식으로만 초안 후보 4개를 응답하세요:

{{
  "candidates": [
    {{
      "id": 1,
      "brand_name": "브랜드명 (국문, 2~20글자)",
      "brand_name_en": "영문명",
      "name_meaning": "이름의 의미와 어감 설명 (50자 이내)",
      "slogan": "핵심 슬로건 (국문, 15자 이내)",
      "story_summary": "브랜드 탄생 서사 요약 (100자 이내)",
      "seed_color": "#XXXXXX",
      "seed_color_reason": "이 컬러를 선택한 이유 (30자 이내)"
    }},
    {{ "id": 2, "brand_name": "...", "brand_name_en": "...", "name_meaning": "...", "slogan": "...", "story_summary": "...", "seed_color": "...", "seed_color_reason": "..." }},
    {{ "id": 3, "brand_name": "...", "brand_name_en": "...", "name_meaning": "...", "slogan": "...", "story_summary": "...", "seed_color": "...", "seed_color_reason": "..." }},
    {{ "id": 4, "brand_name": "...", "brand_name_en": "...", "name_meaning": "...", "slogan": "...", "story_summary": "...", "seed_color": "...", "seed_color_reason": "..." }}
  ]
}}"""


def get_A_interview_prompt(brand_info: dict[str, Any]) -> str:
    return f"""창업자가 방금 아래의 [최종 브랜드 조합]을 확정했습니다. 이 뼈대(MVB)를 바탕으로, 브랜드를 실제 시장에 출시하기 위한 구체적인 실행 전략(디자인, 마케팅, 고객 경험 등)을 수립해야 합니다.

[확정된 최종 브랜드 조합]
{brand_info}

위 결과물들을 완벽하게 도출하기 위해, 확정된 뼈대 정보에서 가장 비어있는 구체적인 디테일을 파악하여 창업자에게 물어볼 핵심 질문 n개를 생성하세요.

[엄격한 제약 사항]
- 질문의 총 개수(n)는 반드시 5개 이상, 10개 이하여야 합니다.
- 모든 질문은 반드시 4지선다형 객관식이어야 하며, 각 선택지는 서로 완전히 다른 방향성을 제시해야 합니다.
- 마크다운이나 부가 설명 없이 오직 아래의 JSON 형식으로만 출력하세요.

{{
  "required_question_count": n,
  "reasoning": "선택된 브랜드 조합은 어떤 감성/장점이 뚜렷하지만, 실제 구현 단계에서 어떤 부분이 모호하여 이를 구체화하기 위해 어떤 내용의 질문 n개를 생성했습니다.",
  "questions": [
    {{
      "question_id": 1,
      "question_text": "질문 내용",
      "options": ["1. 선택지 A", "2. 선택지 B", "3. 선택지 C", "4. 선택지 D"]
    }}
  ]
}}"""


def get_A1_philosophy_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""사용자가 선택한 핵심 브랜드 정체성과 심층 인터뷰 결과를 바탕으로 브랜드 가이드의 '철학과 가치' 영역을 생성하세요.

[사용자 최종 선택값]
- 이름 선택: {brand_info['brand_name']} ({brand_info.get('brand_name_en', '')})
- 의미 선택: {brand_info.get('name_meaning', '')}
- 슬로건 선택: {brand_info.get('slogan', '')}
- 스토리 선택: {brand_info.get('story_summary', '')}
- 컬러 선택: {brand_info.get('seed_color', '')} ({brand_info.get('seed_color_reason', '')})

[추가 실행 전략 심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "brand_philosophy": {{
    "manifesto": "철학 선언문 (1~2문단)",
    "raison_detre": "브랜드 존재 이유 (1문장)",
    "stand_against": ["반대하는 것 1", "반대하는 것 2", "반대하는 것 3"],
    "stand_for": ["지지하고 실천하는 가치 1", "지지하고 실천하는 가치 2", "지지하고 실천하는 가치 3"]
  }},
  "brand_essence": {{
    "keyword": "에센스 키워드 (1~3단어)",
    "keyword_explanation": "해당 키워드의 실제 구현 설명 (3~4줄)",
    "brand_definition": "브랜드 한 줄 정의 (50자 이내)"
  }},
  "core_identity": {{
    "mission": "브랜드 미션 (동사형)",
    "vision": "브랜드 비전 (명사형)",
    "core_values": [
      {{ "value": "핵심 가치 1", "description": "설명", "example": "예시" }},
      {{ "value": "핵심 가치 2", "description": "설명", "example": "예시" }},
      {{ "value": "핵심 가치 3", "description": "설명", "example": "예시" }}
    ]
  }}
}}"""


def get_A2_story_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""사용자가 선택한 핵심 데이터와 심층 인터뷰 결과를 바탕으로 브랜드 가이드의 '네이밍, 슬로건, 브랜드 스토리' 영역을 확장 생성하세요.

[사용자 최종 선택값]
- 이름 선택: {brand_info['brand_name']} ({brand_info.get('brand_name_en', '')})
- 의미 선택: {brand_info.get('name_meaning', '')}
- 슬로건 선택: {brand_info.get('slogan', '')}
- 스토리 선택: {brand_info.get('story_summary', '')}
- 컬러 선택: {brand_info.get('seed_color', '')} ({brand_info.get('seed_color_reason', '')})

[추가 실행 전략 심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "naming_expansion": {{
    "name_story": "탄생 스토리 (100자 이상)",
    "domain_suggestions": ["추천도메인1.com", "추천도메인2.co.kr", "추천도메인3.co.kr"],
    "sns_handles": ["@추천핸들1", "@추천핸들2", "@추천핸들3"],
    "alternative_names": [
      {{ "name": "대안명1", "name_en": "Alt1", "rationale": "상표권 대안으로 추천하는 이유" }},
      {{ "name": "대안명2", "name_en": "Alt2", "rationale": "상표권 대안으로 추천하는 이유" }}
    ]
  }},
  "slogan_expansion": {{
    "main_slogan_en": "영문 메인 슬로건",
    "sub_slogans": [
      {{ "slogan": "서브 슬로건 1", "emphasis": "사용 상황" }},
      {{ "slogan": "서브 슬로건 2", "emphasis": "사용 상황" }},
      {{ "slogan": "서브 슬로건 3", "emphasis": "사용 상황" }}
    ]
  }},
  "brand_story_full": "브랜드 스토리 전문 (반드시 500자 이상, 3~5문단)"
}}"""


def get_A3_positioning_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""사용자가 선택한 핵심 데이터와 심층 인터뷰 결과를 바탕으로 브랜드 가이드의 '포지셔닝 및 브랜드 약속' 영역을 생성하세요.

[사용자 최종 선택값]
- 이름 선택: {brand_info['brand_name']} ({brand_info.get('brand_name_en', '')})
- 의미 선택: {brand_info.get('name_meaning', '')}
- 슬로건 선택: {brand_info.get('slogan', '')}
- 스토리 선택: {brand_info.get('story_summary', '')}
- 컬러 선택: {brand_info.get('seed_color', '')} ({brand_info.get('seed_color_reason', '')})

[추가 실행 전략 심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "positioning": {{
    "statement": "For [타겟], [{brand_info['brand_name']}]은(는) [기존 업계의 뻔한 대안/관행]와(과) 달리 [차별화 혜택]을(를) 제공합니다.",
    "differentiators": [
      {{ "point": "차별화 셀링 포인트 1 제목", "description": "구체적인 차별점 설명 (상세페이지용)" }},
      {{ "point": "차별화 셀링 포인트 2 제목", "description": "구체적인 차별점 설명 (상세페이지용)" }},
      {{ "point": "차별화 셀링 포인트 3 제목", "description": "구체적인 차별점 설명 (상세페이지용)" }}
    ],
    "positioning_map_visualized": {{
      "axis_x": "X축의 양 극단 설명",
      "axis_y": "Y축의 양 극단 설명",
      "quadrants_description": "4개의 사분면이 각각 어떤 시장인지에 대한 시각적 묘사",
      "our_exact_position": "정확한 위치와 분위기 묘사"
    }}
  }},
  "unbreakable_brand_promise": {{
    "declaration": "우리는 당신에게 항상 [핵심 경험]을(를) 드립니다.",
    "proof_of_promise": [
      {{ "channel": "마케팅 콘텐츠", "actionable_rule": "구체적인 실무 행동 지침" }},
      {{ "channel": "패키징 및 언박싱", "actionable_rule": "구체적인 실무 행동 지침" }},
      {{ "channel": "고객 응대 (CS)", "actionable_rule": "구체적인 실무 행동 지침" }}
    ]
  }}
}}"""


def get_A4_core_identity_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""사용자가 선택한 핵심 데이터와 심층 인터뷰 결과를 바탕으로 브랜드 가이드의 '미션, 비전, 핵심 가치(Core Identity)' 영역을 생성하세요.

[사용자 최종 선택값]
- 이름 선택: {brand_info['brand_name']}
- 슬로건 선택: {brand_info.get('slogan', '')}
- 스토리 선택: {brand_info.get('story_summary', '')}
- 컬러 선택: {brand_info.get('seed_color', '')}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "core_identity": {{
    "mission": "우리는 [누구]에게 [무엇]을 [어떻게] 제공한다.",
    "vision": "[시간] 안에 [무엇]이 되는 것",
    "core_values": [
      {{
        "value": "핵심 가치 키워드 1",
        "description": "가치에 대한 20자 이내의 설명",
        "example": "실제 팀원들의 업무 현장 행동/구현 예시 1줄"
      }},
      {{
        "value": "핵심 가치 키워드 2",
        "description": "가치에 대한 20자 이내의 설명",
        "example": "실제 팀원들의 업무 현장 행동/구현 예시 1줄"
      }},
      {{
        "value": "핵심 가치 키워드 3",
        "description": "가치에 대한 20자 이내의 설명",
        "example": "실제 팀원들의 업무 현장 행동/구현 예시 1줄"
      }}
    ]
  }}
}}"""


def get_B_interview_prompt(brand_info: dict[str, Any]) -> str:
    return f"""당신은 지금 창업자가 확정한 [최종 브랜드 조합]을 바탕으로, 이 브랜드에 열광할 '핵심 타겟 페르소나'와 '고객 여정 맵(Customer Journey Map)'을 작성할 준비를 하고 있습니다.

[확정된 최종 브랜드 조합]
{brand_info}

위 결과물들을 완벽하게 도출하기 위해, 확정된 뼈대 정보에서 가장 비어있는 구체적인 디테일을 파악하여 창업자에게 물어볼 핵심 질문 n개를 생성하세요.

[엄격한 제약 사항]
- 질문의 총 개수(n)는 반드시 5개 이상, 10개 이하여야 합니다.
- 모든 질문은 반드시 4지선다형 객관식이어야 하며, 각 선택지는 서로 완전히 다른 방향성을 제시해야 합니다.
- 마크다운이나 부가 설명 없이 오직 아래의 JSON 형식으로만 출력하세요.

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "required_question_count": 1,
  "reasoning": "다음 단계에서 입체적 페르소나 / 고객 여정 맵을 구체적으로 작성하기 위해, 현재 어떤 정보가 부족하므로 이를 파악할 질문 1개를 생성했습니다.",
  "questions": [
    {{
      "question_id": 1,
      "question_text": "타겟 고객의 가장 중요한 라이프스타일/결핍은 무엇입니까?",
      "options": ["1. ...", "2. ...", "3. ...", "4. ..."]
    }}
  ]
}}"""


def get_B1_persona_prompt(brand_info: dict[str, Any], previous_context: str, deepdive_answers_text: str = "") -> str:
    return f"""당신은 10년 차 수석 브랜드 마케팅 디렉터입니다.
창업자가 지금까지 결정한 모든 브랜드 뼈대 데이터와 심층 인터뷰 결과를 변수로 삼아, 시장에서 가장 구매 전환율이 높을 최적의 타겟을 논리적으로 계산(역산)해 내세요.

[제공된 브랜드 핵심 데이터]
- 업종/서비스: {brand_info.get('business_type', '')}
- 브랜드 감성(Vibes): {brand_info.get('vibes', [])}
- 창업자의 초기 타겟 가설: {brand_info.get('target', '')}
- 확정된 브랜드명: {brand_info.get('brand_name', '')}
- 확정된 메인 슬로건: {brand_info.get('slogan', '')}
- 확정된 스토리 요약: {brand_info.get('story_summary', '')}
- 시드 컬러: {brand_info.get('seed_color', '')}

[지금까지 확정된 브랜드 전략]
{previous_context}

[타겟 및 여정 심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "strategic_reasoning": "왜 이 타겟이 도출되었는지에 대한 마케팅 디렉터의 논리적 증명 (2~3문장)",
  "core_target_group": {{
    "definition": "마케팅 과녁이 될 핵심 타겟 1줄 정의",
    "demographics": "광고 세팅용 인구통계 (연령, 성별, 직업, 가구형태)",
    "lifestyle_keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
    "consumption_behavior": "소비 행태 요약 (돈을 아끼는 곳 vs 기꺼이 쓰는 곳)"
  }},
  "primary_persona": {{
    "name": "이름 (가명)",
    "age_and_job": "나이 및 구체적인 직업",
    "daily_scene": "마케팅 타이밍을 잡기 위한 결정적 씬 묘사",
    "pain_point_and_desire": "현재 겪고 있는 결핍과 우리 브랜드를 통한 해결 욕구",
    "emotional_needs": ["정서적 니즈 1", "정서적 니즈 2", "정서적 니즈 3"],
    "deal_breaker": "헛발질을 막아주는 취향의 마지노선"
  }},
  "secondary_personas": [
    {{
      "id": 1,
      "name_and_demographic": "이름 (나이, 직업)",
      "character_type": "타겟 유형",
      "why_they_buy": "구매하는 특수 상황/동기"
    }},
    {{ "id": 2, "name_and_demographic": "...", "character_type": "...", "why_they_buy": "..." }},
    {{ "id": 3, "name_and_demographic": "...", "character_type": "...", "why_they_buy": "..." }},
    {{ "id": 4, "name_and_demographic": "...", "character_type": "...", "why_they_buy": "..." }}
  ],
  "emotional_triggers": [
    {{ "trigger": "감정 트리거 1", "reason": "상세페이지 카피라이팅 소스가 될 구체적 이유" }},
    {{ "trigger": "감정 트리거 2", "reason": "상세페이지 카피라이팅 소스가 될 구체적 이유" }},
    {{ "trigger": "감정 트리거 3", "reason": "상세페이지 카피라이팅 소스가 될 구체적 이유" }}
  ]
}}"""


def get_B2_journey_prompt(brand_info: dict[str, Any], previous_context: str, deepdive_answers_text: str = "") -> str:
    return f"""당신은 10년 차 수석 퍼포먼스/CRM 마케팅 디렉터입니다.
사용자가 확정한 브랜드 핵심 데이터와 인터뷰 결과를 변수로 삼아, 이 브랜드의 타겟이 지갑을 열고 팬이 될 수밖에 없는 최적의 고객 여정 맵(Funnel)을 논리적으로 계산하여 설계하세요.

[제공된 브랜드 핵심 데이터]
- 업종/서비스: {brand_info.get('business_type', '')}
- 브랜드 감성(Vibes): {brand_info.get('vibes', [])}
- 확정된 브랜드명: {brand_info.get('brand_name', '')}
- 확정된 메인 슬로건: {brand_info.get('slogan', '')}
- 확정된 스토리 요약: {brand_info.get('story_summary', '')}

[지금까지 확정된 브랜드 전략]
{previous_context}

[타겟 및 여정 심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "strategic_reasoning": "전략적 퍼널 설계 근거 (2~3문장)",
  "customer_journey_map": [
    {{
      "stage": "인지",
      "touchpoint": "채널",
      "customer_emotion": "고객의 속마음",
      "brand_action": "브랜드의 핵심 킬러 액션"
    }},
    {{
      "stage": "탐색",
      "touchpoint": "채널",
      "customer_emotion": "고객의 속마음",
      "brand_action": "브랜드의 핵심 킬러 액션"
    }},
    {{
      "stage": "구매",
      "touchpoint": "채널",
      "customer_emotion": "고객의 속마음",
      "brand_action": "브랜드의 핵심 킬러 액션"
    }},
    {{
      "stage": "재구매",
      "touchpoint": "채널",
      "customer_emotion": "고객의 속마음",
      "brand_action": "브랜드의 핵심 킬러 액션"
    }},
    {{
      "stage": "전파",
      "touchpoint": "채널",
      "customer_emotion": "고객의 속마음",
      "brand_action": "브랜드의 핵심 킬러 액션"
    }}
  ]
}}"""


def get_C_interview_prompt(brand_info: dict[str, Any]) -> str:
    return f"""확정된 브랜드 조합을 바탕으로 브랜드의 비주얼 시스템을 설계할 준비를 하고 있습니다.

[확정된 최종 브랜드 조합]
{brand_info}

위 결과물들을 완벽하게 도출하기 위해, 확정된 뼈대 정보에서 가장 비어있는 구체적인 디테일을 파악하여 창업자에게 물어볼 핵심 질문 n개를 생성하세요.

[엄격한 제약 사항]
- 질문의 총 개수(n)는 반드시 5개 이상, 10개 이하여야 합니다.
- 모든 질문은 반드시 4지선다형 객관식이어야 하며, 각 선택지는 서로 완전히 다른 방향성을 제시해야 합니다.
- 마크다운이나 부가 설명 없이 오직 아래의 JSON 형식으로만 출력하세요.

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "required_question_count": 1,
  "reasoning": "비주얼 아이덴티티를 구체화하기 위해 필요한 핵심 질문 1개를 생성했습니다.",
  "questions": [
    {{
      "question_id": 1,
      "question_text": "브랜드의 시각 무드를 가장 잘 설명하는 방향은 무엇입니까?",
      "options": ["1. 정갈하고 고급스러운 방향", "2. 따뜻하고 친근한 방향", "3. 자연스럽고 지속가능한 방향", "4. 실험적이고 감각적인 방향"]
    }}
  ]
}}"""


def get_C1_color_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""브랜드의 컬러 팔레트를 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "color_palette": [
    {{ "color_name": "주조색명", "hex_code": "#XXXXXX", "role": "Primary", "reason": "선정 이유" }},
    {{ "color_name": "보조색명", "hex_code": "#XXXXXX", "role": "Secondary", "reason": "선정 이유" }},
    {{ "color_name": "강조색명", "hex_code": "#XXXXXX", "role": "Accent", "reason": "선정 이유" }},
    {{ "color_name": "배경색명", "hex_code": "#XXXXXX", "role": "Background", "reason": "선정 이유" }},
    {{ "color_name": "텍스트색명", "hex_code": "#XXXXXX", "role": "Text Color", "reason": "선정 이유" }}
  ]
}}"""


def get_C2_typography_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""브랜드의 타이포그래피 시스템을 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "typography": {{
    "primary_font": {{
      "font_name_kr": "한글 헤드라인 서체명",
      "google_fonts_family": "Google Fonts 가족명",
      "weight_recommendation": 800,
      "usage_and_reason": "헤드라인/타이틀에 어울리는 이유"
    }},
    "secondary_font": {{
      "font_name_kr": "한글 본문 서체명",
      "google_fonts_family": "Google Fonts 가족명",
      "weight_recommendation": 400,
      "usage_and_reason": "본문/보조 텍스트에 어울리는 이유"
    }}
  }}
}}"""


def get_C3_visual_mood_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""브랜드의 비주얼 무드와 디자인 원칙을 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "visual_mood_guide": {{
    "photography_do": ["권장 표현 1", "권장 표현 2", "권장 표현 3"],
    "photography_dont": ["금지 표현 1", "금지 표현 2", "금지 표현 3"],
    "mood_keywords": ["키워드 1", "키워드 2", "키워드 3", "키워드 4", "키워드 5"]
  }},
  "design_principles": {{
    "layout_direction": "레이아웃 방향성 설명",
    "image_processing": "이미지 보정/가공 규칙 설명"
  }}
}}"""


def get_DE_interview_prompt(brand_info: dict[str, Any]) -> str:
    return f"""확정된 브랜드 조합을 바탕으로 로고와 캐릭터를 설계할 준비를 하고 있습니다.

[확정된 최종 브랜드 조합]
{brand_info}

위 결과물들을 완벽하게 도출하기 위해, 확정된 뼈대 정보에서 가장 비어있는 구체적인 디테일을 파악하여 창업자에게 물어볼 핵심 질문 n개를 생성하세요.

[엄격한 제약 사항]
- 질문의 총 개수(n)는 반드시 5개 이상, 10개 이하여야 합니다.
- 모든 질문은 반드시 4지선다형 객관식이어야 하며, 각 선택지는 서로 완전히 다른 방향성을 제시해야 합니다.
- 마크다운이나 부가 설명 없이 오직 아래의 JSON 형식으로만 출력하세요.

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "required_question_count": 1,
  "reasoning": "로고와 캐릭터를 구체화하기 위해 필요한 핵심 질문 1개를 생성했습니다.",
  "questions": [
    {{
      "question_id": 1,
      "question_text": "이 브랜드의 로고와 캐릭터가 전달해야 할 핵심 인상은 무엇입니까?",
      "options": ["1. 고급스럽고 절제된 인상", "2. 친근하고 따뜻한 인상", "3. 자연스럽고 안정적인 인상", "4. 감각적이고 실험적인 인상"]
    }}
  ]
}}"""


def get_D_logo_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""브랜드 로고 아이덴티티를 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "logo_identity": {{
    "concept": {{
      "symbol_reason": "심볼 선정 이유",
      "color_reason": "컬러 선정 이유",
      "overall_message": "로고가 전달해야 할 전체 메시지",
      "direction_text": "이미지 생성용 디렉션 텍스트"
    }},
    "guide": {{
      "minimum_size": "최소 사용 크기",
      "clear_space": "클리어 스페이스 규정"
    }}
  }}
}}"""


def get_E_character_prompt(brand_info: dict[str, Any], deepdive_answers_text: str = "") -> str:
    return f"""브랜드 캐릭터 가이드를 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[심층 인터뷰 결과]
{deepdive_answers_text}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "character_guide": {{
    "intro": {{
      "name": "캐릭터 이름",
      "appearance": "캐릭터 외형 묘사",
      "symbolic_value": "상징 가치"
    }},
    "reasoning": {{
      "selection_reason": "캐릭터 선택 이유",
      "emotional_connection": "감정적 연결 포인트"
    }},
    "story": {{
      "background": "캐릭터 배경 스토리",
      "brand_role": "브랜드 내 역할"
    }}
  }}
}}"""


def get_logo_variables_prompt(business_type: str, vibes: list[str], target: str, keywords: str = "") -> str:
    mood_options = [
        "모던 & 신뢰",
        "따뜻 & 친근",
        "미니멀 & 프리미엄",
        "자연 & 지속가능",
        "에너지 & 역동",
        "부드러움 & 케어",
        "혁신 & 기술",
        "클래식 & 전통",
    ]
    moods = "', '".join(mood_options)
    return f"""사용자가 다음 정보를 입력했습니다:

업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

이 정보를 바탕으로 로고 생성에 필요한 다음 변수들을 추천해주세요.
반드시 아래 JSON 형식으로만 응답하세요:

{{
  "brand_identity": {{
    "brand_name": "추천 브랜드명",
    "brand_name_meaning": "브랜드명의 의미 1-2문장",
    "brand_topic": "구체적인 사업 주제 또는 업종 설명",
    "core_value": "브랜드 핵심 가치 1-2개 (쉼표 구분)",
    "slogan": "핵심 슬로건 (10단어 이내)"
  }},
  "logo_variables": {{
    "target_mood": "다음 중 선택: '{moods}'",
    "brand_color": "컬러 코드 또는 색상 설명",
    "font_style": "선택: 기하학적 산세리프 / 클래식 세리프 / 손글씨 느낌 / 굵고 강한 / 얇고 우아한",
    "symbol_type": "선택: 기하학적 / 유기적 / 아이콘형 / 추상적 / 레터마크",
    "logo_type": "선택: 심볼+텍스트 조합 / 심볼만 / 텍스트만 / 배지형",
    "background": "선택: 흰색 / 검정 / 브랜드 색상 / 투명"
  }},
  "recommendations_reason": "이 변수들을 추천한 이유 2-3문장"
}}"""

def get_logo_image_prompt(
    brand_name: str,
    direction_text: str,
    brand_info: dict,
    deepdive_answers_text: str,
    data_c: dict,
) -> str:
    # data_c에서 로고에 필요한 값만 추출
    palette = data_c["color_palette"]
    hex_by_role = {c["role"]: c["hex_code"] for c in palette}
    color_palette = ", ".join(
        hex_by_role[r] for r in ("Primary", "Secondary", "Accent") if r in hex_by_role
    )

    mood_keywords = ", ".join(data_c["visual_mood_guide"]["mood_keywords"])
    layout_hint = data_c["design_principles"]["layout_direction"]

    return f"""당신은 세계적 수준의 브랜드 아이덴티티(BI) 디자이너입니다.
아래 브랜드를 위한 심볼/엠블럼 하나를 완성해 주세요.
텍스트나 글자는 이미지에 절대 포함하지 마세요. 심볼 그래픽만 생성합니다.

[확정된 최종 브랜드 조합]: {brand_info}

[심층 인터뷰 결과]: {deepdive_answers_text}

[브랜드명]: {brand_name}
[디자인 핵심 방향성]: {direction_text}

[조형 스타일]
- 구도 원칙: {layout_hint}
- 무드: {mood_keywords}

[컬러]
- 다음 색상만 사용: {color_palette}

[구성]
- 심볼이 캔버스 중앙에 오도록, 사방에 충분한 여백을 확보
- 정사각형 비율에 가깝게, 아이콘/앱 아이콘으로도 쓸 수 있는 독립적인 형태

[배경 및 마감]
- 배경은 완전한 순백색(#FFFFFF)
- 그라데이션, 텍스처, 사실적 음영 없이 solid color로만 표현
- 가장자리는 흐트러짐 없이 선명하고 매끈하게, 스케치·붓터치·워터마크·서명 없음

[텍스트 금지]
- 어떤 형태의 문자, 알파벳, 숫자, 기호도 이미지 안에 그리지 마세요.

[목적]
전문 브랜딩 에이전시 포트폴리오에 들어갈 수준의, 독립적으로 쓸 수 있는 심볼/엠블럼입니다.
"""


def get_character_image_prompt(brand_name: str, char_name: str, char_appearance: str) -> str:
    return f"""당신은 세계적인 수준의 브랜드 캐릭터(마스코트) 전문 일러스트레이터입니다.
다음 지시사항에 따라 브랜드를 대변할 매력적인 캐릭터를 디자인해 주세요.

[브랜드명]: {brand_name}
[캐릭터 이름]: {char_name}
[캐릭터 외형 묘사]: {char_appearance}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 브랜드 로고와 시각적 일관성을 갖춘 깔끔한 2D 벡터 일러스트레이션 또는 매우 정제된 캐릭터 아트.
- 구도: 캐릭터의 전신이나 상반신이 중앙에 명확하게 배치된 프로필 샷.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경.
- 표현: 타겟 고객이 호감을 느낄 수 있는 친근하고 호소력 있는 표정과 동세.
- 텍스트 제어: 이미지 안에 어떤 텍스트나 글자도 포함하지 말 것.
"""


def get_C0_visual_interview_prompt(brand_info: dict[str, Any]) -> str:
    return get_C_interview_prompt(brand_info)


def get_C1_visual_identity_prompt(
    brand_info: dict[str, Any],
    previous_context: str,
    interview_data_c: str,
) -> str:
    return f"""브랜드의 비주얼 시스템을 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[지금까지 확정된 브랜드 전략]
{previous_context}

[비주얼 인터뷰 결과]
{interview_data_c}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "color_palette": [
    {{ "color_name": "주조색명", "hex_code": "#XXXXXX", "role": "Primary", "reason": "선정 이유" }},
    {{ "color_name": "보조색명", "hex_code": "#XXXXXX", "role": "Secondary", "reason": "선정 이유" }},
    {{ "color_name": "강조색명", "hex_code": "#XXXXXX", "role": "Accent", "reason": "선정 이유" }},
    {{ "color_name": "배경색명", "hex_code": "#XXXXXX", "role": "Background", "reason": "선정 이유" }},
    {{ "color_name": "텍스트색명", "hex_code": "#XXXXXX", "role": "Text Color", "reason": "선정 이유" }}
  ],
  "typography": {{
    "primary_font": {{
      "font_name_kr": "한글 헤드라인 서체명",
      "google_fonts_family": "Google Fonts 가족명",
      "weight_recommendation": 800,
      "usage_and_reason": "헤드라인/타이틀에 어울리는 이유"
    }},
    "secondary_font": {{
      "font_name_kr": "한글 본문 서체명",
      "google_fonts_family": "Google Fonts 가족명",
      "weight_recommendation": 400,
      "usage_and_reason": "본문/보조 텍스트에 어울리는 이유"
    }}
  }},
  "visual_mood_guide": {{
    "photography_do": ["권장 표현 1", "권장 표현 2", "권장 표현 3"],
    "photography_dont": ["금지 표현 1", "금지 표현 2", "금지 표현 3"],
    "mood_keywords": ["키워드 1", "키워드 2", "키워드 3", "키워드 4", "키워드 5"]
  }},
  "design_principles": {{
    "layout_direction": "레이아웃 방향성 설명",
    "image_processing": "이미지 보정/가공 규칙 설명"
  }}
}}"""


def get_DE_interview_prompt(brand_info: dict[str, Any], interview_data_c: str) -> str:
    return f"""확정된 브랜드 조합과 C단계 결과를 바탕으로 로고와 캐릭터를 설계할 준비를 하고 있습니다.

[확정된 최종 브랜드 조합]
{brand_info}

[비주얼 인터뷰 결과]
{interview_data_c}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "required_question_count": 1,
  "reasoning": "로고와 캐릭터를 구체화하기 위해 필요한 핵심 질문 1개를 생성했습니다.",
  "questions": [
    {{
      "question_id": 1,
      "question_text": "이 브랜드의 로고와 캐릭터가 전달해야 할 핵심 인상은 무엇입니까?",
      "options": ["1. 고급스럽고 절제된 인상", "2. 친근하고 따뜻한 인상", "3. 자연스럽고 안정적인 인상", "4. 감각적이고 실험적인 인상"]
    }}
  ]
}}"""


def get_DE_identity_prompt(
    brand_info: dict[str, Any],
    data_c: dict[str, Any],
    previous_context: str,
    interview_data_de: str,
) -> str:
    return f"""브랜드의 로고와 캐릭터 가이드를 동시에 설계하세요.

[확정된 최종 브랜드 조합]
{brand_info}

[비주얼 시스템 데이터]
{data_c}

[지금까지 확정된 브랜드 전략]
{previous_context}

[로고·캐릭터 인터뷰 결과]
{interview_data_de}

아래 JSON 형식에 맞추어 응답을 생성하세요:

{{
  "logo_identity": {{
    "concept": {{
      "symbol_reason": "심볼 선정 이유",
      "color_reason": "컬러 선정 이유",
      "overall_message": "로고가 전달해야 할 전체 메시지",
      "direction_text": "이미지 생성용 디렉션 텍스트"
    }},
    "guide": {{
      "minimum_size": "최소 사용 크기",
      "clear_space": "클리어 스페이스 규정"
    }}
  }},
  "character_guide": {{
    "intro": {{
      "name": "캐릭터 이름",
      "appearance": "캐릭터 외형 묘사",
      "symbolic_value": "상징 가치"
    }},
    "reasoning": {{
      "selection_reason": "캐릭터 선택 이유",
      "emotional_connection": "감정적 연결 포인트"
    }},
    "story": {{
      "background": "캐릭터 배경 스토리",
      "brand_role": "브랜드 내 역할"
    }}
  }}
}}"""
