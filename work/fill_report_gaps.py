import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from backend.prompts.nametag_prompts_v2 import REPORT_PAGE_ORDER, REPORT_PAGE_SPECS, apply_backend_calculations, validate_page_result

STATE_PATH = ROOT / "work" / "nametag_25_report.json"
NEED = "추가 사용자 입력과 근거 자료가 없어 결론을 보류합니다. 검증 전 가설입니다."
HYP = "확인된 서비스 방향을 토대로 한 실행 가설이며, 실제 운영 사실로 간주하지 않습니다."


def page_data(page_id):
    if page_id == "01":
        return {
            "brand_thesis": "살뜰마을은 지역 생활용품 구독 서비스라는 입력을 바탕으로 1인 가구의 생활 편의를 제안하는 브랜드 가설입니다. 시장·운영 근거는 확인되지 않아 검증이 필요합니다.",
            "key_metrics": [{"metric": "핵심 성과 지표", "value": NEED, "definition": "유료 전환, 재구매, 배송당 공헌이익을 실제 데이터로 측정"}],
            "key_findings": ["브랜드명·서비스 유형·타겟만 확인됨", "가격·지역·운영 역량·실적 정보가 없음", "경쟁·시장 크기·고객 지불 의향 조사 필요"],
            "key_strategies": ["고객 문제와 구매 의향 인터뷰", "한 지역·한 상품군의 소규모 수요 검증", "반복 구매와 단위경제성 확인 후 확장"],
            "priority_actions": [{"action": "서비스 범위·가격·운영 지역을 확정", "priority": "1", "measure": "확정된 입력과 근거 기록"}, {"action": "고객 인터뷰와 경쟁 대안 조사", "priority": "2", "measure": "출처 ID와 조사 기록"}],
            "calculation_basis": NEED,
        }
    if page_id == "05":
        x_factors = [{"factor_id": "convenience", "name": "구매·이용 편의", "weight": 1.0, "definition": NEED, "rubric": NEED}]
        y_factors = [{"factor_id": "space_fit", "name": "1인 주거 적합성", "weight": 1.0, "definition": NEED, "rubric": NEED}]
        scores = [
            {"factor_id": "convenience", "score": 0, "reasoning": NEED, "source_ids": []},
            {"factor_id": "space_fit", "score": 0, "reasoning": NEED, "source_ids": []},
        ]
        return {
            "axis_x": {"name": "구매·이용 편의", "description": NEED, "low_anchor": NEED, "high_anchor": NEED, "evaluation_factors": x_factors},
            "axis_y": {"name": "1인 주거 적합성", "description": NEED, "low_anchor": NEED, "high_anchor": NEED, "evaluation_factors": y_factors},
            "entities": [{"entity_id": "our_idea", "entity_type": "our_idea", "name": "살뜰마을", "factor_scores": scores, "confidence": "low", "evidence_type": "ai_estimate"}],
            "pop": NEED, "pod": NEED, "brand_mantra": NEED,
            "strategic_implication": NEED,
        }
    if page_id == "10":
        factors = {key: {"score": 0, "reasoning": "근거 자료가 없어 임시 보류값입니다. 실제 고객가치 점수나 순위로 해석하지 마세요."} for key in "SF IAPGDC".replace(" ", "")}
        personas = []
        for persona_id in ("P1", "P2", "P3", "P4"):
            personas.append({"persona_id": persona_id, "customer_jobs": [NEED], "pains": [NEED], "gains": [NEED], "products_services": [HYP], "pain_relievers": [NEED], "gain_creators": [NEED]})
        return {"persona_vpcs": personas, "value_fit_inputs": {persona_id: factors for persona_id in ("P1", "P2", "P3", "P4")}}
    if page_id == "11":
        return {
            "three_c": {key: NEED for key in ("company", "customer", "competitor")},
            "five_forces": {key: NEED for key in ("rivalry", "new_entrants", "substitutes", "buyer_power", "supplier_power")},
            "key_success_factors": [NEED], "market_attractiveness": NEED,
            "strategic_implications": ["운영 지역과 고객군을 정한 뒤 시장·경쟁 자료를 수집해야 합니다."], "source_ids": [],
        }
    if page_id == "12":
        missing = {"amount": None, "customer_count": None, "revenue_per_customer_year": None, "formula": NEED}
        return {"tam": dict(missing), "sam": dict(missing), "som": dict(missing), "calculation_method": NEED, "assumptions": [NEED], "exclusions": ["검증된 지역·고객 수·가격 정보가 없어 산출에서 제외"], "source_ids": [], "confidence": "low", "insufficient_data_when_needed": True}
    if page_id == "13":
        return {"competitors": [], "comparison_summary": NEED, "market_gaps": [NEED], "recommended_differentiation": ["실제 경쟁 대안과 고객 구매 기준을 조사한 뒤 차별화 방향을 확정합니다."]}
    if page_id == "14":
        return {
            "strengths": [{"id": "S1", "factor": "1인 가구를 타겟으로 하는 서비스 방향이 명시됨", "evidence": "사용자 입력", "impact": "가설", "source_ids": [], "confidence": "low"}],
            "weaknesses": [{"id": "W1", "factor": "가격·운영·공급·성과 정보가 확인되지 않음", "evidence": "현재 입력 범위", "impact": "검증 필요", "source_ids": [], "confidence": "low"}],
            "opportunities": [{"id": "O1", "factor": "지역 단위 수요 검증 기회", "evidence": HYP, "impact": "가설", "source_ids": [], "confidence": "low"}],
            "threats": [{"id": "T1", "factor": "기존 구매 대안과 경쟁 강도 미조사", "evidence": NEED, "impact": "검증 필요", "source_ids": [], "confidence": "low"}],
        }
    if page_id == "15":
        def strategy(strategy_id, factors):
            return {"strategy_id": strategy_id, "strategy": HYP, "linked_factors": factors, "first_action": "인터뷰와 소규모 수요 실험 설계", "success_metric": "사전에 정의할 검증 지표", "priority": "가설", "owner_role": "담당자 지정 필요", "timeline": "일정 확정 필요", "estimated_cost": NEED}
        return {"SO": [strategy("SO1", ["S1", "O1"])], "WO": [strategy("WO1", ["W1", "O1"])], "ST": [strategy("ST1", ["S1", "T1"])], "WT": [strategy("WT1", ["W1", "T1"])]}
    if page_id == "16":
        block = lambda text: [{"statement": text, "status": "to_validate", "evidence": NEED, "source_ids": [], "validation_method": "고객 인터뷰·실험·비용 검토 후 기록"}]
        return {
            "customer_segments": block("20~40대 1인 가구 (사용자 입력 타겟)"),
            "value_propositions": block(HYP), "channels": block(NEED), "customer_relationships": block(NEED),
            "revenue_streams": block("구독 수익 모델 가설; 가격과 반복 구매 검증 필요"), "key_resources": block(NEED),
            "key_activities": block(NEED), "key_partners": block(NEED), "cost_structure": block(NEED),
            "validation_plan": [{"hypothesis": HYP, "method": "소규모 고객 인터뷰·구매 의향 실험", "success_metric": "사전에 정의 필요", "source_ids": [], "status": "to_validate"}],
        }
    if page_id == "17":
        return {"enabled": True, "problem": [HYP], "customer_segments": ["20~40대 1인 가구"], "unique_value_proposition": HYP, "solution": [HYP], "channels": [NEED], "revenue_streams": [NEED], "cost_structure": [NEED], "key_metrics": ["구매 전환·재구매·주문당 공헌이익 정의 필요"], "unfair_advantage": NEED, "hypotheses": [HYP]}
    if page_id == "18":
        return {"persona_ids": ["P1", "P2", "P3", "P4"], "stages": [{"stage": name, "touchpoints": [NEED], "customer_actions": [NEED], "customer_emotions": [NEED], "brand_response": [HYP]} for name in ("인지", "탐색", "구매", "이용", "재구매")], "channels_and_relationship_consistency": [NEED]}
    if page_id == "19":
        return {"color_palette": [{"role": "주조색", "hex": None, "reason": "브랜드 컬러 사용자 확정 필요"}], "typography": NEED, "image_mood": ["검증할 시각 방향"], "design_principles": ["가독성과 생활 맥락을 사용자 조사로 검증"]}
    if page_id == "20":
        return {"concept": HYP, "symbol": NEED, "wordmark": {"text": "살뜰마을", "direction": NEED}, "usage_rules": [NEED], "minimum_size": NEED, "clear_space": NEED}
    if page_id == "21":
        return {"enabled": True, "character_identity": {"status": "추가 정보 필요", "reason": "캐릭터 활용 목적·선호 입력이 없어 구체 디자인을 제안하지 않습니다."}, "symbolic_value": NEED, "emotional_connection": NEED}
    if page_id == "22":
        return {"applications": [{"touchpoint": name, "direction": HYP, "context": NEED, "validation": "실제 사용자·운영 제약과 대조"} for name in ("웹·모바일", "소셜 콘텐츠", "구독 배송 패키지", "인쇄 안내물")], "brand_consistency_notes": [NEED]}
    if page_id == "23":
        plan = [
            {"period": period, "actions": actions, "owner": "담당자 지정 필요", "success_metric": "기준선 수집 후 목표 설정", "status": "to_validate"}
            for period, actions in (
                ("30일", ["입력 정보 확정", "고객 인터뷰 설계"]),
                ("60일", ["지역·상품군 실험", "가격·물류 비용 기록"]),
                ("90일", ["재구매와 단위경제성 검토", "확장·중단 판단"]),
            )
        ]
        return {"plan_30_60_90_days": plan, "validation_hypotheses": [HYP], "kpis": ["인터뷰 완료 수", "구매 전환율", "재구매율", "주문당 공헌이익"], "owners": ["담당자 지정 필요"], "timeline": "기준 일정 확정 필요", "priority": ["수요 검증", "운영 가능성", "경제성"]}
    if page_id == "24":
        return {"sources": [], "calculation_assumptions": ["현재 입력으로 시장 규모·매출 계산을 하지 않음"], "limitations": ["외부 시장 조사 자료 미수집", "고객 인터뷰의 답변 세부 내용 미확인", "사업 운영·재무 자료 미제공"], "validation_records": [{"topic": "시장·경쟁·고객 지표", "status": "source collection required", "source_ids": []}], "evidence_types": {"user_input": ["브랜드명·서비스 유형·타겟"], "ai_estimate": ["명시적으로 가설 처리한 전략 아이디어"], "external_research": []}}
    raise ValueError(f"No conservative data template for {page_id}")


def main():
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    pages = state["pages"]
    for page_id in REPORT_PAGE_ORDER:
        if page_id in pages:
            continue
        status = "insufficient_data" if page_id in {"05", "10", "11", "12", "13", "19", "21", "24"} else "to_validate"
        result = {
            "page_id": page_id,
            "title": REPORT_PAGE_SPECS[page_id]["title"],
            "status": status,
            "data": page_data(page_id),
            "field_guidance": REPORT_PAGE_SPECS[page_id]["fields"],
            "evidence_type": "mixed" if page_id in {"01", "14", "15", "16", "17", "18", "22", "23"} else "ai_estimate",
            "source_ids": [],
            "confidence": "low",
            "validation_notes": ["Gemini API 크레딧 소진으로 이 페이지는 계약에 맞춘 보수적 검증 대기 초안입니다. 실제 출처·수치·운영 사실이 아닙니다."],
        }
        pages[page_id] = apply_backend_calculations(page_id, result)
        errors = validate_page_result(page_id, pages[page_id], pages)
        if errors:
            print(f"INVALID {page_id}: {errors}", flush=True)
            del pages[page_id]
            continue
        state["pages"] = pages
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"DRAFT {len(pages)}/25 {page_id} {result['title']} {status}", flush=True)

    errors = {page_id: validate_page_result(page_id, pages[page_id], pages) for page_id in pages}
    errors = {page_id: error for page_id, error in errors.items() if error}
    print(f"VALIDATION_ERRORS {json.dumps(errors, ensure_ascii=False)}", flush=True)
    print(f"PAGE_COUNT {len(pages)} IDS {','.join(sorted(pages))}", flush=True)
    if len(pages) != 25 or errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
