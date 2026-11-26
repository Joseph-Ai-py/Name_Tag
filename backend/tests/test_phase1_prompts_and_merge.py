from backend.prompts.nametag_prompts import get_O_interview_prompt
from backend.routers.legacy_naming_router import BrandData, build_o_regen_prompt
from backend.schemas.legacy_customer_strategy_schema import BResponseSchema


def test_o_interview_prompt_includes_brand_context() -> None:
    brand_data = {
        "business_type": "카페",
        "vibes": ["따뜻함", "미니멀"],
        "target": "20-30 직장인",
        "keywords": "스페셜티",
    }

    prompt = get_O_interview_prompt(brand_data)

    assert "업종/서비스: 카페" in prompt
    assert "브랜드 감성: 따뜻함, 미니멀" in prompt
    assert "타겟 고객: 20-30 직장인" in prompt
    assert "추가 키워드: 스페셜티" in prompt


def test_b_merge_preserves_both_reasoning_fields() -> None:
    b1 = {
        "target_strategy_reasoning": "타겟 전략 근거",
        "core_target_group": {
            "definition": "핵심 타겟",
            "demographics": "30대 직장인",
            "lifestyle_keywords": ["바쁨", "효율"],
            "consumption_behavior": "가성비와 신뢰 동시 중시",
        },
        "primary_persona": {
            "name": "민수",
            "age_and_job": "32세 PM",
            "daily_scene": "출근 전 빠른 선택",
            "pain_point_and_desire": "시간 절약과 품질 확보",
            "emotional_needs": ["안심", "예측 가능성"],
            "deal_breaker": "복잡한 사용성",
        },
        "secondary_personas": [
            {
                "id": 1,
                "name_and_demographic": "지연 (29, 마케터)",
                "character_type": "트렌드형",
                "why_they_buy": "새로운 경험 추구",
            }
        ],
        "emotional_triggers": [
            {"trigger": "후기", "reason": "사회적 증거"}
        ],
    }

    b2 = {
        "journey_strategy_reasoning": "여정 전략 근거",
        "customer_journey_map": [
            {
                "stage": "인지",
                "touchpoint": "SNS",
                "customer_emotion": "흥미",
                "brand_action": "짧은 데모 제공",
            }
        ],
    }

    merged = {**b1, **b2}
    parsed = BResponseSchema.model_validate(merged)

    assert parsed.target_strategy_reasoning == "타겟 전략 근거"
    assert parsed.journey_strategy_reasoning == "여정 전략 근거"


def test_o_regen_prompt_uses_brand_data_not_brand_info() -> None:
    brand_data = BrandData(
        business_type="교육",
        vibes=["신뢰", "친근"],
        target="초등 학부모",
        keywords="기초학력",
    )
    prompt = build_o_regen_prompt(brand_data, {"selected": {"name": "A"}}, "brand_name")

    assert "brand_data" in prompt
    assert "context" in prompt
    assert "brand_info" not in prompt
