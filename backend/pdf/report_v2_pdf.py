from __future__ import annotations

import html
import re
from typing import Any, Callable


PAGE_ORDER = tuple(f"{page_id:02d}" for page_id in range(25))
PAGE_TITLES = {
    "00": ("Cover", "브랜드 전략 보고서"),
    "01": ("Executive Summary", "브랜드·사업 핵심 요약"),
    "02": ("Brand Foundation", "브랜드의 존재 이유"),
    "03": ("Brand Identity", "브랜드의 성격과 인상"),
    "04": ("Brand Story", "브랜드가 만들어진 이야기"),
    "05": ("Brand Positioning", "시장에서 차지할 자리"),
    "06": ("Business Overview", "현재 사업의 모습"),
    "07": ("Customer Personas 01–02", "핵심 고객 페르소나"),
    "08": ("Customer Personas 03–04", "확장 고객 페르소나"),
    "09": ("Persona Comparison", "고객 우선순위 비교"),
    "10": ("Value Proposition", "고객별 가치 적합도"),
    "11": ("Market Analysis", "시장 구조와 성공 요인"),
    "12": ("Market Size", "TAM · SAM · SOM"),
    "13": ("Competitor Analysis", "경쟁 환경과 차별화 기회"),
    "14": ("SWOT Analysis", "사업의 현재 위치 진단"),
    "15": ("TOWS Strategy", "진단을 실행으로 전환"),
    "16": ("Business Model Canvas", "비즈니스 모델 캔버스"),
    "17": ("Lean Canvas", "초기 사업 가설 검증"),
    "18": ("Customer Journey", "고객 경험 흐름"),
    "19": ("Visual Identity", "브랜드의 시각 언어"),
    "20": ("Logo Identity", "브랜드 상징과 사용 규칙"),
    "21": ("Character Identity", "브랜드 캐릭터"),
    "22": ("Brand Applications", "브랜드 접점 적용"),
    "23": ("Validation Roadmap", "30 · 60 · 90일 실행 계획"),
    "24": ("Research Evidence", "근거와 한계"),
}

DEFAULT_PAGE_LAYOUTS: dict[str, tuple[str, str, int]] = {
    "00": ("A4", "portrait", 12),
    "01": ("A4", "portrait", 12),
    "02": ("A4", "portrait", 12),
    "03": ("A3", "portrait", 15),
    "04": ("A4", "portrait", 12),
    "05": ("A3", "landscape", 15),
    "06": ("A4", "portrait", 12),
    "07": ("A3", "portrait", 15),
    "08": ("A3", "portrait", 15),
    "09": ("A3", "landscape", 15),
    "10": ("A3", "landscape", 15),
    "11": ("A4", "landscape", 12),
    "12": ("A3", "landscape", 15),
    "13": ("A4", "landscape", 12),
    "14": ("A4", "landscape", 12),
    "15": ("A4", "landscape", 12),
    "16": ("A3", "landscape", 15),
    "17": ("A3", "landscape", 15),
    "18": ("A3", "landscape", 15),
    "19": ("A4", "portrait", 12),
    "20": ("A4", "portrait", 12),
    "21": ("A4", "portrait", 12),
    "22": ("A4", "landscape", 12),
    "23": ("A4", "landscape", 12),
    "24": ("A4", "portrait", 12),
}

LABELS = {
    "brand_name": "브랜드명",
    "industry": "업종 / 산업",
    "business_type": "사업 유형",
    "report_version": "보고서 버전",
    "report_date": "작성일",
    "key_sentence": "브랜드 핵심 문장",
    "brand_promise": "브랜드 약속",
    "brand_thesis": "Brand Thesis",
    "key_metrics": "핵심 지표",
    "key_findings_3": "핵심 발견",
    "key_strategies_3": "핵심 전략",
    "priority_actions": "우선 실행 과제",
    "golden_circle": "Golden Circle",
    "why": "Why · 존재 이유",
    "how": "How · 고유한 방식",
    "what": "What · 제품·서비스",
    "brand_essence": "Brand Essence",
    "identity_prism": "Identity Prism",
    "core_values": "핵심 가치",
    "archetype": "브랜드 원형",
    "personas": "고객 페르소나",
    "persona_id": "페르소나 ID",
    "computed_coordinates": "백엔드 계산 좌표",
    "source_ids": "출처 ID",
    "confidence": "신뢰도",
    "evidence_type": "근거 유형",
    "strategic_insight": "전략 인사이트",
    "validation_notes": "검증 메모",
    "brand_thesis": "브랜드 핵심 명제",
    "key_findings": "핵심 발견",
    "key_strategies": "핵심 전략",
    "priority_actions": "우선 실행 과제",
    "calculation_basis": "산출 기준",
    "golden_circle": "골든 서클",
    "how": "How · 고유한 방식",
    "what": "What · 제품·서비스",
    "identity_prism": "브랜드 아이덴티티 프리즘",
    "physique": "외형",
    "personality": "성격",
    "culture": "문화",
    "relationship": "관계",
    "reflection": "고객 반영 이미지",
    "self_image": "고객의 자기 이미지",
    "core_values": "핵심 가치",
    "naming": "이름의 의미",
    "meaning": "이름에 담긴 의미",
    "pronunciation": "발음",
    "symbolism": "상징성",
    "origin": "브랜드의 시작",
    "belief": "브랜드의 믿음",
    "promise": "브랜드 약속",
    "slogan": "슬로건",
    "axis_x": "가로축",
    "axis_y": "세로축",
    "name": "이름",
    "description": "설명",
    "low_anchor": "낮은 기준점",
    "high_anchor": "높은 기준점",
    "evaluation_factors": "평가 요소",
    "weight": "가중치",
    "entities": "비교 대상",
    "entity_id": "대상 ID",
    "entity_type": "대상 유형",
    "factor_scores": "요인별 점수",
    "computed_coordinates": "계산된 좌표",
    "pop": "필수 조건",
    "pod": "차별 요소",
    "brand_mantra": "브랜드 만트라",
    "strategic_implication": "전략적 시사점",
    "business_stage": "사업 단계",
    "products_services": "제품·서비스",
    "resources": "보유 자원",
    "current_performance": "현재 성과",
    "constraints": "제약 조건",
    "age_range": "연령대",
    "occupation_or_situation": "직업·생활 상황",
    "lifestyle": "생활 방식",
    "background": "배경",
    "customer_jobs": "고객이 해결하려는 일",
    "behavior": "행동 특성",
    "behaviors": "행동 특성",
    "purchase_criteria": "구매 기준",
    "pains": "불편·고충",
    "gains": "기대하는 이점",
    "motivation": "구매 동기",
    "barriers": "구매 장벽",
    "alternatives": "현재 대안",
    "quote": "고객의 목소리",
    "product_expectations": "제품 기대",
    "product_concerns": "제품 우려",
    "generation_basis": "작성 근거",
    "comparison": "페르소나 비교",
    "criteria": "비교 기준",
    "segment_label": "고객 유형",
    "shared_problems": "공통 문제",
    "differences": "고객별 차이",
    "priority_segment": "우선 공략 고객",
    "persona_vpcs": "고객별 가치 적합도",
    "value_fit_inputs": "가치 적합도 입력값",
    "problem_intensity": "문제 강도",
    "frequency": "문제 발생 빈도",
    "solution_intent": "해결 의향",
    "willingness_to_pay": "지불 의향",
    "accessibility": "접근 가능성",
    "three_c": "3C 분석",
    "five_forces": "5가지 경쟁 요인",
    "company": "자사",
    "customer": "고객",
    "competitor": "경쟁사",
    "key_success_factors": "핵심 성공 요인",
    "market_attractiveness": "시장 매력도",
    "tam": "전체 시장 · TAM",
    "sam": "유효 시장 · SAM",
    "som": "초기 목표 시장 · SOM",
    "amount": "시장 규모",
    "customer_count": "고객 수",
    "revenue_per_customer_year": "연간 고객당 매출",
    "calculation_method": "산출 방법",
    "assumptions": "가정",
    "exclusions": "제외 범위",
    "competitors": "경쟁사",
    "comparison_summary": "비교 요약",
    "market_gaps": "시장 공백",
    "recommended_differentiation": "차별화 제안",
    "strengths": "강점 · 내부",
    "weaknesses": "약점 · 내부",
    "opportunities": "기회 · 외부",
    "threats": "위협 · 외부",
    "factor": "진단 요인",
    "impact": "영향도",
    "SO": "강점을 살려 기회를 잡는 전략",
    "WO": "약점을 보완해 기회를 잡는 전략",
    "ST": "강점으로 위협에 대응하는 전략",
    "WT": "약점과 위협을 줄이는 전략",
    "strategy": "전략",
    "linked_factors": "연결 요인",
    "first_action": "첫 실행",
    "success_metric": "성공 지표",
    "estimated_cost": "예상 비용",
    "customer_segments": "고객 세그먼트",
    "value_propositions": "가치 제안",
    "channels": "고객 접점·채널",
    "customer_relationships": "고객 관계",
    "revenue_streams": "수익원",
    "key_resources": "핵심 자원",
    "key_activities": "핵심 활동",
    "key_partners": "핵심 파트너",
    "cost_structure": "비용 구조",
    "validation_plan": "검증 계획",
    "hypothesis": "가설",
    "method": "검증 방법",
    "success_metric": "성공 지표",
    "stages": "고객 여정 단계",
    "stage": "단계",
    "touchpoints": "접점",
    "touchpoint": "접점",
    "customer_actions": "고객 행동",
    "customer_emotions": "고객 감정",
    "brand_response": "브랜드 대응",
    "channels_and_relationship_consistency": "채널·관계 일관성",
    "color_palette": "색상 팔레트",
    "hex": "색상 코드",
    "typography": "서체 방향",
    "image_mood": "이미지 분위기",
    "design_principles": "디자인 원칙",
    "concept": "콘셉트",
    "symbol": "심볼",
    "wordmark": "워드마크",
    "usage_rules": "사용 규칙",
    "minimum_size": "최소 사용 크기",
    "clear_space": "주변 여백",
    "character_identity": "캐릭터 정체성",
    "symbolic_value": "상징 가치",
    "emotional_connection": "감정적 연결",
    "applications": "브랜드 적용 지점",
    "brand_consistency_notes": "브랜드 일관성 메모",
    "plan_30_60_90_days": "30·60·90일 실행 계획",
    "validation_hypotheses": "검증할 가설",
    "kpis": "핵심 성과 지표",
    "owners": "담당자",
    "timeline": "일정",
    "sources": "출처",
    "source_ids": "출처 ID",
    "calculation_assumptions": "계산 가정",
    "limitations": "자료의 한계",
    "validation_records": "검증 기록",
    "evidence_types": "근거 유형",
    "evidence_type": "근거 유형",
    "confidence": "신뢰도",
    "status": "검증 상태",
    "statement": "내용",
    "evidence": "근거",
    "validation_method": "검증 방법",
    "source_ids": "출처 ID",
    "score": "점수",
    "reasoning": "평가 이유",
    "formula": "산식",
    "period": "기간",
    "actions": "실행 내용",
    "owner": "담당자",
    "role": "역할",
}


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _render_inline_markdown(value: Any) -> str:
    """Render safe **bold** spans from AI-authored body text."""
    text = str(value)
    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", text, flags=re.DOTALL):
        parts.append(_e(text[cursor:match.start()]))
        parts.append(f'<strong class="emphasis">{_e(match.group(1))}</strong>')
        cursor = match.end()
    parts.append(_e(text[cursor:]))
    return "".join(parts)


def _page_name(page_id: str) -> str:
    if page_id not in PAGE_TITLES:
        raise ValueError(f"Unsupported report page ID: {page_id}")
    return f"report_{page_id}"


def _label(key: Any) -> str:
    text = str(key)
    return LABELS.get(text, text.replace("_", " ").strip().capitalize())


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _render_value(label: str, value: Any, depth: int = 0) -> str:
    """Render nested page JSON as readable report components, never raw JSON."""
    if _is_missing(value):
        return (
            f'<div class="field"><div class="field-label">{_e(label)}</div>'
            '<div class="missing">추가 정보 필요</div></div>'
        )
    if isinstance(value, dict):
        children = "".join(
            _render_value(_label(key), child, depth + 1)
            for key, child in value.items()
            if key != "validation_notes"
        )
        return (
            f'<section class="data-group depth-{min(depth, 3)}"><h3>{_e(label)}</h3>'
            f'<div class="data-grid">{children}</div></section>'
        )
    if isinstance(value, list):
        if not value:
            return f'<div class="field"><div class="field-label">{_e(label)}</div><div class="missing">추가 정보 필요</div></div>'
        if all(not isinstance(item, (dict, list)) for item in value):
            items = "".join(f"<li>{_render_inline_markdown(item)}</li>" for item in value)
            return f'<section class="field"><div class="field-label">{_e(label)}</div><ul class="tag-list">{items}</ul></section>'
        cards = []
        for index, item in enumerate(value, start=1):
            item_label = item.get("persona_id") or item.get("id") or item.get("name") if isinstance(item, dict) else None
            title = _e(item_label or f"{label} {index}")
            body = _render_value("세부 내용", item, depth + 1)
            cards.append(f'<article class="item-card"><h4>{title}</h4>{body}</article>')
        return f'<section class="field"><div class="field-label">{_e(label)}</div><div class="item-grid">{"".join(cards)}</div></section>'
    if isinstance(value, bool):
        display = "예" if value else "아니요"
    else:
        display = str(value)
    return f'<div class="field"><div class="field-label">{_e(label)}</div><div class="field-value">{_render_inline_markdown(display)}</div></div>'


def _render_structured_data(data: dict[str, Any]) -> str:
    content = "".join(_render_value(_label(key), value) for key, value in data.items())
    return content or '<div class="empty-state">이 페이지에 표시할 데이터가 없습니다.</div>'


def _source_meta(page: dict[str, Any]) -> str:
    status = page.get("status", "")
    status_labels = {
        "complete": "완료",
        "insufficient_data": "추가 정보 필요",
        "to_validate": "검증 필요",
    }
    evidence_type = page.get("evidence_type", "")
    evidence_label = "AI 평가 / 추정" if str(evidence_type).startswith("ai_") or evidence_type == "ai_estimate" else evidence_type
    meta = [
        f'<span>상태 · {_e(status_labels.get(status, status or "미지정"))}</span>',
        f'<span>신뢰도 · {_e(page.get("confidence", "미지정"))}</span>',
        f'<span>근거 · {_e(evidence_label or "미지정")}</span>',
    ]
    source_ids = page.get("source_ids") or []
    meta.append(f'<span>출처 ID · {_e(", ".join(map(str, source_ids)) if source_ids else "없음")}</span>')
    notes = page.get("validation_notes") or []
    if notes:
        meta.append(f'<span class="validation-note">검증 메모 · {_e(" · ".join(map(str, notes)))}</span>')
    return "".join(meta)


def _standard_page(page_id: str, page: dict[str, Any], content: str, *, cover: bool = False) -> str:
    english_title, korean_title = PAGE_TITLES[page_id]
    title = page.get("title") or english_title
    data = page.get("data") if isinstance(page.get("data"), dict) else {}
    if cover:
        brand_name = data.get("brand_name") or "추가 정보 필요"
        key_sentence = data.get("key_sentence") or "브랜드의 본질부터 사업 전략, 시각적 정체성까지"
        brand_promise = data.get("brand_promise")
        cover_promise = f'<p class="cover-promise">{_render_inline_markdown(brand_promise)}</p>' if brand_promise else ""
        return (
            f'<section class="report-page cover-page" style="page: {_page_name(page_id)}">'
            '<div class="cover-top"><span>NAME TAG · BRAND & BUSINESS STRATEGY</span>'
            f'<span>{_e(data.get("report_version") or "브랜드 전략 보고서")}</span></div>'
            '<div class="cover-main"><div class="cover-kicker">BUILD A BRAND THAT MEANS BUSINESS</div>'
            f'<h1>{_e(brand_name)}</h1><p class="cover-copy">{_render_inline_markdown(key_sentence)}</p>{cover_promise}'
            '<div class="cover-facts">'
            f'<div><small>업종 / 산업</small><strong>{_e(data.get("industry") or "추가 정보 필요")}</strong></div>'
            f'<div><small>보고서 버전</small><strong>{_e(data.get("report_version") or "브랜드 전략 보고서")}</strong></div>'
            f'<div><small>작성일</small><strong>{_e(data.get("report_date") or "입력값 필요")}</strong></div>'
            '</div></div>'
            '<div class="cover-bottom"><span>브랜드의 본질부터 사업 전략, 시각적 정체성까지</span>'
            f'<span>00 · {_e(title)}</span></div></section>'
        )
    return (
        f'<section class="report-page page-{page_id}" style="page: {_page_name(page_id)}">'
        f'<header class="page-header"><div><div class="eyebrow">NAME TAG · BRAND & BUSINESS REPORT · {page_id}</div>'
        f'<h1>{_e(title)}</h1><div class="subtitle">{_e(korean_title)}</div></div>'
        f'<div class="page-meta">{_source_meta(page)}</div></header>'
        f'<main class="page-content">{content}</main>'
        f'<footer class="page-footer"><span>NAME TAG · BRAND & BUSINESS STRATEGY</span><span>{page_id} / 25</span></footer>'
        '</section>'
    )


def build_00_cover_page(page: dict[str, Any]) -> str:
    return _standard_page("00", page, "", cover=True)


def _build_generic(page_id: str, page: dict[str, Any]) -> str:
    data = page.get("data") if isinstance(page.get("data"), dict) else {}
    return _standard_page(page_id, page, _render_structured_data(data))


def build_01_executive_summary_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    thesis = data.get("brand_thesis") or "핵심 요약을 추가 정보와 함께 확인하세요."
    metrics = data.get("key_metrics", [])
    findings = data.get("key_findings_3", [])
    strategies = data.get("key_strategies_3", [])
    content = (
        f'<div class="thesis">{_e(thesis)}</div>'
        f'<section class="metric-grid">{_render_value("핵심 지표", metrics)}</section>'
        f'<div class="two-column">{_render_value("핵심 발견", findings)}{_render_value("핵심 전략", strategies)}</div>'
        f'{_render_value("우선 실행 과제", data.get("priority_actions"))}'
        f'{_render_value("산출 기준", data.get("calculation_basis"))}'
    )
    return _standard_page("01", page, content)


def build_02_brand_foundation_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    circle = data.get("golden_circle") if isinstance(data.get("golden_circle"), dict) else {}
    circle_cards = "".join(
        f'<article class="golden-card golden-{key}"><span>{label}</span>{_render_value(label, circle.get(key))}</article>'
        for key, label in (("why", "WHY · 존재 이유"), ("how", "HOW · 고유한 방식"), ("what", "WHAT · 제품과 서비스"))
    )
    content = (
        f'<div class="golden-circle">{circle_cards}</div>'
        f'<div class="essence-panel"><span>BRAND ESSENCE</span>{_render_value("브랜드 에센스", data.get("brand_essence"))}</div>'
        f'{_render_value("고객 문제와의 연결", data.get("customer_connection"))}'
    )
    return _standard_page("02", page, content)


def build_03_brand_identity_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    prism = data.get("identity_prism") if isinstance(data.get("identity_prism"), dict) else {}
    prism_order = ("physique", "personality", "culture", "relationship", "reflection", "self_image")
    prism_labels = {
        "physique": "Physique · 외형", "personality": "Personality · 성격",
        "culture": "Culture · 문화", "relationship": "Relationship · 관계",
        "reflection": "Reflection · 반영", "self_image": "Self-image · 자아 이미지",
    }
    prism_cards = "".join(
        f'<article class="prism-card"><span>{prism_labels[key]}</span>{_render_value(prism_labels[key], prism.get(key))}</article>'
        for key in prism_order
    )
    content = (
        f'<section class="prism-panel"><div class="section-kicker">BRAND IDENTITY PRISM</div>'
        f'<div class="prism-grid">{prism_cards}</div></section>'
        f'<div class="identity-lower"><div>{_render_value("브랜드 원형", data.get("archetype"))}</div>'
        f'<div>{_render_value("핵심 가치", data.get("core_values_3_to_5") or data.get("core_values"))}</div></div>'
        f'{_render_value("행동 정의", data.get("behavior_definitions"))}'
    )
    return _standard_page("03", page, content)


def build_04_brand_story_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    story = data.get("story") if isinstance(data.get("story"), dict) else {}
    story_steps = (("origin", "ORIGIN", "시작"), ("problem", "PROBLEM", "문제"), ("belief", "BELIEF", "믿음"), ("promise", "PROMISE", "약속"))
    steps = "".join(
        f'<article class="story-step"><span>{index:02d}</span><div class="section-kicker">{eyebrow}</div>'
        f'<h2>{label}</h2>{_render_value(label, story.get(key))}</article>'
        for index, (key, eyebrow, label) in enumerate(story_steps, start=1)
    )
    content = (
        f'{_render_value("네이밍의 의미와 상징", data.get("naming_origin_meaning_pronunciation_symbolism"))}'
        f'<div class="story-flow">{steps}</div>'
        f'<div class="slogan-panel">{_render_value("브랜드 슬로건", data.get("slogan"))}</div>'
        f'{_render_value("창업자 경험 관련 검증", data.get("founder_experience_is_not_fabricated"))}'
    )
    return _standard_page("04", page, content)


def _coordinate_svg(entities: list[dict[str, Any]], x_axis: dict[str, Any], y_axis: dict[str, Any]) -> str:
    points = []
    for entity_index, entity in enumerate(entities):
        coords = entity.get("computed_coordinates") or {}
        try:
            x_value = float(coords["x"])
            y_value = float(coords["y"])
        except (KeyError, TypeError, ValueError):
            continue
        if not (0 <= x_value <= 100 and 0 <= y_value <= 100):
            continue
        x = 48 + x_value * 4.65
        y = 236 - y_value * 2.05
        label_rank = 0
        for prior in entities[:entity_index]:
            prior_coords = prior.get("computed_coordinates") or {}
            try:
                if float(prior_coords["x"]) == x_value and float(prior_coords["y"]) == y_value:
                    label_rank += 1
            except (KeyError, TypeError, ValueError):
                continue
        label_y = y - 6 - 13 * label_rank if y > 170 else y - 6 + 13 * label_rank
        label = _e(entity.get("name") or entity.get("entity_id") or "대상")
        entity_id = _e(entity.get("entity_id") or "")
        points.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="plot-point" fill="#a96535" stroke="#ffffff" stroke-width="2"/>'
            f'<text x="{x + 12:.1f}" y="{label_y:.1f}" class="plot-label" fill="#514d45" font-size="13.5">{label or entity_id}</text>'
        )
    x_name = _e(x_axis.get("name") or "X축")
    y_name = _e(y_axis.get("name") or "Y축")
    return (
        '<svg class="quadrant-chart" viewBox="0 0 560 300" role="img" aria-label="포지셔닝 사분면">'
        '<rect x="48" y="31" width="465" height="205" class="quadrant-bg" fill="#faf9f5" stroke="#cfc9bd" stroke-width="1"/>'
        '<line x1="280.5" y1="31" x2="280.5" y2="236" class="axis-line" stroke="#b9b2a6" stroke-dasharray="4 4" stroke-width="1"/>'
        '<line x1="48" y1="133.5" x2="513" y2="133.5" class="axis-line" stroke="#b9b2a6" stroke-dasharray="4 4" stroke-width="1"/>'
        '<text x="48" y="270" class="axis-label" fill="#514d45" font-size="13.5">0</text><text x="495" y="270" class="axis-label" fill="#514d45" font-size="13.5">100</text>'
        f'<text x="225" y="294" class="axis-title" fill="#514d45" font-size="14.5" font-weight="700">{x_name}</text>'
        f'<text x="10" y="18" class="axis-title" fill="#514d45" font-size="14.5" font-weight="700">{y_name}</text>'
        f'{"".join(points)}'
        '</svg>'
    )


def _axis_summary(label: str, axis: dict[str, Any]) -> str:
    factors = axis.get("evaluation_factors") if isinstance(axis.get("evaluation_factors"), list) else []
    factor_rows = []
    for factor in factors:
        if not isinstance(factor, dict):
            continue
        factor_rows.append(
            "<tr>"
            f'<td>{_e(factor.get("factor_id", ""))}</td>'
            f'<td>{_e(factor.get("name", ""))}</td>'
            f'<td>{_e(factor.get("weight", ""))}</td>'
            "</tr>"
        )
    table = (
        f'<table class="compact-table"><thead><tr><th>요소 ID</th><th>평가 요소</th><th>가중치</th></tr></thead>'
        f'<tbody>{"".join(factor_rows)}</tbody></table>'
        if factor_rows else '<div class="missing">평가 요소 추가 필요</div>'
    )
    return (
        f'<section class="axis-card"><h3>{_e(axis.get("name") or label)}</h3>'
        f'<div class="axis-description">{_e(axis.get("description") or "축 정의 추가 필요")}</div>'
        f'<div class="axis-anchors"><span>낮음 · {_e(axis.get("low_anchor") or "정의 필요")}</span>'
        f'<span>높음 · {_e(axis.get("high_anchor") or "정의 필요")}</span></div>{table}</section>'
    )


def _positioning_entity_table(entities: list[dict[str, Any]]) -> str:
    rows = []
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        coords = entity.get("computed_coordinates") or {}
        factor_scores = entity.get("factor_scores") or {}
        if isinstance(factor_scores, dict):
            score_items = factor_scores.items()
        elif isinstance(factor_scores, list):
            score_items = [
                (item.get("factor_id", ""), item)
                for item in factor_scores if isinstance(item, dict)
            ]
        else:
            score_items = []
        score_text = ", ".join(
            f'{factor_id}: {value.get("score", "") if isinstance(value, dict) else value}'
            for factor_id, value in score_items
        )
        reasoning = entity.get("reasoning") or ""
        sources = entity.get("source_ids") or []
        rows.append(
            "<tr>"
            f'<td><strong>{_e(entity.get("name") or entity.get("entity_id") or "대상")}</strong>'
            f'<small>{_e(entity.get("entity_type", ""))}</small></td>'
            f'<td>{_e(coords.get("x", "계산 대기"))} / {_e(coords.get("y", "계산 대기"))}</td>'
            f'<td>{_e(score_text or "평가 점수 없음")}</td>'
            f'<td>{_e(entity.get("confidence", "미지정"))} · {_e(entity.get("evidence_type", "미지정"))}</td>'
            f'<td>{_e(reasoning or (", ".join(map(str, sources)) if sources else "상세 근거는 Research Evidence 참조"))}</td>'
            "</tr>"
        )
    if not rows:
        return '<div class="missing">평가 대상 데이터를 추가 정보와 함께 확인하세요.</div>'
    return (
        '<div class="table-wrap"><table class="compact-table"><thead><tr>'
        '<th>브랜드 / 기업</th><th>X / Y 좌표</th><th>요소 점수</th><th>신뢰도 · 근거 유형</th><th>근거 요약</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def build_05_brand_positioning_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    entities = data.get("entities") if isinstance(data.get("entities"), list) else []
    chart = _coordinate_svg(entities, data.get("axis_x", {}), data.get("axis_y", {}))
    content = (
        f'<div class="positioning-top"><div class="chart-panel">{chart}'
        '<div class="chart-caption">좌표는 평가 점수와 가중치를 바탕으로 백엔드가 계산합니다.</div></div>'
        f'<div class="axis-stack">{_axis_summary("X축", data.get("axis_x", {}))}'
        f'{_axis_summary("Y축", data.get("axis_y", {}))}</div></div>'
        f'<section class="entity-evaluations"><h2>동일 기준으로 평가한 브랜드와 경쟁사</h2>{_positioning_entity_table(entities)}</section>'
        f'<div class="positioning-bottom"><div>{_render_value("POP · 시장 기본 조건", data.get("pop"))}'
        f'{_render_value("POD · 차별화 요소", data.get("pod"))}</div>'
        f'<div>{_render_value("Brand Mantra", data.get("brand_mantra"))}'
        f'{_render_value("전략적 시사점", data.get("strategic_implication"))}</div></div>'
    )
    return _standard_page("05", page, content)


def build_06_business_overview_page(page: dict[str, Any]) -> str:
    return _build_generic("06", page)


def _render_persona_cards(page_id: str, page: dict[str, Any]) -> str:
    data = page.get("data", {})
    personas = data.get("personas") if isinstance(data.get("personas"), list) else []
    cards = []
    for persona in personas:
        if not isinstance(persona, dict):
            continue
        name = persona.get("name") or persona.get("name (mark fictional)") or persona.get("persona_id") or "페르소나"
        identity = " · ".join(str(persona.get(key)) for key in ("persona_id", "archetype_label", "segment", "age_range") if persona.get(key))
        details = []
        for key, value in persona.items():
            if key in {"persona_id", "name", "name (mark fictional)", "confidence"}:
                continue
            if isinstance(value, dict):
                display = " · ".join(f"{_label(child_key)}: {child_value}" for child_key, child_value in value.items())
            elif isinstance(value, list):
                display = " · ".join(str(item) for item in value) if value else "정보 확인 필요"
            elif isinstance(value, bool):
                display = "예" if value else "아니요"
            else:
                display = str(value) if value is not None and str(value).strip() else "정보 확인 필요"
            details.append(f'<div class="persona-detail"><strong>{_e(_label(key))}</strong><span>{_e(display)}</span></div>')
        cards.append(
            f'<article class="persona-card"><div class="persona-label">{_e(identity or "AI 페르소나 모델")}</div>'
            f'<h2>{_e(name)}</h2><div class="persona-details">{"".join(details)}</div></article>'
        )
    if not cards:
        cards.append(_render_structured_data(data))
    return _standard_page(page_id, page, f'<div class="persona-grid">{"".join(cards)}</div>')


def build_07_personas_01_02_page(page: dict[str, Any]) -> str:
    return _render_persona_cards("07", page)


def build_08_personas_03_04_page(page: dict[str, Any]) -> str:
    return _render_persona_cards("08", page)


def build_09_persona_comparison_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    comparison = data.get("comparison") if isinstance(data.get("comparison"), list) else []
    columns = list(dict.fromkeys(
        key for row in comparison if isinstance(row, dict) for key in row
        if key not in {"persona_id", "persona_name"}
    ))
    header = "".join(f"<th>{_e(_label(key))}</th>" for key in ["persona_id", *columns])
    rows = []
    for row in comparison:
        if not isinstance(row, dict):
            continue
        cells = [row.get("persona_name") or row.get("persona_id") or "페르소나"]
        cells.extend(
            ", ".join(map(str, row.get(key, []))) if isinstance(row.get(key), list)
            else row.get(key, "추가 정보 필요")
            for key in columns
        )
        rows.append("<tr>" + "".join(f"<td>{_e(cell)}</td>" for cell in cells) + "</tr>")
    table = (
        f'<div class="table-wrap comparison-table"><table><thead><tr>{header}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        if rows else '<div class="missing">페르소나별 비교 자료가 필요합니다.</div>'
    )
    content = (
        f'{table}<div class="two-column">{_render_value("공통 문제", data.get("shared_problems"))}'
        f'{_render_value("고객별 차이", data.get("differences"))}</div>'
        f'{_render_value("우선 세그먼트", data.get("priority_segment"))}'
    )
    return _standard_page("09", page, content)


def build_10_value_proposition_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    vpcs = data.get("persona_vpcs") or data.get("persona_value_fits") or []
    if not isinstance(vpcs, list):
        vpcs = []
    chart_entities = []
    for vpc in vpcs:
        if not isinstance(vpc, dict):
            continue
        chart_entities.append({
            "entity_id": vpc.get("persona_id"),
            "name": vpc.get("persona_id"),
            "computed_coordinates": vpc.get("computed_coordinates") or {},
        })
    chart = _coordinate_svg(chart_entities, {"name": "문제 강도 · 긴급도"}, {"name": "가치 적합도"})
    cards = []
    for vpc in vpcs:
        if isinstance(vpc, dict):
            display_vpc = {key: value for key, value in vpc.items() if key != "computed_coordinates"}
            cards.append(f'<article class="item-card">{_render_structured_data(display_vpc)}</article>')
    content = (
        f'<div class="chart-panel">{chart}<div class="chart-caption">X/Y 좌표와 사분면은 검증된 점수·가중치로 백엔드에서 계산합니다.</div></div>'
        f'<div class="item-grid vpc-grid">{"".join(cards) if cards else _render_structured_data(data)}</div>'
        f'{_render_value("우선 공략 페르소나", data.get("priority_personas"))}'
        f'{_render_value("전략 인사이트", data.get("strategic_insight"))}'
    )
    return _standard_page("10", page, content)


def build_11_market_analysis_page(page: dict[str, Any]) -> str:
    return _build_generic("11", page)


def build_12_market_size_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    cards = []
    for market_id, label in (("tam", "TAM"), ("sam", "SAM"), ("som", "SOM")):
        item = data.get(market_id, {})
        if not isinstance(item, dict):
            item = {}
        amount = item.get("amount", item.get("value"))
        amount_text = "자료 부족" if amount is None else amount
        cards.append(
            f'<article class="market-card"><div class="field-label">{label}</div>'
            f'<div class="market-value">{_e(amount_text)}</div>'
            f'{_render_value("고객 수", item.get("customer_count"))}'
            f'{_render_value("연간 고객당 매출", item.get("annual_revenue_per_customer"))}'
            f'{_render_value("산출 근거", item.get("formula") or item.get("calculation_basis"))}'
            '</article>'
        )
    content = (
        f'<div class="market-grid">{"".join(cards)}</div>'
        f'{_render_value("산출 방법", data.get("calculation_method"))}'
        f'<div class="two-column">{_render_value("가정", data.get("assumptions"))}{_render_value("제외 범위", data.get("exclusions"))}</div>'
        f'{_render_value("출처 ID", data.get("source_ids"))}'
    )
    return _standard_page("12", page, content)


def build_13_competitor_analysis_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    competitors = data.get("competitors") if isinstance(data.get("competitors"), list) else []
    content = (
        f'{_render_value("경쟁사 비교", competitors)}'
        f'{_render_value("비교 요약", data.get("comparison_summary"))}'
        f'<div class="two-column">{_render_value("시장 공백", data.get("market_gaps"))}'
        f'{_render_value("차별화 제안", data.get("recommended_differentiation"))}</div>'
    )
    return _standard_page("13", page, content)


def build_14_swot_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    names = (
        ("strengths", "강점 · 내부"),
        ("weaknesses", "약점 · 내부"),
        ("opportunities", "기회 · 외부"),
        ("threats", "위협 · 외부"),
    )
    cells = "".join(
        f'<section class="swot-cell swot-{key}"><h2>{_e(label)}</h2>{_render_value(label, data.get(key))}</section>'
        for key, label in names
    )
    return _standard_page("14", page, f'<div class="swot-grid">{cells}</div>')


def build_15_tows_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    strategies = ("SO", "WO", "ST", "WT")
    cells = "".join(
        f'<section class="tows-cell"><h2>{key} 전략</h2>{_render_value("실행 전략", data.get(key))}</section>'
        for key in strategies
    )
    return _standard_page("15", page, f'<div class="tows-grid">{cells}</div>')


BMC_LABELS = {
    "key_partners": "핵심 파트너",
    "key_activities": "핵심 활동",
    "key_resources": "핵심 자원",
    "value_propositions": "가치 제안",
    "customer_relationships": "고객 관계",
    "channels": "채널",
    "customer_segments": "고객 세그먼트",
    "cost_structure": "비용 구조",
    "revenue_streams": "수익원",
}


def _canvas_page(page_id: str, page: dict[str, Any], labels: dict[str, str]) -> str:
    data = page.get("data", {})
    blocks = "".join(
        f'<article class="canvas-block block-{_e(key)}"><h2>{_e(label)}</h2>{_render_value(label, data.get(key))}</article>'
        for key, label in labels.items()
    )
    extra = _render_value("검증 계획", data.get("validation_plan")) if "validation_plan" in data else ""
    canvas_type = "bmc" if page_id == "16" else "lean"
    return _standard_page(page_id, page, f'<div class="canvas-grid {canvas_type}">{blocks}</div>{extra}')


def build_16_business_model_canvas_page(page: dict[str, Any]) -> str:
    return _canvas_page("16", page, BMC_LABELS)


def build_17_lean_canvas_page(page: dict[str, Any]) -> str:
    labels = {
        "problem": "문제",
        "solution": "해결책",
        "unique_value_proposition": "고유 가치 제안",
        "unfair_advantage": "모방하기 어려운 우위",
        "customer_segments": "고객 세그먼트",
        "key_metrics": "핵심 지표",
        "channels": "채널",
        "cost_structure": "비용 구조",
        "revenue_streams": "수익원",
    }
    return _canvas_page("17", page, labels)


def build_18_customer_journey_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    stages = data.get("stages") if isinstance(data.get("stages"), list) else []
    stage_cards = []
    for index, stage in enumerate(stages, start=1):
        stage_cards.append(
            f'<article class="journey-stage"><div class="stage-number">{index:02d}</div>'
            f'{_render_structured_data(stage) if isinstance(stage, dict) else _render_value("고객 여정", stage)}</article>'
        )
    content = f'<div class="journey-line">{"".join(stage_cards) if stage_cards else _render_structured_data(data)}</div>'
    return _standard_page("18", page, content)


def build_19_visual_identity_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    palette = data.get("color_palette") if isinstance(data.get("color_palette"), list) else []
    swatches = []
    for item in palette:
        if not isinstance(item, dict):
            continue
        color = str(item.get("hex") or item.get("hex_code") or item.get("color") or "")
        style = f' style="background-color:{color}"' if re.fullmatch(r"#[0-9A-Fa-f]{3,8}", color) else ""
        swatches.append(
            f'<article class="swatch-card"><div class="swatch"{style}></div>'
            f'{_render_structured_data(item)}</article>'
        )
    content = (
        f'<section class="visual-palette"><h2>컬러 팔레트</h2><div class="swatch-grid">{"".join(swatches) if swatches else _render_value("컬러 팔레트", palette)}</div></section>'
        f'{_render_value("타이포그래피", data.get("typography"))}'
        f'<div class="two-column">{_render_value("사진·이미지 가이드", data.get("photography_do"))}'
        f'{_render_value("피해야 할 표현", data.get("photography_dont"))}</div>'
        f'{_render_value("무드 키워드", data.get("mood_keywords"))}'
        f'{_render_value("디자인 원칙", data.get("design_principles") or data.get("layout_direction"))}'
    )
    return _standard_page("19", page, content)


def build_20_logo_identity_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    content = (
        f'<div class="logo-concept">{_render_value("로고 콘셉트", data.get("logo_concept"))}</div>'
        f'<div class="two-column">{_render_value("심볼", data.get("symbol"))}{_render_value("워드마크", data.get("wordmark"))}</div>'
        f'{_render_value("사용 규칙", data.get("usage_rules"))}'
        f'<div class="two-column">{_render_value("최소 크기", data.get("minimum_size"))}{_render_value("보호 여백", data.get("clear_space"))}</div>'
    )
    return _standard_page("20", page, content)


def build_21_character_identity_page(page: dict[str, Any]) -> str:
    return _build_generic("21", page)


def build_22_brand_applications_page(page: dict[str, Any]) -> str:
    return _build_generic("22", page)


def build_23_validation_roadmap_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    plan = data.get("plan") or data.get("roadmap") or data.get("phases")
    content = (
        f'{_render_value("30/60/90일 실행 계획", plan)}'
        f'<div class="two-column">{_render_value("검증 가설", data.get("validation_hypotheses"))}'
        f'{_render_value("실험", data.get("experiments"))}</div>'
        f'<div class="two-column">{_render_value("KPI", data.get("kpis"))}'
        f'{_render_value("담당자와 일정", {"owners": data.get("owners"), "timeline": data.get("timeline"), "priority": data.get("priority")})}</div>'
    )
    return _standard_page("23", page, content)


def build_24_research_evidence_page(page: dict[str, Any]) -> str:
    data = page.get("data", {})
    sources = data.get("sources") if isinstance(data.get("sources"), list) else []
    if sources:
        headers = ("source_id", "title", "publisher", "published_at", "accessed_at", "url")
        head = "".join(f'<th>{_e(_label(column))}</th>' for column in headers)
        rows = []
        for source in sources:
            source = source if isinstance(source, dict) else {"title": source}
            rows.append("<tr>" + "".join(f'<td>{_e(source.get(column, ""))}</td>' for column in headers) + "</tr>")
        source_html = f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    else:
        source_html = _render_value("출처 목록", sources)
    content = (
        f'{source_html}<div class="two-column">{_render_value("계산 가정", data.get("calculation_assumptions"))}'
        f'{_render_value("자료의 한계", data.get("limitations"))}</div>'
        f'{_render_value("검증 상태", data.get("validation_status"))}'
        f'{_render_value("AI 추정과 외부 근거 구분", data.get("ai_estimate_vs_external_evidence"))}'
    )
    return _standard_page("24", page, content)


PAGE_RENDERERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "00": build_00_cover_page,
    "01": build_01_executive_summary_page,
    "02": build_02_brand_foundation_page,
    "03": build_03_brand_identity_page,
    "04": build_04_brand_story_page,
    "05": build_05_brand_positioning_page,
    "06": build_06_business_overview_page,
    "07": build_07_personas_01_02_page,
    "08": build_08_personas_03_04_page,
    "09": build_09_persona_comparison_page,
    "10": build_10_value_proposition_page,
    "11": build_11_market_analysis_page,
    "12": build_12_market_size_page,
    "13": build_13_competitor_analysis_page,
    "14": build_14_swot_page,
    "15": build_15_tows_page,
    "16": build_16_business_model_canvas_page,
    "17": build_17_lean_canvas_page,
    "18": build_18_customer_journey_page,
    "19": build_19_visual_identity_page,
    "20": build_20_logo_identity_page,
    "21": build_21_character_identity_page,
    "22": build_22_brand_applications_page,
    "23": build_23_validation_roadmap_page,
    "24": build_24_research_evidence_page,
}


def _layout_for(page_id: str, layouts: list[dict[str, Any]]) -> tuple[str, str, int]:
    for layout in layouts:
        if str(layout.get("page_id")) == page_id:
            size = str(layout.get("paper_size", "A4")).upper()
            orientation = str(layout.get("orientation", "portrait")).lower()
            margin = layout.get("margins_mm", 12)
            if size not in {"A4", "A3"}:
                size = "A4"
            if orientation not in {"portrait", "landscape"}:
                orientation = "portrait"
            try:
                margin = max(5, min(30, int(margin)))
            except (TypeError, ValueError):
                margin = 12
            return size, orientation, margin
    return DEFAULT_PAGE_LAYOUTS[page_id]


def build_report_v2_html(
    pages: dict[str, dict[str, Any]], page_layouts: list[dict[str, Any]] | None = None
) -> str:
    layouts = page_layouts or []
    page_css: list[str] = []
    sections: list[str] = []
    for page_id in sorted(pages, key=lambda value: PAGE_ORDER.index(value)):
        if page_id not in PAGE_RENDERERS:
            raise ValueError(f"Unsupported report page ID: {page_id}")
        page = pages[page_id]
        if page.get("page_id", page_id) != page_id:
            raise ValueError(f"page_id does not match pages key: {page_id}")
        size, orientation, margin = _layout_for(page_id, layouts)
        if page_id == "00":
            margin = 0
        page_css.append(f"@page {_page_name(page_id)} {{ size: {size} {orientation}; margin: {margin}mm; }}")
        sections.append(PAGE_RENDERERS[page_id](page))

    brand_color = "#B78367"
    visual_page = pages.get("19", {}).get("data", {})
    palette = visual_page.get("color_palette", []) if isinstance(visual_page, dict) else []
    for color_item in palette if isinstance(palette, list) else []:
        if isinstance(color_item, dict):
            candidate = color_item.get("hex") or color_item.get("hex_code") or color_item.get("color")
            if isinstance(candidate, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", candidate):
                brand_color = candidate
                break
    if brand_color == "#B78367":
        cover_data = pages.get("00", {}).get("data", {})
        candidate = cover_data.get("seed_color") if isinstance(cover_data, dict) else None
        if isinstance(candidate, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", candidate):
            brand_color = candidate

    html_document = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
@page { size: A4 portrait; margin: 12mm; }
""" + "\n".join(page_css) + """
* { box-sizing: border-box; }
body { margin: 0; font-family: "Noto Sans CJK KR", "Malgun Gothic", sans-serif; color: #18212f; font-size: 10pt; }
.report-page { position: relative; min-height: 100%; break-after: page; page-break-after: always; }
.report-page:last-child { break-after: auto; page-break-after: auto; }
.page-header { display: flex; justify-content: space-between; gap: 18px; align-items: flex-end; border-bottom: 2px solid #1f3c5a; padding-bottom: 9px; margin-bottom: 16px; }
.eyebrow { color: #74849a; font-size: 8pt; letter-spacing: 1.2px; text-transform: uppercase; }
h1 { color: #183653; font-size: 22pt; line-height: 1.15; margin: 5px 0 2px; }
.subtitle { color: #617287; font-size: 11pt; }
.page-meta { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 4px 11px; max-width: 50%; color: #738196; font-size: 7.5pt; }
.page-meta span { white-space: nowrap; }
.page-meta .validation-note { white-space: normal; }
.page-content { display: block; }
.page-footer { display: flex; justify-content: space-between; border-top: 1px solid #dce3ea; margin-top: 16px; padding-top: 7px; color: #8491a1; font-size: 7pt; letter-spacing: .4px; }
.data-grid, .two-column, .item-grid, .persona-grid, .market-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.data-group { border: 1px solid #e0e6ed; border-radius: 10px; padding: 12px; margin: 0 0 12px; break-inside: avoid; }
.data-group h3, .field-label { color: #607287; font-size: 8pt; font-weight: 700; letter-spacing: .45px; margin: 0 0 5px; text-transform: uppercase; }
.data-group > h3 { border-bottom: 1px solid #e7edf2; padding-bottom: 7px; margin-bottom: 9px; }
.field { background: #f7f9fb; border-radius: 7px; padding: 9px 10px; margin: 0 0 7px; break-inside: avoid; }
.field-value { line-height: 1.45; white-space: pre-wrap; overflow-wrap: anywhere; }
.field .data-group { margin: 5px 0 0; background: white; }
.missing, .empty-state { color: #9a6a1d; background: #fff8e8; border: 1px dashed #e8cc94; border-radius: 7px; padding: 8px 10px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 5px; list-style: none; padding: 0; margin: 4px 0 0; }
.tag-list li { background: #eaf0f5; border-radius: 14px; padding: 4px 8px; font-size: 8.5pt; }
.item-card, .persona-card, .market-card, .canvas-block, .journey-stage { border: 1px solid #dce4ec; border-radius: 9px; padding: 10px; background: #fff; break-inside: avoid; }
.item-card h4, .persona-card h2, .canvas-block h2, .swot-cell h2, .tows-cell h2 { color: #214769; margin: 0 0 8px; font-size: 11pt; }
.persona-label { color: #74849a; font-size: 8pt; letter-spacing: .5px; }
.persona-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.persona-card { padding: 10px; min-width: 0; }
.persona-details { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 8px; }
.persona-detail { display: grid; grid-template-columns: minmax(58px, 34%) minmax(0, 1fr); align-items: start; gap: 4px; padding: 4px 5px; background: var(--soft); font-size: 7.2pt; line-height: 1.35; overflow-wrap: anywhere; }
.persona-detail strong { color: var(--muted); font-size: 6.4pt; font-weight: 700; }
.persona-detail span { min-width: 0; }
.persona-card h2 { font-size: 17pt; margin: 4px 0 10px; }
.thesis { background: #183653; color: #fff; border-radius: 12px; padding: 18px 20px; font-size: 17pt; line-height: 1.4; margin-bottom: 14px; }
.metric-grid { margin-bottom: 12px; }
.metric-grid .item-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.chart-panel { border: 1px solid #dce4ec; border-radius: 10px; padding: 12px; margin-bottom: 12px; break-inside: avoid; }
.quadrant-chart { display: block; width: 100%; max-height: 330px; }
.page-05 .quadrant-chart { height: 100mm; max-height: 100mm; }
.page-05 .chart-panel { padding: 8px 10px; margin-bottom: 8px; }
.page-05 .quadrant-chart { height: 65mm; max-height: 65mm; }
.positioning-top { display: grid; grid-template-columns: 1.05fr .95fr; gap: 8px; align-items: start; }
.page-05 .axis-card { border: 1px solid #dce4ec; border-radius: 8px; padding: 6px 8px; margin-bottom: 6px; }
.page-05 .axis-card h3 { margin: 0 0 3px; color: #214769; font-size: 9pt; }
.page-05 .axis-description, .page-05 .axis-anchors { font-size: 7pt; color: #53677b; margin-bottom: 3px; }
.page-05 .axis-anchors { display: flex; justify-content: space-between; }
.page-05 .entity-evaluations { margin-top: 4px; }
.page-05 .entity-evaluations h2 { color: #214769; font-size: 9pt; margin: 4px 0; }
.page-05 .compact-table { font-size: 6.8pt; }
.page-05 .compact-table th, .page-05 .compact-table td { padding: 3px 4px; }
.page-05 .compact-table small { display: block; color: #7d8b99; }
.positioning-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px; }
.positioning-bottom .field { padding: 5px 7px; margin-bottom: 4px; }
.quadrant-bg { fill: #f5f8fa; stroke: #aebdcb; stroke-width: 1; }
.axis-line { stroke: #9babb9; stroke-dasharray: 4 4; stroke-width: 1; }
.plot-point { fill: #d98336; stroke: #fff; stroke-width: 2; }
.plot-label, .axis-label { fill: #34495e; font-size: 10px; }
.axis-title { fill: #41566a; font-size: 11px; font-weight: 700; }
.chart-caption { color: #758398; font-size: 8pt; margin-top: 5px; }
.table-wrap { width: 100%; overflow-wrap: anywhere; }
table { width: 100%; border-collapse: collapse; font-size: 8.5pt; }
th { background: #eaf0f5; color: #23425e; text-align: left; }
th, td { border: 1px solid #d5dee7; padding: 6px 7px; vertical-align: top; }
tr { break-inside: avoid; }
.market-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); margin-bottom: 12px; }
.market-value { font-size: 21pt; font-weight: 800; color: #214769; margin: 5px 0 10px; }
.page-12 .market-grid { gap: 6px; margin-bottom: 7px; }
.page-12 .market-card { padding: 7px; }
.page-12 .market-value { font-size: 16pt; margin: 2px 0 5px; }
.page-12 .field { padding: 5px 6px; margin-bottom: 3px; }
.swot-grid, .tows-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.swot-cell, .tows-cell { border: 1px solid #dce4ec; border-radius: 10px; padding: 12px; background: #fbfcfd; break-inside: avoid; }
.swot-strengths { border-top: 4px solid #5c9b74; }.swot-weaknesses { border-top: 4px solid #d39a4a; }
.swot-opportunities { border-top: 4px solid #5686b3; }.swot-threats { border-top: 4px solid #b56b6b; }
.canvas-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); grid-template-rows: repeat(3, minmax(48mm, auto)); gap: 6px; }
.canvas-grid.bmc .block-key_partners { grid-column: 1; grid-row: 1 / 3; }
.canvas-grid.bmc .block-key_activities { grid-column: 2; grid-row: 1; }
.canvas-grid.bmc .block-key_resources { grid-column: 2; grid-row: 2; }
.canvas-grid.bmc .block-value_propositions { grid-column: 3; grid-row: 1 / 3; }
.canvas-grid.bmc .block-customer_relationships { grid-column: 4; grid-row: 1; }
.canvas-grid.bmc .block-channels { grid-column: 4; grid-row: 2; }
.canvas-grid.bmc .block-customer_segments { grid-column: 5; grid-row: 1 / 3; }
.canvas-grid.bmc .block-cost_structure { grid-column: 1 / 3; grid-row: 3; }
.canvas-grid.bmc .block-revenue_streams { grid-column: 3 / 6; grid-row: 3; }
.canvas-grid.lean .block-problem { grid-column: 1; grid-row: 1; }
.canvas-grid.lean .block-solution { grid-column: 2; grid-row: 1; }
.canvas-grid.lean .block-unique_value_proposition { grid-column: 3; grid-row: 1 / 3; }
.canvas-grid.lean .block-unfair_advantage { grid-column: 4; grid-row: 1; }
.canvas-grid.lean .block-customer_segments { grid-column: 5; grid-row: 1; }
.canvas-grid.lean .block-key_metrics { grid-column: 1; grid-row: 2; }
.canvas-grid.lean .block-channels { grid-column: 2; grid-row: 2; }
.canvas-grid.lean .block-cost_structure { grid-column: 1 / 3; grid-row: 3; }
.canvas-grid.lean .block-revenue_streams { grid-column: 3 / 6; grid-row: 3; }
.canvas-block { padding: 8px; background: #f9fbfc; }.canvas-block h2 { font-size: 9pt; border-bottom: 1px solid #e0e6ed; padding-bottom: 5px; }
.canvas-block .field { background: transparent; padding: 3px; }
.canvas-block .field-label { font-size: 7pt; }
.journey-line { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
.stage-number { width: 26px; height: 26px; border-radius: 50%; background: #1f3c5a; color: #fff; text-align: center; line-height: 26px; margin-bottom: 6px; }
.visual-palette { margin-bottom: 12px; }.visual-palette h2 { color: #214769; font-size: 12pt; }
.swatch-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; }
.swatch-card { border: 1px solid #dce4ec; border-radius: 8px; padding: 7px; break-inside: avoid; }
.swatch { height: 24mm; border-radius: 5px; background: #edf1f4; border: 1px solid #dce4ec; margin-bottom: 7px; }
.vpc-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.page-10 .vpc-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; }
.page-10 .vpc-grid > .item-card { padding: 6px; }
.page-10 .vpc-grid .field { padding: 4px 5px; margin-bottom: 3px; font-size: 7.5pt; }
.page-10 .vpc-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; }
.page-10 .vpc-grid > .item-card { padding: 6px; }
.page-10 .vpc-grid .field { padding: 4px 5px; margin-bottom: 3px; font-size: 7.5pt; }
.comparison-table table { font-size: 7.2pt; }
.comparison-table th, .comparison-table td { padding: 4px 5px; }
.cover-page { min-height: 100%; background: linear-gradient(155deg, #f7f4ed 0%, #fff 58%, #e8eef2 100%); padding: 18mm 15mm; display: flex; flex-direction: column; justify-content: space-between; color: #193650; }
.cover-top, .cover-bottom { display: flex; justify-content: space-between; color: #738196; font-size: 8pt; letter-spacing: 1px; }
.cover-main { margin-top: 26mm; }
.cover-kicker { color: #b36e30; font-weight: 700; letter-spacing: 2px; font-size: 9pt; }
.cover-page h1 { font-size: 42pt; line-height: 1.05; margin: 12px 0; overflow-wrap: anywhere; }
.cover-copy { font-size: 18pt; line-height: 1.5; max-width: 145mm; color: #425a70; }
.cover-promise { border-left: 3px solid #c8874b; padding: 8px 14px; margin-top: 18px; color: #324e67; font-size: 12pt; }
.cover-facts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 30mm; }
.cover-facts div { border-top: 1px solid #bdc9d2; padding-top: 8px; }.cover-facts small { display: block; color: #738196; margin-bottom: 4px; }
.cover-facts strong { font-size: 11pt; }
@page report_10 { size: A3 landscape; margin: 15mm; }
@page report_16 { size: A3 landscape; margin: 15mm; }
@page report_17 { size: A3 landscape; margin: 15mm; }
/* NAME TAG: warm paper, gentle Korean sans typography, and soft rounded surfaces. */
:root { --seed: __BRAND_COLOR__; --ink: #383630; --muted: #817970; --paper: #fffdf9; --line: #e9e1d7; --soft: #f6f1e9; --soft-accent: #f3e8df; }
body { font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; color: var(--ink); background: var(--paper); line-height: 1.78; font-size: 10.5pt; }
.report-page { background: var(--paper); }
.page-header { border-bottom: 1px solid var(--line); padding-bottom: 14px; margin-bottom: 22px; align-items: flex-end; }
.eyebrow, .section-kicker { color: var(--seed); font-size: 7.5pt; letter-spacing: .8px; font-weight: 600; }
h1, .item-card h4, .persona-card h2 { font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; color: #403b35; font-weight: 500; }
h1 { font-size: 27pt; letter-spacing: 0; line-height: 1.28; }
h2 { font-size: 16pt; line-height: 1.4; font-weight: 600; }
h3 { font-size: 13pt; line-height: 1.45; font-weight: 600; }
h4 { font-size: 11.5pt; line-height: 1.45; font-weight: 600; }
.subtitle { color: var(--muted); font-size: 11pt; letter-spacing: 0; }
.page-meta { max-width: 47%; color: var(--muted); font-size: 7pt; gap: 5px 10px; }
.page-footer { border-color: var(--line); color: #9b9389; margin-top: 22px; font-size: 7pt; }
.data-group { border: 0; border-top: 1px solid var(--line); border-radius: 0; padding: 14px 0 4px; margin-bottom: 16px; }
.data-group > h3 { color: #625a51; font-size: 13pt; letter-spacing: 0; font-weight: 600; }
.field-label { color: var(--muted); font-size: 8.2pt; letter-spacing: .2px; font-weight: 600; }
.field { background: var(--soft); border-radius: 12px; padding: 14px 16px; margin-bottom: 9px; }
.field-value { color: #45413b; font-size: 10.5pt; line-height: 1.78; }
.field-value strong.emphasis, .tag-list strong.emphasis { color: #3c342e; font-weight: 700; }
.item-card, .persona-card, .market-card, .canvas-block, .journey-stage { border: 1px solid var(--line); border-radius: 14px; padding: 14px; background: #fffdfa; box-shadow: 0 2px 8px rgba(75, 58, 42, .035); }
.item-card h4, .canvas-block h2, .swot-cell h2, .tows-cell h2 { color: #655d53; font-weight: 600; }
.thesis { background: var(--soft-accent); color: #494139; border-radius: 18px; font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; font-size: 17pt; font-weight: 500; line-height: 1.65; padding: 24px 26px; }
.tag-list li { background: #f0e8df; border-radius: 999px; color: #61584f; padding: 5px 11px; }
.missing, .empty-state { color: #78644f; background: #faf4eb; border: 1px solid #eadcc9; border-radius: 12px; padding: 11px 13px; }
table { font-size: 8pt; }
th { background: #f4efe8; color: #61594f; }
th, td { border-color: var(--line); }
.chart-panel, .axis-card { border-color: var(--line); border-radius: 14px; background: #fffdfa; }
.quadrant-bg { fill: #faf9f5; stroke: #cfc9bd; }
.axis-line { stroke: #b9b2a6; }
.plot-point { fill: var(--seed); }
.axis-title, .plot-label { fill: #514d45; }
.swot-cell, .tows-cell { background: #fffdfa; border-color: var(--line); border-radius: 14px; padding: 15px; }
.cover-page { display: block; position: relative; background: linear-gradient(145deg, #fbf7f0 0%, #f8f2e9 72%, #f2e8dc 100%); color: var(--ink); width: 210mm; height: 297mm; min-height: 297mm; margin: 0; padding: 26mm 28mm; }
.cover-top, .cover-bottom { color: #8d8378; }
.cover-kicker { color: var(--seed); font-weight: 600; letter-spacing: 1.1px; }
.cover-page h1, .cover-copy, .cover-promise { color: #403b35; }
.cover-page h1 { font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; font-weight: 500; }
.cover-main { margin-top: 22mm; }
.cover-copy { color: #6c6258; }
.cover-promise { border-color: var(--seed); color: #61574d; background: rgba(255,255,255,.52); border-radius: 0 14px 14px 0; padding: 12px 16px; }
.cover-facts div { border-color: #dfd2c3; }
.cover-facts { margin-top: 22mm; }
.cover-facts small { color: #8d8378; }
.cover-bottom { position: absolute; left: 28mm; right: 28mm; bottom: 26mm; margin-top: 0; }
.golden-circle { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0; }
.golden-card { border-top: 0; border-radius: 14px; background: var(--soft); padding: 14px 15px 12px; }
.golden-card > span, .essence-panel > span { color: #756455; font-size: 8pt; font-weight: 600; letter-spacing: .5px; }
.golden-card .field-label, .essence-panel .field-label, .prism-card .field-label, .story-step .field-label { display: none; }
.essence-panel { padding: 19px 20px; margin: 15px 0; background: var(--soft-accent); border-left: 4px solid var(--seed); border-radius: 0 14px 14px 0; }
.prism-panel { margin: 14px 0 18px; padding: 17px; background: #f8f4ed; border-radius: 16px; }
.prism-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 12px; }
.prism-card { background: #fffdfa; padding: 13px; border: 1px solid var(--line); border-radius: 12px; break-inside: avoid; }
.prism-card > span { color: #756455; font-size: 7.5pt; font-weight: 600; }
.identity-lower { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.story-flow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 18px 0; }
.story-step { padding: 14px; border-top: 0; border-radius: 14px; background: var(--soft); break-inside: avoid; }
.story-step > span { color: var(--seed); font: 600 15pt "Noto Sans KR", "Malgun Gothic", sans-serif; }
.story-step h2 { font: 500 11pt "Noto Sans KR", "Malgun Gothic", sans-serif; margin: 5px 0 10px; }
.slogan-panel { margin: 15px 0; padding: 18px; text-align: center; background: var(--soft); border: 0; border-radius: 14px; }
</style></head><body>""" + "".join(sections) + "</body></html>"
    return html_document.replace("__BRAND_COLOR__", brand_color)


def _compact_pdf_value(value: Any) -> str:
    """Render one compact, escaped value for full-report pagination."""
    if value is None or value == "":
        return "추가 정보 필요"
    if isinstance(value, dict):
        return " · ".join(
            f'<span class="compact-label">{_e(_label(key))}:</span> {_compact_pdf_value(child)}'
            for key, child in value.items()
        )
    if isinstance(value, list):
        return " · ".join(_compact_pdf_value(child) for child in value) if value else "추가 정보 필요"
    if isinstance(value, bool):
        return "예" if value else "아니요"
    if isinstance(value, str):
        enum_labels = {
            "complete": "완료", "validated": "검증 완료", "insufficient_data": "자료 부족",
            "to_validate": "검증 필요", "assumption": "가정", "low": "낮음", "medium": "보통", "high": "높음",
            "ai_estimate": "AI 추정", "user_input": "사용자 입력", "external_research": "외부 조사",
        }
        if value in enum_labels:
            return enum_labels[value]
    return _render_inline_markdown(value)


def _compact_pdf_page_data(data: dict[str, Any]) -> str:
    sections: list[str] = []
    for key, value in data.items():
        label = _e(_label(key))
        if isinstance(value, dict):
            body = "".join(
                f'<div class="compact-row"><span class="compact-label">{_e(_label(child_key))}</span> {_compact_pdf_value(child)}</div>'
                for child_key, child in value.items()
            )
        elif isinstance(value, list) and any(isinstance(item, dict) for item in value):
            records = []
            for index, item in enumerate(value, 1):
                if isinstance(item, dict):
                    identity_key = next((name for name in ("persona_id", "strategy_id", "competitor_id", "id", "name", "period", "stage", "metric", "factor_id") if item.get(name)), None)
                    identity = item.get(identity_key) if identity_key else f"항목 {index}"
                    records.append(f'<div class="compact-record"><strong>{_e(identity)}</strong> · {_compact_pdf_value(item)}</div>')
                else:
                    records.append(f'<div class="compact-record">{_compact_pdf_value(item)}</div>')
            body = "".join(records)
        else:
            body = _compact_pdf_value(value)
        sections.append(f'<section class="compact-section"><h2>{label}</h2><div>{body}</div></section>')
    return "".join(sections) or '<div class="empty-state">추가 정보 필요</div>'


def _compact_pdf_cards(data: dict[str, Any]) -> str:
    """Render complete data with page-specific cards and grids."""
    def field(key: str, val: Any, extra: str = "") -> str:
        if isinstance(val, list) and val and all(isinstance(item, dict) for item in val):
            body = "".join(f'<article class="record-card">{_compact_pdf_value(item)}</article>' for item in val)
        else:
            body = f'<div class="field-value">{_compact_pdf_value(val)}</div>'
        return f'<section class="field-card {extra}"><h2>{_e(_label(key))}</h2>{body}</section>'

    if isinstance(data.get("personas"), list):
        cards = []
        hidden = {"persona_id", "name", "name (mark fictional)", "quote (mark fictional)", "confidence", "evidence_type"}
        for person in data["personas"]:
            if not isinstance(person, dict):
                continue
            pid = person.get("persona_id", "")
            name = person.get("name") or person.get("name (mark fictional)") or pid or "고객 페르소나"
            identity = " · ".join(str(person[k]) for k in ("persona_id", "archetype_label", "segment", "age_range") if person.get(k))
            details = "".join(
                f'<div class="persona-detail"><strong>{_e(_label(k))}</strong><span>{_compact_pdf_value(v)}</span></div>'
                for k, v in person.items() if k not in hidden
            )
            quote = person.get("quote")
            quote_html = f'<blockquote>{_render_inline_markdown(quote)}</blockquote>' if quote else ""
            cards.append(f'<article class="persona-card"><div class="card-kicker">고객 페르소나 · {_render_inline_markdown(identity)}</div><h2>{_render_inline_markdown(name)}</h2><div class="persona-details">{details}</div>{quote_html}</article>')
        return f'<div class="persona-grid">{"".join(cards)}</div>'

    if isinstance(data.get("comparison"), list):
        cards = "".join(
            f'<article class="comparison-card"><div class="card-kicker">{_e(item.get("persona_id", "고객"))}</div>{_compact_pdf_value(item.get("criteria", item))}</article>'
            for item in data["comparison"] if isinstance(item, dict)
        )
        extras = "".join(field(k, data.get(k)) for k in ("shared_problems", "differences", "priority_segment") if data.get(k))
        extras = f'<div class="comparison-support"><h2>비교 결과와 우선순위</h2><div class="support-grid">{extras}</div></div>' if extras else ""
        return f'<div class="comparison-grid">{cards}</div>{extras}'

    if all(k in data for k in ("strengths", "weaknesses", "opportunities", "threats")):
        names = {"strengths":"강점 · 내부", "weaknesses":"약점 · 내부", "opportunities":"기회 · 외부", "threats":"위협 · 외부"}
        return '<div class="quadrant-grid swot-grid">' + ''.join(field(k, data.get(k), f"swot-{k}") for k in names) + '</div>'
    if all(k in data for k in ("SO", "WO", "ST", "WT")):
        return '<div class="quadrant-grid">' + ''.join(field(k, data.get(k), f"tows-{k}") for k in ("SO", "WO", "ST", "WT")) + '</div>'

    if all(k in data for k in ("customer_segments", "value_propositions", "channels", "revenue_streams", "cost_structure")):
        order = ("key_partners", "key_activities", "key_resources", "value_propositions", "customer_relationships", "channels", "customer_segments", "cost_structure", "revenue_streams")
        grid = "".join(field(k, data.get(k)) for k in order if k in data)
        extra = field("validation_plan", data["validation_plan"]) if data.get("validation_plan") else ""
        return f'<div class="canvas-grid">{grid}</div>{extra}'

    if isinstance(data.get("stages"), list):
        stages = "".join(
            f'<article class="journey-card"><div class="step-number">{i:02d}</div><h2>{_e(str(item.get("stage") or f"단계 {i}"))}</h2>{_compact_pdf_value({k:v for k,v in item.items() if k != "stage"})}</article>'
            for i, item in enumerate(data["stages"], 1) if isinstance(item, dict)
        )
        extras = "".join(field(k, v) for k, v in data.items() if k not in {"stages", "persona_ids"})
        return f'<div class="journey-grid">{stages}</div>{extras}'

    if all(k in data for k in ("tam", "sam", "som")):
        cards = "".join(field(k.upper(), data.get(k), f"market-{k}") for k in ("tam", "sam", "som"))
        extras = "".join(field(k, v) for k, v in data.items() if k not in {"tam", "sam", "som"})
        return f'<div class="market-grid">{cards}</div><div class="support-grid">{extras}</div>'

    if "persona_vpcs" in data:
        entities = [{"entity_id": item.get("persona_id"), "name": item.get("persona_id"), "computed_coordinates": item.get("computed_coordinates") or {}}
                    for item in data.get("persona_vpcs", []) if isinstance(item, dict)]
        chart = _coordinate_svg(entities, {"name": "문제 강도"}, {"name": "가치 적합도"})
        cards = "".join(field("고객 가치 적합도", item) for item in data.get("persona_vpcs", []) if isinstance(item, dict))
        return f'<div class="chart-panel">{chart}<div class="chart-caption">좌표는 제공된 입력값을 시각화합니다.</div></div><div class="vpc-grid">{cards}</div>'

    if "competitors" in data:
        cards = "".join(f'<article class="record-card"><div class="card-kicker">{_e(str(item.get("name") or item.get("competitor_id") or "비교 대상"))}</div>{_compact_pdf_value(item)}</article>' for item in data.get("competitors", []) if isinstance(item, dict))
        extras = "".join(field(k, v) for k, v in data.items() if k != "competitors")
        return f'<div class="comparison-grid">{cards}</div>{extras}'

    fields = "".join(field(k, v) for k, v in data.items() if k != "enabled")
    return f'<div class="support-grid">{fields}</div>'


def build_report_v2_compact_html(pages: dict[str, dict[str, Any]]) -> str:
    """Build a one-report-section-per-page HTML document for full 25-page exports.

    The detailed dashboard templates use dense CSS grids that can fragment into
    dozens of physical pages in WeasyPrint. This pagination-safe layout preserves
    each page's complete data, hierarchy, evidence state, and bold markdown.
    """
    sections: list[str] = []
    page_css: list[str] = []
    for page_id in PAGE_ORDER:
        if page_id not in pages:
            continue
        paper, orientation, margin = DEFAULT_PAGE_LAYOUTS[page_id]
        footer_rules = "" if page_id == "00" else (
            '@bottom-left { content: "NAME TAG · BRAND & BUSINESS STRATEGY"; '
            'font: 9pt "Noto Sans KR", sans-serif; color: #625b51; '
            'border-top: .7pt solid #e4d8ca; padding-top: 1.5mm; } '
            f'@bottom-right {{ content: "{page_id} / 25"; font: 9pt "Noto Sans KR", sans-serif; '
            'color: #625b51; border-top: .7pt solid #e4d8ca; padding-top: 1.5mm; }'
        )
        page_css.append(
            f"@page {_page_name(page_id)} {{ size: {paper} {orientation}; margin: {0 if page_id == '00' else margin}mm; {footer_rules} }}"
        )
        page = pages[page_id]
        data = page.get("data") if isinstance(page.get("data"), dict) else {}
        body_size = 10.0
        title = page.get("title") or PAGE_TITLES[page_id][0]
        subtitle = PAGE_TITLES[page_id][1]
        content = _compact_pdf_cards(data)
        insight_keys = ("brand_thesis", "strategic_implication", "brand_essence", "customer_connection", "priority_segment", "market_attractiveness", "recommended_differentiation", "unique_value_proposition")
        insight = next((data.get(key) for key in insight_keys if data.get(key)), None)
        if isinstance(insight, list):
            insight = insight[0] if insight else None
        insight_html = (
            f'<aside class="insight-bar"><strong>핵심 인사이트</strong><div>{_compact_pdf_value(insight)}</div></aside>'
            if insight and page_id != "00" else ""
        )
        if page_id == "00":
            content = (
                '<div class="cover-kicker">NAME TAG · BRAND & BUSINESS STRATEGY</div>'
                f'<h1 class="cover-title">{_render_inline_markdown(data.get("brand_name") or "NAME TAG")}</h1>'
                f'<p class="cover-headline">{_render_inline_markdown(data.get("key_sentence") or "브랜드 전략 보고서")}</p>'
                f'<div class="cover-promise">{_render_inline_markdown(data.get("brand_promise") or "")}</div>'
                f'<div class="cover-facts">{_compact_pdf_value({key: data.get(key) for key in ("industry", "report_version", "report_date") if data.get(key)})}</div>'
            )
            header = ""
            note = ""
        else:
            status = str(page.get("status", "미지정"))
            status_labels = {"complete": "완료", "insufficient_data": "자료 부족", "to_validate": "검증 필요"}
            confidence_labels = {"low": "낮음", "medium": "보통", "high": "높음"}
            confidence = str(page.get("confidence", "미지정"))
            status_class = {"complete": "ready", "insufficient_data": "insufficient"}.get(status, "caution")
            header = (
                f'<header><div class="eyebrow">NAME TAG · BRAND & BUSINESS REPORT · {page_id}</div>'
                f'<div class="page-meta"><span class="status-badge {status_class}">{_e(status_labels.get(status, status))}</span>'
                f'<span class="confidence-badge">신뢰도 · {_e(confidence_labels.get(confidence, confidence))}</span></div>'
                f'<h1>{_e(title)}</h1><div class="subtitle">{_e(subtitle)}</div></header>'
            )
            validation_notes = page.get("validation_notes") or []
            note = f'<div class="validation-note"><strong>검증 메모</strong><div>{_render_inline_markdown(" · ".join(map(str, validation_notes)))}</div></div>' if validation_notes else ""
        page_height = {"A4": (297 if orientation == "portrait" else 210), "A3": (420 if orientation == "portrait" else 297)}[paper]
        min_height = page_height - (2 * (0 if page_id == "00" else margin))
        sections.append(
            f'<section class="report-page page-{page_id}" style="page: {_page_name(page_id)}; font-size:{body_size}pt; min-height:{min_height}mm">'
            f'{header}{note}<main>{content}</main>{insight_html}</section>'
        )

    css = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@page { size: A4 portrait; margin:12mm; }
__PAGE_CSS__
* { box-sizing:border-box; }
body { margin:0; font-family:"Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif; color:#383630; background:#fffdf9; line-height:1.42; }
.report-page { break-after:page; page-break-after:always; padding-bottom:8mm; }
.report-page:last-child { break-after:auto; page-break-after:auto; }
header { position:relative; border-bottom:1pt solid #e4d8ca; padding:0 0 4mm; margin:0 0 5mm; }
.eyebrow,.cover-kicker { color:#8c513b; font-size:9pt; letter-spacing:.7px; font-weight:600; }
h1 { color:#403b35; font-size:24pt; line-height:1.14; font-weight:500; margin:2mm 0 1mm; }
.subtitle { color:#595248; font-size:12pt; }
.page-meta { position:absolute; right:0; top:0; width:58mm; display:flex; justify-content:flex-end; align-items:center; gap:2mm; text-align:right; font-size:10pt; white-space:nowrap; }
.status-badge,.confidence-badge { display:inline-block; border-radius:99px; padding:1.1mm 2mm; white-space:nowrap; }
.status-badge { color:#63331f; background:#f4dfd2; font-weight:700; }
.status-badge.ready { color:#254c36; background:#dcefe2; }
.status-badge.insufficient { color:#6e2f2b; background:#f2d8d3; }
.confidence-badge { color:#4f4b43; background:#f1ece5; }
.field-card,.record-card,.persona-card,.comparison-card,.journey-card { border:1pt solid #e4d8ca; border-radius:3mm; background:#fffdfa; padding:4mm; break-inside:avoid; }
.field-card h2 { color:#684c3b; font-size:12pt; font-weight:700; margin:0 0 2mm; }
.field-value { font-size:10pt; line-height:1.45; overflow-wrap:anywhere; }
.support-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:3mm; align-content:start; }
.record-card { padding:2.5mm 3mm; margin:1.5mm 0; font-size:10pt; line-height:1.4; }
.record-card .card-kicker,.card-kicker { color:#654a38; font-size:10pt; font-weight:700; margin-bottom:1.5mm; }
.persona-grid { display:grid; grid-template-columns:minmax(0,1fr); gap:0; align-content:start; }
.persona-card + .persona-card { break-before:page; page-break-before:always; }
.comparison-grid,.market-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:4mm; align-content:start; }
.comparison-support { break-before:page; page-break-before:always; }
.comparison-support > h2 { color:#654a38; font-size:17pt; margin:0 0 4mm; }
.persona-card { padding:4mm; }
.persona-card h2 { color:#403b35; font-size:17pt; margin:1.5mm 0 3mm; }
.persona-details { display:grid; grid-template-columns:minmax(0,1fr); gap:0; }
.persona-detail { display:grid; grid-template-columns:38mm minmax(0,1fr); gap:2mm; padding:1.2mm 0; border-top:.5pt solid #ece5dd; min-width:0; align-items:start; }
.persona-detail strong { color:#534a40; font-size:9pt; font-weight:700; }
.persona-detail span { display:block; font-size:10pt; line-height:1.35; overflow-wrap:anywhere; }
.page-07 .persona-detail span,.page-08 .persona-detail span { font-size:12pt; line-height:1.38; }
.page-07 .persona-detail strong,.page-08 .persona-detail strong { font-size:10pt; }
blockquote { margin:3mm 0 0; padding:2mm 3mm; border-left:2pt solid #a96143; background:#f8f0e9; font-size:10pt; }
.comparison-card { font-size:10pt; line-height:1.42; }
.quadrant-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:4mm; align-content:start; }
.swot-strengths { border-top:3pt solid #60896b; }.swot-weaknesses { border-top:3pt solid #be7c55; }
.swot-opportunities { border-top:3pt solid #7295a0; }.swot-threats { border-top:3pt solid #9d6e6a; }
.canvas-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:2.5mm; align-content:start; }
.canvas-grid .field-card { padding:3mm; min-height:31mm; }
.canvas-grid .field-card h2 { border-bottom:.7pt solid #dfc5b4; padding-bottom:1mm; }
.journey-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:2.5mm; align-content:start; }
.journey-card { position:relative; padding:4mm; border-top:2.5pt solid #b78367; font-size:10pt; }
.journey-card h2 { font-size:12pt; margin:1mm 0 2mm; }
.step-number { color:#8c513b; font-weight:700; font-size:10pt; }
.chart-panel { border:1pt solid #e4d8ca; border-radius:3mm; padding:3mm; margin-bottom:4mm; }
.chart-panel svg { display:block; width:100%; max-height:78mm; }
.chart-caption { color:#4f4b43; font-size:9pt; margin-top:1mm; }
.vpc-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:2.5mm; }
.compact-section { margin:0 0 1.6mm; padding:0 0 .7mm; border-bottom:.35pt solid #e9e1d7; break-inside:auto; }
.compact-section h2 { color:#655d53; font-size:1.16em; line-height:1.14; margin:0 0 .6mm; font-weight:600; }
.compact-row,.compact-record { margin:.25mm 0; }
.compact-record { border-left:1.1pt solid #d8c5b4; padding-left:1.2mm; }
.compact-label { color:#575047; font-size:9pt; font-weight:700; }
strong.emphasis { color:#3c342e; font-weight:700; }
.validation-note { color:#49372b; background:#f8eee4; border-left:3pt solid #b78367; border-radius:0 2mm 2mm 0; margin:0 0 4mm; padding:2.5mm 3mm; font-size:10pt; line-height:1.4; }
.validation-note strong { display:block; font-size:10pt; margin-bottom:1mm; }
main { min-width:0; }
.insight-bar { display:grid; grid-template-columns:30mm minmax(0,1fr); gap:3mm; align-items:start; border-left:3pt solid #a96143; border-radius:0 2mm 2mm 0; background:#f6eee5; margin-top:4mm; padding:3mm 4mm; font-size:10pt; line-height:1.4; break-inside:avoid; }
.insight-bar strong { color:#633b2b; font-size:10pt; }
.page-00 { padding:20mm 22mm; }
.cover-kicker { letter-spacing:1px; }
.cover-title { font-size:42pt; margin:13mm 0 4mm; }
.cover-headline { max-width:166mm; font-size:16pt; color:#554a3e; line-height:1.5; word-break:keep-all; }
.cover-promise { border-left:2pt solid #b78367; background:#f6f1e9; padding:4mm; margin:4mm 0; }
.cover-facts { margin-top:22mm; color:#655d53; font-size:9pt; }
</style></head><body>__SECTIONS__</body></html>"""
    return css.replace("__PAGE_CSS__", "\n".join(page_css)).replace("__SECTIONS__", "".join(sections))
