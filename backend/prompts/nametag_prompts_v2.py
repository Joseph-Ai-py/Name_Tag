"""NAME TAG V2 report prompt implementation based on the linked Notion spec.

The Notion document calls the report 24 pages, but its page table lists IDs 00–24
(25 entries). This module includes every listed page ID and does not silently omit one.
It builds one page per model call so downstream code can validate and render each result.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Callable


COMMON_RULES = """공통 작성 규칙:
- 아래 페이지 명세에 있는 키를 빠뜨리지 말고 JSON 객체로만 응답한다.
- 자료가 부족한 항목은 내용을 꾸며내지 말고 status를 insufficient_data 또는 to_validate로 둔다.
- AI 추정값은 evidence_type을 ai_estimate로 표시하고 reasoning과 confidence를 함께 제공한다.
- 외부 사실은 source_ids로 출처 목록을 참조한다. 출처 원문을 만들거나 source_id를 임의로 지어내지 않는다.
- 가상 인물 및 가상 인용문은 반드시 fictional임을 표시한다.
- 점수는 0~100, 신뢰도는 low/medium/high 중 하나로 표시한다.
- 좌표, 가중합, 사분면, TAM/SAM/SOM 수치 등 계산 책임이 백엔드인 값은 계산값을 생성하지 않고 계산 입력과 근거만 반환한다.
- 현재 입력과 앞 단계 결과에 없는 창업자 경험, 시장 통계, 경쟁사 사실을 단정하지 않는다.
- 사람이 읽는 data 문자열에는 핵심 키워드·결정·행동을 Markdown **굵게**로 표시한다. 문장마다 1~2개만 강조하고 문장 전체를 굵게 만들지 않는다.
- 굵게 표시는 data의 본문 문자열에만 사용한다. JSON 키, ID, 제목, 상태, 신뢰도, 수치에는 마크업을 넣지 않는다."""

V2_SYSTEM_PROMPT = """당신은 NAME TAG V2 브랜드·사업 전략 보고서 생성기입니다.
호출 프롬프트에 지정된 페이지 또는 인터뷰 계약과 JSON 구조만 따릅니다.
JSON 객체만 반환하고, 설명이나 마크다운 코드 펜스를 덧붙이지 않습니다.
모르는 외부 사실, 출처, 수치, 창업자 경험을 만들어내지 않습니다.
사람이 읽는 보고서 본문 data의 핵심 키워드·결정·행동은 **굵게** 표시하되 문장마다 1~2개만 고릅니다.
굵게 마크업은 본문 문자열에만 사용하고 JSON 키, ID, 제목, 상태, 신뢰도, 수치에는 넣지 않습니다."""

CONSISTENCY_RULES = """[보고서 전체 일관성 규칙]
- canonical_state와 완료 페이지는 보고서의 기준 데이터다. 새 페이지에서 이를 다시 추론하거나 조용히 바꾸지 않는다.
- 같은 브랜드명, persona_id, competitor_id, source_id, SWOT ID, 축·평가 factor_id를 모든 페이지에서 그대로 재사용한다.
- 완료 페이지와 새 페이지 내용이 충돌하면 새 페이지의 추측으로 덮어쓰지 말고 충돌을 validation_notes에 기록한다.
- 상위 페이지가 의도적으로 수정되면 영향을 받는 하위 페이지는 다시 생성할 대상이다.
- 점수 축·가중치·루브릭은 한 번 확정한 뒤 모든 비교 대상에 동일하게 적용한다.
- 수치 산식과 백엔드 계산 결과는 입력·근거가 바뀌지 않는 한 재작성하지 않는다."""

INTERVIEW_RULES = """인터뷰 출력 규칙:
- 질문은 5~10개 생성한다.
- 각 질문에는 선택지 4개를 정확히 둔다.
- question_id는 인터뷰 안에서 중복되지 않는 정수다.
- required_question_count는 questions 배열 길이와 일치한다.
- 질문은 제공된 브랜드·사업 문맥에 맞추고, 이미 확정된 항목은 반복하지 않는다.
- UI의 자유 입력 기능은 유지한다. 자유 입력 응답은 선택지 답변과 별도로 인터뷰 결과에 수집된다.
- 응답은 JSON 객체만 반환한다."""

INTERVIEW_SPECS = {
    "brand": {
        "title": "Initial Brand Interview",
        "purpose": "브랜드 후보 생성에 필요한 업종, 타겟 문제, 차별점, 톤, 핵심 약속의 빈 정보를 확인한다.",
        "context_pages": [],
    },
    "business": {
        "title": "Business Interview",
        "purpose": "사업 단계, 제품·서비스, 가격, 팀 자원, 운영 제약, 현재 성과와 증거를 확인한다.",
        "context_pages": ["02", "03", "04"],
    },
    "customer": {
        "title": "Customer Interview",
        "purpose": "고객의 상황, 과업, 문제, 기대, 대체재, 구매 기준, 장벽과 행동을 확인한다.",
        "context_pages": ["02", "03", "04", "06"],
    },
    "market": {
        "title": "Market and Competitor Interview",
        "purpose": "시장 범위·지역·기간, 고객 수와 지출 근거, 직접·간접 경쟁사와 대체재 단서를 확인한다.",
        "context_pages": ["06", "07", "08"],
    },
    "visual": {
        "title": "Visual Identity Interview",
        "purpose": "컬러, 타이포그래피, 이미지 무드, 레이아웃 및 이미지 처리 선호를 확인한다.",
        "context_pages": ["02", "03", "04"],
    },
    "logo_character": {
        "title": "Logo and Character Interview",
        "purpose": "심볼의 선 두께·조형 원리, 워드마크, 캐릭터 성격·감정·사용 맥락을 확인한다.",
        "context_pages": ["19"],
    },
}

# Operational routing inferred from the Notion page content and its V1 interview
# stages. These interviews collect inputs; they do not replace research evidence.
REQUIRED_INTERVIEWS_BY_PAGE = {
    "02": ["brand"], "03": ["brand"], "04": ["brand"],
    "06": ["business"], "07": ["customer"], "08": ["customer"],
    "11": ["market"], "12": ["market"], "13": ["market"],
    "19": ["visual"], "20": ["logo_character"], "21": ["logo_character"],
}

def build_report_interview_prompt(
    interview_id: str, context: dict[str, Any]
) -> str:
    """Generate a context-aware 5–10 question interview for report intake."""
    if interview_id not in INTERVIEW_SPECS:
        raise ValueError(f"Unsupported interview_id: {interview_id}")
    spec = INTERVIEW_SPECS[interview_id]
    all_pages = context.get("pages", {})
    relevant_pages = {
        page_id: all_pages[page_id]
        for page_id in spec["context_pages"]
        if page_id in all_pages
    }
    direct_context = {
        key: value for key, value in context.items()
        if key not in {"pages", "canonical_state"}
    }
    example = {
        "required_question_count": 5,
        "reasoning": "현재 입력에서 비어 있는 결정을 확인하는 이유",
        "questions": [
            {
                "question_id": question_id,
                "question_text": f"확인할 구체적인 질문 {question_id}",
                "options": [f"선택지 {question_id}-1", f"선택지 {question_id}-2", f"선택지 {question_id}-3", f"선택지 {question_id}-4"],
            }
            for question_id in range(1, 6)
        ],
    }
    return f"""당신은 NAME TAG V2 보고서 작성을 위한 인터뷰 설계자입니다.
{INTERVIEW_RULES}
{CONSISTENCY_RULES}

[인터뷰 ID]
{interview_id}
[목적]
{spec['purpose']}
[참고할 완료 페이지]
{spec['context_pages']}
[사용자 입력 및 완료된 문맥]
{json.dumps(direct_context, ensure_ascii=False, default=str)}

[이 인터뷰에 필요한 완료 페이지]
{json.dumps(relevant_pages, ensure_ascii=False, default=str)}

[확정된 공통 기준]
{json.dumps(context.get('canonical_state', {}), ensure_ascii=False, default=str)}

이미 확인된 내용은 다시 묻지 마세요. 모르는 외부 사실을 선택지에 사실처럼 넣지 마세요. 선택지 4개는 서로 구별되고 실제 답변에 도움이 되게 작성하세요. 사용자는 UI에서 각 질문에 자유 입력도 할 수 있습니다.

반환 구조 예시:
{json.dumps(example, ensure_ascii=False, indent=2)}
질문은 5~10개 생성하고, 실제 개수에 맞춰 required_question_count를 설정하세요. 오직 JSON 객체만 반환하세요."""


def validate_interview_result(result: dict[str, Any]) -> list[str]:
    """Validate the shared interview response contract."""
    errors: list[str] = []
    questions = result.get("questions")
    if not isinstance(questions, list) or not 5 <= len(questions) <= 10:
        return ["questions must contain 5 to 10 items"]
    if result.get("required_question_count") != len(questions):
        errors.append("required_question_count must equal questions length")
    if not all(isinstance(question, dict) for question in questions):
        return ["each question must be an object"]
    ids = [q.get("question_id") for q in questions]
    if any(not isinstance(question_id, int) or isinstance(question_id, bool) for question_id in ids):
        errors.append("question_id values must be integers")
    valid_ids = [question_id for question_id in ids if isinstance(question_id, int) and not isinstance(question_id, bool)]
    if len(valid_ids) != len(set(valid_ids)):
        errors.append("question_id values must be unique")
    for index, question in enumerate(questions, start=1):
        if not isinstance(question.get("question_text"), str) or not question["question_text"].strip():
            errors.append(f"question {index} needs question_text")
        options = question.get("options")
        if not isinstance(options, list) or len(options) != 4:
            errors.append(f"question {index} must have exactly four options")
        elif any(not isinstance(option, str) or not option.strip() for option in options):
            errors.append(f"question {index} options must be non-empty strings")
    return errors


def build_initial_brand_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for initial brand assumptions before brand candidate generation."""
    return build_report_interview_prompt("brand", context)


def build_business_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for Business Overview inputs."""
    return build_report_interview_prompt("business", context)


def build_customer_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for persona and customer journey inputs."""
    return build_report_interview_prompt("customer", context)


def build_market_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for market size, market analysis, and competitor research inputs."""
    return build_report_interview_prompt("market", context)


def build_visual_identity_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for Visual Identity page inputs."""
    return build_report_interview_prompt("visual", context)


def build_logo_character_interview_prompt(context: dict[str, Any]) -> str:
    """Interview for Logo Identity and conditional Character Identity inputs."""
    return build_report_interview_prompt("logo_character", context)


# Each page spec is a model-facing data contract, derived from the Notion page table.
# Fields are descriptive contracts, not a substitute for backend JSON Schema validation.
REPORT_PAGE_SPECS: dict[str, dict[str, Any]] = {
    "00": {"title": "Cover", "deps": [], "fields": ["brand_name", "industry", "report_version", "report_date", "key_sentence", "brand_promise"]},
    "01": {"title": "Executive Summary", "deps": ["02", "03", "04", "05", "06", "09", "10", "11", "12", "13", "14", "15", "16", "18", "19", "20", "22", "23"], "fields": ["brand_thesis", "key_metrics", "key_findings_3", "key_strategies_3", "priority_actions", "calculation_basis"]},
    "02": {"title": "Brand Foundation", "deps": [], "fields": ["golden_circle.why", "golden_circle.how", "golden_circle.what", "brand_essence", "customer_connection"]},
    "03": {"title": "Brand Identity", "deps": ["02"], "fields": ["identity_prism.physique", "identity_prism.personality", "identity_prism.culture", "identity_prism.relationship", "identity_prism.reflection", "identity_prism.self_image", "archetype", "core_values_3_to_5", "behavior_definitions"]},
    "04": {"title": "Brand Story", "deps": ["02", "03"], "fields": ["naming_origin_meaning_pronunciation_symbolism", "story.origin", "story.problem", "story.belief", "story.promise", "slogan", "founder_experience_is_not_fabricated"]},
    "05": {"title": "Brand Positioning", "deps": ["11", "13"], "fields": ["axes.x_and_y_with_description_anchors_factors_weights_rubric", "entities.our_idea_and_competitors", "factor_scores.score_reasoning_source_ids", "confidence", "evidence_type", "pop", "pod", "brand_mantra", "strategic_implication", "coordinates_backend_calculated"]},
    "06": {"title": "Business Overview", "deps": [], "fields": ["business_stage", "products_services", "features_benefits_pricing", "team_capabilities_budget_infrastructure", "current_performance", "constraints", "evidence"]},
    "07": {"title": "Customer Personas 01–02", "deps": ["06"], "fields": ["personas_P1_P2", "persona_fields_from_page_07_08_spec", "fictional_name_and_quote_flags", "generation_basis", "confidence"]},
    "08": {"title": "Customer Personas 03–04", "deps": ["06"], "fields": ["personas_P3_P4", "persona_fields_from_page_07_08_spec", "distinct_goals_situations_pains_behaviors", "fictional_name_and_quote_flags", "generation_basis", "confidence"]},
    "09": {"title": "Persona Comparison", "deps": ["07", "08"], "fields": ["persona_ids_P1_to_P4", "comparison.problem_intensity_frequency_solution_intent_willingness_accessibility_barriers_fit", "shared_problems", "differences", "priority_segment_and_reasoning", "score_evidence_type"]},
    "10": {"title": "Value Proposition", "deps": ["07", "08", "09", "06"], "fields": ["persona_vpcs_for_P1_to_P4", "jobs_pains_gains_products_pain_relievers_gain_creators", "scores_S_F_I_A_P_G_D_C_with_reasoning", "x_y_inputs", "coordinates_backend_calculated", "quadrant_backend_determined", "fit_explanation"]},
    "11": {"title": "Market Analysis", "deps": ["06", "07", "08"], "fields": ["three_c.company_customer_competitor", "five_forces.intensity_evidence_impact", "key_success_factors_3_to_5", "market_attractiveness", "strategic_implications", "source_ids"]},
    "12": {"title": "Market Size", "deps": ["06", "11"], "fields": ["tam_sam_som.amount_customer_count_revenue_per_customer_year", "calculation_method_and_formula", "bottom_up_top_down_comparison", "assumptions_exclusions", "source_ids", "confidence", "insufficient_data_when_needed"]},
    "13": {"title": "Competitor Analysis", "deps": ["06", "11"], "fields": ["competitors_3_to_5_direct_indirect_substitute", "company_website_product_target_positioning_price_strengths_limitations_channels", "source_ids_per_fact", "comparison_summary", "market_gaps", "recommended_differentiation"]},
    "14": {"title": "SWOT Analysis", "deps": ["06", "11", "12", "13"], "fields": ["strengths_internal_ids_S1", "weaknesses_internal_ids_W1", "opportunities_external_ids_O1", "threats_external_ids_T1", "factor_evidence_source_ids_impact_confidence"]},
    "15": {"title": "TOWS Strategy", "deps": ["14"], "fields": ["SO_WO_ST_WT_strategies", "strategy_id", "linked_existing_factor_ids", "first_action", "success_metric", "priority", "owner_role", "timeline", "estimated_cost"]},
    "16": {"title": "Business Model Canvas", "deps": ["06", "09", "10", "11", "14", "15"], "fields": ["customer_segments", "value_propositions", "channels", "customer_relationships", "revenue_streams", "key_resources", "key_activities", "key_partners", "cost_structure", "validation_plan", "status_evidence_source_ids_validation_method"]},
    "17": {"title": "Lean Canvas", "deps": ["06", "09", "10", "11"], "conditional": True, "fields": ["enabled", "problem", "customer_segments", "unique_value_proposition", "solution", "channels", "revenue_streams", "cost_structure", "key_metrics", "unfair_advantage", "hypotheses"]},
    "18": {"title": "Customer Journey", "deps": ["07", "08", "16"], "fields": ["persona_ids", "stages", "touchpoints", "customer_actions", "customer_emotions", "brand_response", "channels_and_relationship_consistency"]},
    "19": {"title": "Visual Identity", "deps": ["02", "03", "04", "07", "08"], "fields": ["color_palette", "typography", "photography_do_dont", "mood_keywords", "layout_direction", "image_processing"]},
    "20": {"title": "Logo Identity", "deps": ["03", "04", "19"], "fields": ["logo_concept", "symbol", "wordmark", "usage_rules", "minimum_size", "clear_space"]},
    "21": {"title": "Character Identity", "deps": ["03", "07", "08", "19"], "conditional": True, "fields": ["character_appearance_personality_story_role", "symbolic_value", "emotional_connection"]},
    "22": {"title": "Brand Applications", "deps": ["19", "20", "21", "07", "08"], "fields": ["web_sns_package_print_digital_ui_mockups", "application_context", "brand_consistency_notes"]},
    "23": {"title": "Validation Roadmap", "deps": ["09", "10", "11", "12", "13", "14", "15", "16"], "fields": ["30_60_90_day_plan", "validation_hypotheses", "experiments", "kpis", "owners", "timeline", "priority"]},
    "24": {"title": "Research Evidence", "deps": ["01", "05", "06", "09", "10", "11", "12", "13", "14"], "fields": ["sources.source_id_title_publisher_url_published_at_accessed_at", "calculation_assumptions", "limitations", "validation_status", "ai_estimate_vs_external_evidence"]},
}


PERSONA_FIELDS = [
    "persona_id", "archetype_label", "segment", "name (mark fictional)",
    "age_range", "occupation_or_situation", "lifestyle", "background",
    "customer_jobs", "behavior", "purchase_criteria", "pains", "gains",
    "motivation", "barriers", "alternatives", "quote (mark fictional)",
    "product_expectations", "product_concerns", "generation_basis", "confidence",
]

PAGE_TASKS = {
    "00": "표지에 필요한 식별 정보와 브랜드 핵심 문장을 작성한다.",
    "01": "사업을 1분 안에 이해하도록 핵심 요약, 발견 3개, 전략 3개, 우선 과제를 작성한다. 수치에는 산출 기준과 근거를 연결한다.",
    "02": "Golden Circle과 Brand Essence를 작성하고 고객 문제와 논리적으로 연결한다.",
    "03": "Identity Prism 6면, 대표 Archetype, 핵심 가치 3~5개와 행동 정의를 작성한다.",
    "04": "네이밍 의미와 Origin→Problem→Belief→Promise 스토리를 작성한다. 입력에 없는 실제 창업 경험은 만들지 않는다.",
    "05": "시장·경쟁 자료에 맞는 공통 X/Y축, 앵커, 평가 요소, 가중치, 루브릭을 만들고 우리 아이디어와 경쟁사를 같은 기준으로 평가한다. 축별 가중치 합은 1.0이다. entities의 각 항목은 entity_id, entity_type, name, factor_scores[{factor_id,score,reasoning,source_ids}], confidence, evidence_type를 포함한다. 모든 entity에 축의 모든 factor_id 점수를 제공한다. 좌표는 계산하지 않는다.",
    "06": "사업 단계, 제품·서비스, 자원, 성과, 제약, 확보된 증거를 정리한다. 내부 역량은 SWOT과 연결 가능하도록 구체적으로 쓴다.",
    "07": "서로 다른 고객 유형 P1/P2를 생성한다. 이 페이지의 persona_id는 정확히 P1, P2로 고정한다. 각 페르소나는 공통 페르소나 필드를 모두 포함한다.",
    "08": "P3/P4를 P1/P2의 복제 없이 생성한다. 이 페이지의 persona_id는 정확히 P3, P4로 고정한다. 목표·상황·문제·행동이 구별되어야 한다.",
    "09": "P1~P4를 동일한 비교 기준으로 비교하고 우선 공략 고객과 근거를 제안한다. comparison 항목마다 persona_id와 기준별 점수·근거·evidence_type을 연결한다.",
    "10": 'P1~P4 각각의 독립 VPC를 생성한다. 각 persona_vpcs 항목은 persona_id, customer_jobs, pains, gains, products_services, pain_relievers, gain_creators를 포함한다. value_fit_inputs는 반드시 객체이며 P1~P4 키 각각 아래에 S/F/I/A/P/G/D/C 키를 둔다. 각 factor 값은 score(0~100 숫자)와 reasoning(근거 문자열)을 가진 객체다. 예시 구조: {"P1":{"S":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"F":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"I":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"A":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"P":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"G":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"D":{"score":0,"reasoning":"근거 부족으로 검증 필요"},"C":{"score":0,"reasoning":"근거 부족으로 검증 필요"}}}. P2~P4도 같은 구조를 제공한다. X=0.35S+0.25F+0.25I+0.15A, Y=0.35P+0.30G+0.20D+0.15C를 적용할 입력을 반환하되 좌표와 사분면은 계산하지 않는다.',
    "11": "3C, Porter 5 Forces, KSF를 출처와 함께 분석한다.",
    "12": "TAM/SAM/SOM을 고객 수와 연간 고객당 매출의 근거 있는 산식으로 작성한다. 근거 부족 시 insufficient_data로 표시한다.",
    "13": "직접·간접 경쟁사와 대체재를 구분해 3~5개 우선 분석하고, 각 기업에 변경하지 않을 competitor_id를 부여하며 사실별 출처 ID를 연결한다.",
    "14": "내부 요인은 S/W, 외부 요인은 O/T로 구분한다. 요인 객체는 id, factor, evidence, impact, source_ids, confidence를 갖고 그룹별 접두어(S/W/O/T)를 사용한다.",
    "15": "SWOT의 실제 요인 ID를 연결해 SO/WO/ST/WT 실행 전략을 작성한다. 전략 객체는 strategy_id, strategy, linked_factors, first_action, success_metric, priority, owner_role, timeline, estimated_cost를 갖는다.",
    "16": "BMC 9개 블록과 보조 검증 계획을 작성한다. 각 블록 항목은 statement, status(validated/assumption/to_validate), evidence, source_ids, validation_method를 둔다.",
    "17": "초기 가설 검증에 적합한 경우에만 Lean Canvas를 enabled=true로 작성한다. 불필요하면 enabled=false로 반환한다.",
    "18": "동일 persona_id를 사용해 고객 접점, 행동, 감정, 브랜드 대응이 연결된 여정을 작성한다.",
    "19": "컬러, 타이포그래피, 이미지 무드, 레이아웃, 이미지 처리 원칙을 작성한다.",
    "20": "로고 콘셉트, 심볼, 워드마크, 최소 크기, 클리어 스페이스 규칙을 작성한다.",
    "21": "사업과 브랜드에 캐릭터가 적합한 경우 캐릭터 정체성을 작성한다. 필요하지 않으면 enabled=false로 반환한다.",
    "22": "브랜드 전략과 시각 규칙을 반영한 웹·SNS·패키지·인쇄물·디지털 UI 적용 방향을 작성한다.",
    "23": "30/60/90일 검증 과제, KPI, 담당 역할, 일정, 우선순위를 작성한다.",
    "24": "보고서에서 사용한 출처, 계산 가정, 한계, 검증 내역을 정리하고 AI 추정과 외부 근거를 구분한다.",
}


# Few-shot examples demonstrate output behavior, not industry facts. The examples
# use explicit placeholders or synthetic values so the model does not copy them
# as evidence about the user's business.
FEW_SHOT_EXAMPLES = {
    "00": {
        "input": "브랜드명 미제공, 업종 미제공",
        "output": {"page_id": "00", "title": "Cover", "status": "insufficient_data", "data": {"brand_name": "추가 정보 필요", "industry": "추가 정보 필요", "report_version": "V2", "report_date": "입력값 필요", "key_sentence": "추가 정보 필요", "brand_promise": "추가 정보 필요"}, "field_guidance": ["brand_name", "industry", "report_version", "report_date", "key_sentence", "brand_promise"], "evidence_type": "user_input", "source_ids": [], "confidence": "low"},
        "lesson": "미입력 정보를 지어내지 않고 필요한 정보로 표시한다.",
    },
    "12": {
        "input": "시장 고객 수와 연간 고객당 매출 자료가 제공되지 않음",
        "output": {"page_id": "12", "title": "Market Size", "status": "insufficient_data", "data": {"tam": {"amount": None, "customer_count": None, "annual_revenue_per_customer": None}, "sam": {"amount": None, "customer_count": None, "annual_revenue_per_customer": None}, "som": {"amount": None, "customer_count": None, "annual_revenue_per_customer": None}, "calculation_method": "고객 수 × 연간 고객당 매출 자료 필요", "assumptions": [], "exclusions": [], "source_ids": []}, "evidence_type": "insufficient_data", "source_ids": [], "confidence": "low"},
        "lesson": "근거가 없으면 점유율을 임의 적용하지 않고 수치 대신 누락 상태와 필요한 자료를 반환한다.",
    },
    "14": {
        "input": "현재 팀 역량은 사용자 입력, 외부 시장 근거는 아직 없음",
        "output": {"page_id": "14", "title": "SWOT Analysis", "status": "to_validate", "data": {"strengths": [{"id": "S1", "factor": "입력에서 확인된 내부 역량", "evidence": "사용자 입력 참조", "impact": "평가 필요", "source_ids": [], "confidence": "low"}], "weaknesses": [], "opportunities": [], "threats": []}, "evidence_type": "user_input", "source_ids": [], "confidence": "low"},
        "lesson": "S/W는 내부 요인, O/T는 외부 요인으로 분리하고 외부 근거가 없으면 O/T를 만들어내지 않는다.",
    },
    "16": {
        "input": "고객 세그먼트는 가설이며 아직 검증되지 않음",
        "output": {"page_id": "16", "title": "Business Model Canvas", "status": "to_validate", "data": {"customer_segments": [{"statement": "가설 고객 세그먼트", "status": "assumption", "evidence": "현재 입력에 기반한 가설", "source_ids": [], "validation_method": "고객 인터뷰로 확인"}], "value_propositions": [], "channels": [], "customer_relationships": [], "revenue_streams": [], "key_resources": [], "key_activities": [], "key_partners": [], "cost_structure": [], "validation_plan": []}, "evidence_type": "ai_estimate", "source_ids": [], "confidence": "low"},
        "lesson": "검증 전 사업 모델 요소는 validated가 아니라 assumption 또는 to_validate로 표시한다.",
    },
}


REQUIRED_DATA_KEYS = {
    "00": ["brand_name", "industry", "report_version", "report_date", "key_sentence", "brand_promise"],
    "01": ["brand_thesis", "key_metrics", "key_findings", "key_strategies", "priority_actions", "calculation_basis"],
    "02": ["golden_circle", "brand_essence", "customer_connection"],
    "03": ["identity_prism", "archetype", "core_values"],
    "04": ["naming", "story", "slogan"],
    "05": ["axis_x", "axis_y", "entities", "pop", "pod", "brand_mantra", "strategic_implication"],
    "06": ["business_stage", "products_services", "resources", "current_performance", "constraints", "evidence"],
    "07": ["personas"], "08": ["personas"],
    "09": ["comparison", "shared_problems", "differences", "priority_segment"],
    "10": ["persona_vpcs", "value_fit_inputs"],
    "11": ["three_c", "five_forces", "key_success_factors", "market_attractiveness", "source_ids"],
    "12": ["tam", "sam", "som", "calculation_method", "assumptions", "exclusions", "source_ids"],
    "13": ["competitors", "comparison_summary", "market_gaps", "recommended_differentiation"],
    "14": ["strengths", "weaknesses", "opportunities", "threats"],
    "15": ["SO", "WO", "ST", "WT"],
    "16": ["customer_segments", "value_propositions", "channels", "customer_relationships", "revenue_streams", "key_resources", "key_activities", "key_partners", "cost_structure", "validation_plan"],
    "17": ["enabled", "problem", "customer_segments", "unique_value_proposition", "solution", "channels", "revenue_streams", "cost_structure", "key_metrics", "unfair_advantage", "hypotheses"],
    "18": ["persona_ids", "stages"],
    "19": ["color_palette", "typography", "image_mood", "design_principles"],
    "20": ["concept", "symbol", "wordmark", "usage_rules"],
    "21": ["enabled", "character_identity"],
    "22": ["applications", "brand_consistency_notes"],
    "23": ["plan_30_60_90_days", "validation_hypotheses", "kpis", "owners", "timeline", "priority"],
    "24": ["sources", "calculation_assumptions", "limitations", "validation_records", "evidence_types"],
}


def build_consistency_manifest(pages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Extract shared identities and decisions from validated upstream pages."""
    def data(page_id: str) -> dict[str, Any]:
        return pages.get(page_id, {}).get("data", {})

    brand_name = data("00").get("brand_name")
    if not brand_name:
        brand_name = data("04").get("naming", {}).get("name")
    persona_by_id: dict[str, Any] = {}
    for page_id in ("07", "08"):
        for persona in data(page_id).get("personas", []):
            if persona.get("persona_id"):
                persona_by_id[persona["persona_id"]] = {
                    key: persona.get(key)
                    for key in (
                        "persona_id", "segment", "customer_jobs", "pains", "gains",
                        "purchase_criteria", "barriers", "alternatives",
                    )
                    if key in persona
                }
    swot_ids = []
    for group in ("strengths", "weaknesses", "opportunities", "threats"):
        swot_ids.extend(item.get("id") for item in data("14").get(group, []) if item.get("id"))
    positioning = data("05")
    competitor_data = data("13").get("competitors", [])
    evidence_sources = data("24").get("sources", [])
    return {
        "brand_name": brand_name,
        "brand_essence": data("02").get("brand_essence"),
        "core_values": data("03").get("core_values", []),
        "brand_promise": data("04").get("story", {}).get("promise"),
        "business_stage": data("06").get("business_stage"),
        "products_services": data("06").get("products_services"),
        "persona_ids": sorted(persona_by_id),
        "personas": persona_by_id,
        "competitors": [
            {key: item.get(key) for key in ("competitor_id", "name", "type") if key in item}
            for item in competitor_data
        ],
        "positioning_axes": {
            "axis_x": positioning.get("axis_x"),
            "axis_y": positioning.get("axis_y"),
        } if positioning else {},
        "swot_factor_ids": sorted(swot_ids),
        "color_palette": data("19").get("color_palette", []),
        "source_ids": sorted(
            source.get("source_id") for source in evidence_sources if source.get("source_id")
        ),
        "completed_page_ids": sorted(pages),
    }


def dependency_closure(page_id: str) -> set[str]:
    """Return transitive page dependencies for a focused prompt context."""
    if page_id not in REPORT_PAGE_SPECS:
        raise ValueError(f"Unsupported report page_id: {page_id}")
    found: set[str] = set()
    pending = list(REPORT_PAGE_SPECS[page_id]["deps"])
    while pending:
        dependency = pending.pop()
        if dependency in found:
            continue
        found.add(dependency)
        pending.extend(REPORT_PAGE_SPECS[dependency]["deps"])
    return found


def downstream_page_ids(page_id: str) -> set[str]:
    """Return transitive dependents so an upstream edit can invalidate stale pages."""
    if page_id not in REPORT_PAGE_SPECS:
        raise ValueError(f"Unsupported report page_id: {page_id}")
    invalidated = {page_id}
    changed = True
    while changed:
        changed = False
        for candidate, spec in REPORT_PAGE_SPECS.items():
            if candidate not in invalidated and invalidated.intersection(spec["deps"]):
                invalidated.add(candidate)
                changed = True
    return invalidated


def build_report_page_prompt(
    page_id: str, report_context: dict[str, Any]
) -> str:
    """Build a prompt for exactly one Notion-defined report page."""
    if page_id not in REPORT_PAGE_SPECS:
        raise ValueError(f"Unsupported report page_id: {page_id}")
    spec = REPORT_PAGE_SPECS[page_id]
    persona_note = (
        "\n공통 페르소나 필드: " + json.dumps(PERSONA_FIELDS, ensure_ascii=False)
        if page_id in {"07", "08"}
        else ""
    )
    contract = {
        "page_id": page_id,
        "title": spec["title"],
        "status": "complete | insufficient_data | to_validate",
        "data": {field: "이 필드에 맞는 값" for field in REQUIRED_DATA_KEYS[page_id]},
        "field_guidance": spec["fields"],
        "evidence_type": "external_research | user_input | ai_estimate | mixed",
        "source_ids": [],
        "confidence": "low | medium | high",
        "validation_notes": [],
    }
    few_shot = FEW_SHOT_EXAMPLES.get(page_id)
    few_shot_text = (
        "[Few-shot 예시: 형식과 판단 규칙만 참고하고 값은 복사하지 말 것]\n"
        + json.dumps(few_shot, ensure_ascii=False, indent=2)
        if few_shot
        else "이 페이지용 few-shot 예시는 없습니다. 출력 계약과 페이지 규칙을 따르세요."
    )
    upstream_pages = report_context.get("pages", {})
    needed_page_ids = dependency_closure(page_id)
    relevant_pages = {
        dependency: upstream_pages[dependency]
        for dependency in needed_page_ids
        if dependency in upstream_pages
    }
    manifest = report_context.get("canonical_state") or build_consistency_manifest(upstream_pages)
    direct_context = {
        key: value for key, value in report_context.items()
        if key not in {"pages", "canonical_state"}
    }
    interview_answers = direct_context.get("interview_answers")
    if isinstance(interview_answers, dict):
        allowed_interviews = set(REQUIRED_INTERVIEWS_BY_PAGE.get(page_id, []))
        direct_context["interview_answers"] = {
            key: value for key, value in interview_answers.items()
            if key in allowed_interviews
        }
    return f"""당신은 NAME TAG V2 브랜드·사업 보고서 작성기입니다.
{COMMON_RULES}
{CONSISTENCY_RULES}

[페이지]
ID: {page_id}
제목: {spec['title']}
조건부 페이지: {spec.get('conditional', False)}
선행 페이지: {spec['deps']}

[페이지 작업]
{PAGE_TASKS[page_id]}{persona_note}

[현재까지의 입력 및 선행 결과]
{json.dumps(direct_context, ensure_ascii=False, default=str)}

[이 페이지의 직접·간접 선행 페이지]
{json.dumps(relevant_pages, ensure_ascii=False, default=str)}

[Canonical state: 확정된 공통 기준]
{json.dumps(manifest, ensure_ascii=False, default=str)}

{few_shot_text}

[출력 계약]
아래 객체의 최상위 키와 page_id/title은 유지하세요. data 내부는 페이지 명세의 모든 필드를 포함하세요. 예시 값 설명을 실제 값으로 대체하고, 모르는 내용은 명시적으로 표시하세요.
{json.dumps(contract, ensure_ascii=False, indent=2)}
오직 JSON 객체 하나만 반환하세요."""


# Named page builders for routing and individual copy/paste use.
def build_cover_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("00", context)
def build_executive_summary_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("01", context)
def build_brand_foundation_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("02", context)
def build_brand_identity_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("03", context)
def build_brand_story_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("04", context)
def build_brand_positioning_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("05", context)
def build_business_overview_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("06", context)
def build_personas_01_02_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("07", context)
def build_personas_03_04_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("08", context)
def build_persona_comparison_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("09", context)
def build_value_proposition_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("10", context)
def build_market_analysis_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("11", context)
def build_market_size_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("12", context)
def build_competitor_analysis_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("13", context)
def build_swot_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("14", context)
def build_tows_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("15", context)
def build_business_model_canvas_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("16", context)
def build_lean_canvas_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("17", context)
def build_customer_journey_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("18", context)
def build_visual_identity_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("19", context)
def build_logo_identity_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("20", context)
def build_character_identity_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("21", context)
def build_brand_applications_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("22", context)
def build_validation_roadmap_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("23", context)
def build_research_evidence_page_prompt(context: dict[str, Any]) -> str: return build_report_page_prompt("24", context)


REPORT_PAGE_ORDER = [f"{number:02d}" for number in range(25)]

# Keep page IDs, prompt builder names, response contracts, and PDF page builders
# connected through this registry instead of routing every page through an
# unnamed generic prompt function.
PAGE_PROMPT_BUILDERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "00": build_cover_page_prompt,
    "01": build_executive_summary_page_prompt,
    "02": build_brand_foundation_page_prompt,
    "03": build_brand_identity_page_prompt,
    "04": build_brand_story_page_prompt,
    "05": build_brand_positioning_page_prompt,
    "06": build_business_overview_page_prompt,
    "07": build_personas_01_02_page_prompt,
    "08": build_personas_03_04_page_prompt,
    "09": build_persona_comparison_page_prompt,
    "10": build_value_proposition_page_prompt,
    "11": build_market_analysis_page_prompt,
    "12": build_market_size_page_prompt,
    "13": build_competitor_analysis_page_prompt,
    "14": build_swot_page_prompt,
    "15": build_tows_page_prompt,
    "16": build_business_model_canvas_page_prompt,
    "17": build_lean_canvas_page_prompt,
    "18": build_customer_journey_page_prompt,
    "19": build_visual_identity_page_prompt,
    "20": build_logo_identity_page_prompt,
    "21": build_character_identity_page_prompt,
    "22": build_brand_applications_page_prompt,
    "23": build_validation_roadmap_page_prompt,
    "24": build_research_evidence_page_prompt,
}


def build_named_report_page_prompt(page_id: str, context: dict[str, Any]) -> str:
    """Build a page prompt through its named page-specific function."""
    try:
        builder = PAGE_PROMPT_BUILDERS[page_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported report page ID: {page_id}") from exc
    return builder(context)


def build_report_generation_plan() -> list[dict[str, Any]]:
    """Return a topological page order; conditional pages remain marked."""
    remaining = set(REPORT_PAGE_ORDER)
    resolved: set[str] = set()
    ordered: list[str] = []
    while remaining:
        ready = [
            page_id for page_id in REPORT_PAGE_ORDER
            if page_id in remaining
            and set(REPORT_PAGE_SPECS[page_id]["deps"]).issubset(resolved)
        ]
        if not ready:
            raise ValueError("report page dependency cycle detected")
        ordered.extend(ready)
        resolved.update(ready)
        remaining.difference_update(ready)
    return [{"page_id": page_id, **REPORT_PAGE_SPECS[page_id]} for page_id in ordered]


VPC_X_WEIGHTS = {"S": 0.35, "F": 0.25, "I": 0.25, "A": 0.15}
VPC_Y_WEIGHTS = {"P": 0.35, "G": 0.30, "D": 0.20, "C": 0.15}


def calculate_weighted_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    """Backend-owned weighted score calculation; validates score and weight ranges."""
    if set(scores) != set(weights):
        raise ValueError("scores and weights must use the same factor keys")
    if any(not 0 <= float(value) <= 100 for value in scores.values()):
        raise ValueError("all factor scores must be between 0 and 100")
    if any(float(value) < 0 for value in weights.values()):
        raise ValueError("weights must be non-negative")
    if abs(sum(float(value) for value in weights.values()) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1.0")
    return sum(float(scores[key]) * float(weights[key]) for key in weights)


def calculate_vpc_coordinates(scores: dict[str, float]) -> dict[str, float | str]:
    """Calculate VPC X/Y from Notion's stated weights and assign the 50-point quadrant."""
    x_scores = {key: scores[key] for key in VPC_X_WEIGHTS}
    y_scores = {key: scores[key] for key in VPC_Y_WEIGHTS}
    x = calculate_weighted_score(x_scores, VPC_X_WEIGHTS)
    y = calculate_weighted_score(y_scores, VPC_Y_WEIGHTS)
    if x >= 50 and y >= 50:
        quadrant = "high_problem_high_fit"
    elif x >= 50:
        quadrant = "high_problem_low_fit"
    elif y >= 50:
        quadrant = "low_problem_high_fit"
    else:
        quadrant = "low_problem_low_fit"
    return {"x": round(x, 2), "y": round(y, 2), "quadrant": quadrant}


def calculate_positioning_axis_score(
    factor_scores: list[dict[str, Any]], evaluation_factors: list[dict[str, Any]]
) -> float:
    """Backend weighted score for one positioning axis and one evaluated entity."""
    weights = {str(item["factor_id"]): float(item["weight"]) for item in evaluation_factors}
    scores = {str(item["factor_id"]): float(item["score"]) for item in factor_scores}
    if len(scores) != len(factor_scores):
        raise ValueError("factor_scores must not contain duplicate factor_id values")
    if set(scores) != set(weights):
        raise ValueError("entity scores must cover exactly the axis evaluation factors")
    return calculate_weighted_score(scores, weights)


def apply_backend_calculations(page_id: str, result: dict[str, Any]) -> dict[str, Any]:
    """Attach deterministic coordinates that the V2 design assigns to the backend."""
    data = result.get("data", {})
    if page_id == "10":
        coordinates: dict[str, dict[str, Any]] = {}
        for persona_id, factor_values in data.get("value_fit_inputs", {}).items():
            scores = {
                factor_id: value.get("score") if isinstance(value, dict) else value
                for factor_id, value in factor_values.items()
            }
            coordinates[persona_id] = calculate_vpc_coordinates(scores)
        data["computed_coordinates"] = coordinates
        for vpc in data.get("persona_vpcs", []):
            persona_id = str(vpc.get("persona_id"))
            if persona_id in coordinates:
                vpc["computed_coordinates"] = coordinates[persona_id]
    elif page_id == "05":
        axes = {axis_id: data.get(axis_id, {}) for axis_id in ("axis_x", "axis_y")}
        coordinate_map: dict[str, dict[str, float]] = {}
        for entity in data.get("entities", []):
            factor_scores = {str(item["factor_id"]): item for item in entity.get("factor_scores", [])}
            computed: dict[str, float] = {}
            for axis_id, coordinate_key in (("axis_x", "x"), ("axis_y", "y")):
                factors = axes[axis_id].get("evaluation_factors", [])
                relevant_scores = [factor_scores[str(factor["factor_id"])] for factor in factors]
                computed[coordinate_key] = round(
                    calculate_positioning_axis_score(relevant_scores, factors), 2
                )
            entity["computed_coordinates"] = computed
            coordinate_map[str(entity.get("entity_id"))] = computed
        data["computed_coordinates"] = coordinate_map
    return result


def validate_tows_factor_links(
    tows_strategies: dict[str, list[dict[str, Any]]], swot_factor_ids: set[str]
) -> list[str]:
    """Ensure every TOWS strategy links only to factors produced on the SWOT page."""
    errors: list[str] = []
    for strategy_type in ("SO", "WO", "ST", "WT"):
        for strategy in tows_strategies.get(strategy_type, []):
            for factor_id in strategy.get("linked_factors", []):
                if factor_id not in swot_factor_ids:
                    errors.append(
                        f"{strategy.get('strategy_id', strategy_type)} references unknown SWOT factor {factor_id}"
                    )
    return errors


def validate_page_result(
    page_id: str,
    result: dict[str, Any],
    prior_pages: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    """Return contract violations; callers should repair only these errors."""
    errors: list[str] = []
    if page_id not in REPORT_PAGE_SPECS:
        return [f"unsupported page_id: {page_id}"]
    if result.get("page_id") != page_id:
        errors.append("page_id does not match requested page")
    if result.get("title") != REPORT_PAGE_SPECS[page_id]["title"]:
        errors.append("title does not match page contract")
    if result.get("status") not in {"complete", "insufficient_data", "to_validate"}:
        errors.append("status must be complete, insufficient_data, or to_validate")
    data = result.get("data")
    if not isinstance(data, dict):
        errors.append("data must be an object")
        return errors
    missing = [field for field in REQUIRED_DATA_KEYS[page_id] if field not in data]
    if missing:
        errors.append("data is missing required contract fields: " + ", ".join(missing))
    if result.get("confidence") not in {"low", "medium", "high"}:
        errors.append("confidence must be low, medium, or high")
    if not isinstance(result.get("source_ids", []), list):
        errors.append("source_ids must be an array")
    if not isinstance(result.get("validation_notes", []), list):
        errors.append("validation_notes must be an array")
    if page_id in {"07", "08"}:
        personas = data.get("personas")
        expected = 2
        if not isinstance(personas, list) or len(personas) != expected:
            errors.append(f"page {page_id} must contain exactly {expected} personas")
    if page_id == "16":
        expected_bmc = set(REQUIRED_DATA_KEYS["16"])
        if set(data).intersection(expected_bmc) != expected_bmc:
            errors.append("BMC must contain all nine canvas blocks and validation_plan")
    if page_id == "05":
        for axis_name in ("axis_x", "axis_y"):
            axis = data.get(axis_name)
            if isinstance(axis, dict):
                factors = axis.get("evaluation_factors", [])
                if not isinstance(factors, list) or not factors:
                    errors.append(f"{axis_name} needs evaluation_factors")
                    continue
                weights = []
                for factor in factors:
                    if not isinstance(factor, dict) or not factor.get("factor_id"):
                        errors.append(f"{axis_name} factors need factor_id and weight")
                        continue
                    try:
                        weight = float(factor.get("weight"))
                    except (TypeError, ValueError):
                        errors.append(f"{axis_name} weights must be numeric")
                        continue
                    if weight < 0:
                        errors.append(f"{axis_name} weights must be non-negative")
                    weights.append(weight)
                if weights and abs(sum(weights) - 1.0) > 1e-9:
                    errors.append(f"{axis_name} factor weights must sum to 1.0")
        axes = [
            data.get("axis_x") if isinstance(data.get("axis_x"), dict) else {},
            data.get("axis_y") if isinstance(data.get("axis_y"), dict) else {},
        ]
        axis_factor_lists = [
            axis.get("evaluation_factors") if isinstance(axis.get("evaluation_factors"), list) else []
            for axis in axes
        ]
        expected_factors = {
            str(factor.get("factor_id"))
            for factors in axis_factor_lists
            for factor in factors
            if isinstance(factor, dict) and factor.get("factor_id")
        }
        entities = data.get("entities", [])
        if not isinstance(entities, list) or not entities:
            errors.append("positioning must contain evaluated entities")
        else:
            for entity in entities:
                if not isinstance(entity, dict):
                    errors.append("positioning entities must be objects")
                    continue
                factor_scores = entity.get("factor_scores", [])
                if not isinstance(factor_scores, list) or not all(isinstance(item, dict) for item in factor_scores):
                    errors.append("positioning factor_scores must be an array of objects")
                    continue
                factor_ids = [str(item.get("factor_id")) for item in factor_scores]
                if set(factor_ids) != expected_factors or len(factor_ids) != len(set(factor_ids)):
                    errors.append("each positioning entity must score every shared factor exactly once")
                for factor_score in factor_scores:
                    score = factor_score.get("score")
                    if not isinstance(score, (int, float)) or not 0 <= score <= 100:
                        errors.append("positioning factor scores must be between 0 and 100")
                    if not factor_score.get("reasoning"):
                        errors.append("positioning factor scores need reasoning")
    if page_id == "14":
        for group, prefix in (("strengths", "S"), ("weaknesses", "W"), ("opportunities", "O"), ("threats", "T")):
            for item in data.get(group, []):
                if not str(item.get("id", "")).startswith(prefix):
                    errors.append(f"{group} item IDs must start with {prefix}")
    prior_pages = prior_pages or {}
    if page_id in {"07", "08"}:
        expected_ids = {"07": {"P1", "P2"}, "08": {"P3", "P4"}}[page_id]
        actual_ids = {str(item.get("persona_id")) for item in data.get("personas", [])}
        if actual_ids != expected_ids:
            errors.append(f"page {page_id} persona IDs must be {sorted(expected_ids)}")
    if page_id == "04" and "00" in prior_pages:
        expected_name = prior_pages["00"].get("data", {}).get("brand_name")
        actual_name = data.get("naming", {}).get("name")
        if expected_name and actual_name != expected_name:
            errors.append("naming.name must match the selected brand_name on page 00")
    if page_id in {"09", "10", "18"} and prior_pages:
        expected_persona_ids = set(build_consistency_manifest(prior_pages)["persona_ids"])
        if page_id == "09":
            actual_ids = {
                str(item.get("persona_id"))
                for item in data.get("comparison", [])
                if item.get("persona_id")
            }
            if len(actual_ids) != len(data.get("comparison", [])):
                errors.append("each comparison row must reference one persona_id")
        elif page_id == "10":
            actual_ids = {str(item.get("persona_id")) for item in data.get("persona_vpcs", [])}
        else:
            actual_ids = set(data.get("persona_ids", []))
        if expected_persona_ids and actual_ids != expected_persona_ids:
            errors.append("persona IDs must match the canonical P1–P4 set")
    if page_id == "15" and "14" in prior_pages:
        swot_ids = set(build_consistency_manifest(prior_pages)["swot_factor_ids"])
        errors.extend(validate_tows_factor_links(data, swot_ids))
    if page_id == "10" and "07" in prior_pages and "08" in prior_pages:
        expected_ids = set(build_consistency_manifest(prior_pages)["persona_ids"])
        vpcs = data.get("persona_vpcs", [])
        vpc_ids = {str(item.get("persona_id")) for item in vpcs}
        if vpc_ids != expected_ids:
            errors.append("page 10 must contain one VPC for each canonical persona ID")
        inputs = data.get("value_fit_inputs", {})
        if not isinstance(inputs, dict):
            errors.append("value_fit_inputs must be an object keyed by canonical persona ID")
            inputs = {}
        if set(inputs) != expected_ids:
            errors.append("value_fit_inputs must contain all and only the canonical persona IDs")
        for persona_id, factors in inputs.items():
            if not isinstance(factors, dict):
                errors.append(f"{persona_id} value_fit_inputs must be an object")
                continue
            if set(factors) != {"S", "F", "I", "A", "P", "G", "D", "C"}:
                errors.append(f"{persona_id} must include S/F/I/A/P/G/D/C scores")
                continue
            for factor_id, score_data in factors.items():
                score = score_data.get("score") if isinstance(score_data, dict) else score_data
                if not isinstance(score, (int, float)) or not 0 <= score <= 100:
                    errors.append(f"{persona_id}.{factor_id} score must be 0–100")
                if isinstance(score_data, dict) and not score_data.get("reasoning"):
                    errors.append(f"{persona_id}.{factor_id} needs reasoning")
    if page_id == "13":
        competitors = data.get("competitors", [])
        ids = [item.get("competitor_id") for item in competitors]
        if any(not value for value in ids) or len(ids) != len(set(ids)):
            errors.append("competitors must have unique, non-empty competitor_id values")
        if result.get("status") == "complete" and not 3 <= len(competitors) <= 5:
            errors.append("page 13 should prioritize 3 to 5 competitors")
    if page_id == "05" and "13" in prior_pages:
        expected_entities = {"our_idea"} | {
            str(item.get("competitor_id"))
            for item in prior_pages["13"].get("data", {}).get("competitors", [])
            if item.get("competitor_id")
        }
        actual_entities = {str(item.get("entity_id")) for item in data.get("entities", [])}
        if actual_entities != expected_entities:
            errors.append("positioning entities must reuse our_idea and page 13 competitor IDs")
    if page_id == "16":
        allowed_statuses = {"validated", "assumption", "to_validate"}
        for block in REQUIRED_DATA_KEYS["16"][:-1]:
            for item in data.get(block, []):
                if item.get("status") not in allowed_statuses:
                    errors.append(f"BMC {block} items need a valid status")
                if "evidence" not in item or "source_ids" not in item or "validation_method" not in item:
                    errors.append(f"BMC {block} items need evidence, source_ids, and validation_method")
    if page_id == "05":
        for axis_name in ("axis_x", "axis_y"):
            axis = data.get(axis_name)
            if not isinstance(axis, dict):
                continue
            factor_ids = {item.get("factor_id") for item in axis.get("evaluation_factors", [])}
            for entity in data.get("entities", []):
                scored_ids = {item.get("factor_id") for item in entity.get("factor_scores", [])}
                if scored_ids and not factor_ids.issubset(scored_ids):
                    errors.append(f"all entities must be evaluated on the {axis_name} factors")
    return errors


def build_repair_prompt(
    page_id: str,
    prior_result: dict[str, Any],
    errors: list[str],
    canonical_state: dict[str, Any] | None = None,
) -> str:
    """Ask for a schema repair while preserving valid content and its evidence."""
    return f"""수정 대상은 NAME TAG V2 보고서 {page_id} 페이지입니다.
아래 오류만 고치고, 오류가 없는 내용·점수·근거·source_ids는 유지하세요.
외부 사실이나 입력에 없는 값을 만들어내지 마세요.
오류: {json.dumps(errors, ensure_ascii=False)}
기존 결과: {json.dumps(prior_result, ensure_ascii=False, default=str)}
확정된 공통 기준: {json.dumps(canonical_state or {}, ensure_ascii=False, default=str)}
페이지 계약: {json.dumps(REPORT_PAGE_SPECS[page_id], ensure_ascii=False)}
유효한 JSON 객체 하나만 반환하세요."""


def next_report_pages(
    completed_page_ids: set[str],
    skipped_page_ids: set[str] | None = None,
    conditional_decisions: dict[str, bool] | None = None,
) -> list[str]:
    """Return ready pages; conditional pages require an explicit enabled decision."""
    skipped_page_ids = skipped_page_ids or set()
    conditional_decisions = conditional_decisions or {}
    resolved_page_ids = completed_page_ids | skipped_page_ids
    ready = []
    for page_id in REPORT_PAGE_ORDER:
        if page_id in resolved_page_ids:
            continue
        if REPORT_PAGE_SPECS[page_id].get("conditional"):
            if page_id not in conditional_decisions or not conditional_decisions[page_id]:
                continue
        deps = set(REPORT_PAGE_SPECS[page_id]["deps"])
        if deps.issubset(resolved_page_ids):
            ready.append(page_id)
    return ready


def build_interview_generation_plan() -> list[dict[str, Any]]:
    """Return the intake interviews and the report inputs they inform."""
    return [
        {"interview_id": interview_id, **spec}
        for interview_id, spec in INTERVIEW_SPECS.items()
    ]


def next_report_interviews(
    completed_page_ids: set[str],
    completed_interview_ids: set[str],
) -> list[str]:
    """Return interviews unlocked by their required completed context pages."""
    return [
        interview_id for interview_id, spec in INTERVIEW_SPECS.items()
        if interview_id not in completed_interview_ids
        and set(spec["context_pages"]).issubset(completed_page_ids)
    ]


class ReportHarness:
    """Thin orchestration harness around an injected JSON-generating model client.

    The caller supplies generate_json(prompt) -> dict. This class does not perform
    network calls, market research, PDF rendering, or persistence on its own.
    """

    def __init__(
        self,
        generate_json: Callable[[str], dict[str, Any]],
        max_repairs: int = 1,
        completed_pages: dict[str, dict[str, Any]] | None = None,
    ):
        self.generate_json = generate_json
        self.max_repairs = max(0, max_repairs)
        self.completed_pages = deepcopy(completed_pages or {})
        self.skipped_page_ids: set[str] = set()
        self.conditional_decisions: dict[str, bool] = {}
        self.interviews: dict[str, dict[str, Any]] = {}
        self.interview_answers: dict[str, Any] = {}
        self.invalidated_page_ids: set[str] = set()

    def set_conditional_decision(self, page_id: str, enabled: bool) -> None:
        if page_id not in {"17", "21"}:
            raise ValueError("only Lean Canvas (17) and Character Identity (21) are conditional")
        self.conditional_decisions[page_id] = enabled
        if not enabled:
            self.skip_page(page_id)
        else:
            self.skipped_page_ids.discard(page_id)

    def skip_page(self, page_id: str) -> None:
        """Mark a deliberately omitted conditional page as resolved for dependencies."""
        if not REPORT_PAGE_SPECS.get(page_id, {}).get("conditional"):
            raise ValueError(f"page {page_id} is not conditional")
        self.completed_pages.pop(page_id, None)
        self.skipped_page_ids.add(page_id)

    def generate_interview(self, interview_id: str, context: dict[str, Any]) -> dict[str, Any]:
        pages = {**context.get("pages", {}), **self.completed_pages}
        enriched_context = {
            **context,
            "pages": pages,
            "canonical_state": build_consistency_manifest(pages),
            "prior_interviews": self.interviews,
            "interview_answers": self.interview_answers,
        }
        prompt = build_report_interview_prompt(interview_id, enriched_context)
        result = self.generate_json(prompt)
        for _ in range(self.max_repairs):
            errors = validate_interview_result(result)
            if not errors:
                self.interviews[interview_id] = result
                return result
            repair_prompt = (
                prompt
                + "\n이전 응답의 형식 오류만 수정하세요. 오류: "
                + json.dumps(errors, ensure_ascii=False)
                + "\n이전 응답: "
                + json.dumps(result, ensure_ascii=False, default=str)
            )
            result = self.generate_json(repair_prompt)
        errors = validate_interview_result(result)
        if errors:
            raise ValueError("interview response failed validation: " + "; ".join(errors))
        self.interviews[interview_id] = result
        return result

    def record_interview_answers(self, interview_id: str, answers: Any) -> set[str]:
        """Store submitted interview answers separately from generated questions."""
        if interview_id not in INTERVIEW_SPECS:
            raise ValueError(f"Unsupported interview_id: {interview_id}")
        if interview_id not in self.interviews:
            raise ValueError(f"generate interview {interview_id} before recording its answers")
        if interview_id in self.interview_answers and self.interview_answers[interview_id] != answers:
            roots = {
                page_id for page_id, interview_ids in REQUIRED_INTERVIEWS_BY_PAGE.items()
                if interview_id in interview_ids
            }
            invalidated: set[str] = set()
            for root in roots:
                invalidated.update(downstream_page_ids(root))
            for page_id in invalidated:
                self.completed_pages.pop(page_id, None)
            self.invalidated_page_ids.update(invalidated)
        self.interview_answers[interview_id] = deepcopy(answers)
        return set(self.invalidated_page_ids)

    def get_invalidated_page_ids(self) -> set[str]:
        """Return IDs the persistence layer should delete or regenerate."""
        return set(self.invalidated_page_ids)

    def ready_interviews(self) -> list[str]:
        """List interviews that can use the current canonical report state."""
        return next_report_interviews(
            set(self.completed_pages), set(self.interview_answers)
        )

    def generate_page(
        self, page_id: str, context: dict[str, Any], *, regenerate: bool = False
    ) -> dict[str, Any]:
        if (page_id in self.completed_pages or page_id in context.get("pages", {})) and not regenerate:
            raise ValueError(f"page {page_id} already exists; use regenerate=True to replace it")
        context_pages = dict(context.get("pages", {}))
        if regenerate:
            invalidated = downstream_page_ids(page_id)
            for dependent_id in invalidated:
                self.completed_pages.pop(dependent_id, None)
                context_pages.pop(dependent_id, None)
                self.skipped_page_ids.discard(dependent_id)
            self.invalidated_page_ids.update(invalidated)
        for invalidated_id in self.invalidated_page_ids:
            context_pages.pop(invalidated_id, None)
        pages = {**context_pages, **self.completed_pages}
        if REPORT_PAGE_SPECS[page_id].get("conditional"):
            if page_id not in self.conditional_decisions:
                raise ValueError(f"set the conditional decision for page {page_id} before generation")
            if not self.conditional_decisions[page_id]:
                self.skip_page(page_id)
                return {"page_id": page_id, "skipped": True, "reason": "conditional page disabled"}
        resolved = set(pages) | self.skipped_page_ids
        missing_deps = set(REPORT_PAGE_SPECS[page_id]["deps"]) - resolved
        if missing_deps:
            raise ValueError(f"page {page_id} requires completed pages: {sorted(missing_deps)}")
        provided_answers = {**self.interview_answers, **context.get("interview_answers", {})}
        missing_interviews = set(REQUIRED_INTERVIEWS_BY_PAGE.get(page_id, [])) - set(provided_answers)
        if missing_interviews:
            raise ValueError(f"page {page_id} requires recorded interview answers: {sorted(missing_interviews)}")
        enriched_context = {
            **context,
            "pages": pages,
            "canonical_state": build_consistency_manifest(pages),
            "interview_answers": provided_answers,
            "skipped_page_ids": sorted(self.skipped_page_ids),
        }
        prompt = build_named_report_page_prompt(page_id, enriched_context)
        result = self.generate_json(prompt)
        for _ in range(self.max_repairs):
            errors = validate_page_result(page_id, result, pages)
            if not errors:
                result = apply_backend_calculations(page_id, result)
                self.completed_pages[page_id] = result
                self.invalidated_page_ids.discard(page_id)
                return result
            result = self.generate_json(
                build_repair_prompt(page_id, result, errors, build_consistency_manifest(pages))
            )
        errors = validate_page_result(page_id, result, pages)
        if errors:
            raise ValueError(f"page {page_id} failed validation: " + "; ".join(errors))
        result = apply_backend_calculations(page_id, result)
        self.completed_pages[page_id] = result
        self.invalidated_page_ids.discard(page_id)
        return result

    def generate_ready_pages(
        self, context: dict[str, Any], limit: int | None = None
    ) -> list[dict[str, Any]]:
        """Generate pages whose dependencies are resolved, using latest canonical state each time."""
        external_page_ids = set(context.get("pages", {}))
        external_page_ids.difference_update(self.invalidated_page_ids)
        resolved = set(self.completed_pages) | external_page_ids | self.skipped_page_ids
        ready = next_report_pages(resolved, self.skipped_page_ids, self.conditional_decisions)
        provided_answers = {**self.interview_answers, **context.get("interview_answers", {})}
        ready = [
            page_id for page_id in ready
            if set(REQUIRED_INTERVIEWS_BY_PAGE.get(page_id, [])).issubset(provided_answers)
        ]
        if limit is not None:
            ready = ready[:limit]
        return [self.generate_page(page_id, context) for page_id in ready]
