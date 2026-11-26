import json

from backend.pdf.report_v2_pdf import build_report_v2_compact_html, build_report_v2_html
from backend.routers import report_v2
from backend.services.gemini_service import parse_ai_response
from backend.prompts.nametag_prompts_v2 import (
    COMMON_RULES,
    FEW_SHOT_EXAMPLES,
    PAGE_PROMPT_BUILDERS,
    REPORT_PAGE_ORDER,
    REPORT_PAGE_SPECS,
    ReportHarness,
    V2_SYSTEM_PROMPT,
    apply_backend_calculations,
    build_report_generation_plan,
    build_report_interview_prompt,
    build_named_report_page_prompt,
    build_report_page_prompt,
    next_report_interviews,
    next_report_pages,
    validate_interview_result,
    validate_page_result,
)
from backend.pdf.report_v2_pdf import PAGE_RENDERERS
from backend.schemas.report_v2 import ReportPageSchema, ReportV2PdfRequest


def test_v2_prompt_interview_example_matches_interview_rules() -> None:
    prompt = build_report_interview_prompt("brand", {"brand": {"business_type": "카페"}})
    sample_text = prompt.split("반환 구조 예시:\n", 1)[1].split("\n질문은 5~10개", 1)[0]
    sample = json.loads(sample_text)

    assert sample["required_question_count"] == len(sample["questions"]) == 5
    assert all(len(question["options"]) == 4 for question in sample["questions"])
    assert validate_interview_result(sample) == []


def test_v2_rejects_malformed_question_ids_and_choices() -> None:
    sample = {
        "required_question_count": 5,
        "questions": [
            {"question_id": index, "question_text": "질문", "options": ["A", "B", "C", "D"]}
            for index in range(1, 6)
        ],
    }
    sample["questions"][4]["question_id"] = [5]
    sample["questions"][0]["options"][0] = "  "
    errors = validate_interview_result(sample)

    assert "question_id values must be integers" in errors
    assert "question 1 options must be non-empty strings" in errors


def test_report_page_specs_have_complete_order_and_acyclic_plan() -> None:
    plan = build_report_generation_plan()
    assert REPORT_PAGE_ORDER == [f"{index:02d}" for index in range(25)]
    assert {entry["page_id"] for entry in plan} == set(REPORT_PAGE_SPECS)
    assert len(plan) == 25
    assert set(PAGE_PROMPT_BUILDERS) == set(REPORT_PAGE_ORDER)
    assert set(PAGE_RENDERERS) == set(REPORT_PAGE_ORDER)


def test_named_page_prompt_function_is_selected_by_page_id() -> None:
    prompt = build_named_report_page_prompt("00", {"brand": {"business_type": "카페"}})
    assert "Cover" in prompt


def test_initial_ready_pages_and_conditional_page_handling() -> None:
    assert next_report_pages(set(), set(), {"17": False, "21": False}) == ["00", "02", "06"]
    assert "17" in next_report_pages({"06", "09", "10", "11"}, set(), {"17": True})


def test_interviews_unlock_only_after_context_pages_are_completed() -> None:
    assert next_report_interviews(set(), set()) == ["brand"]
    assert "business" not in next_report_interviews(set(), {"brand"})
    assert "business" in next_report_interviews({"02", "03", "04"}, {"brand"})


def test_ai_json_parser_preserves_nested_objects_and_braces_in_strings() -> None:
    parsed = parse_ai_response('prefix ```json\n{"data":{"why":{"text":"brace } stays"}}}\n``` suffix')
    assert parsed["data"]["why"]["text"] == "brace } stays"


def test_report_harness_generates_and_validates_cover_without_model_call() -> None:
    calls = []

    def fake_generate(prompt: str) -> dict:
        calls.append(prompt)
        return FEW_SHOT_EXAMPLES["00"]["output"]

    harness = ReportHarness(fake_generate, max_repairs=0)
    result = harness.generate_page("00", {"brand": {"business_type": "미입력"}})

    assert result["page_id"] == "00"
    assert validate_page_result("00", result) == []
    assert len(calls) == 1


def test_v2_pdf_uses_required_mixed_page_layouts_and_escapes_content() -> None:
    html = build_report_v2_html(
        {
            "05": {"page_id": "05", "title": "Brand Positioning", "data": {"pop": "<safe>"}},
            "10": {"page_id": "10", "title": "Value Proposition", "data": {}},
        }
    )

    assert "@page report_05 { size: A3 landscape; margin: 15mm; }" in html
    assert "@page report_10 { size: A3 landscape; margin: 15mm; }" in html
    assert "&lt;safe&gt;" in html


def test_page_prompts_request_limited_keyword_emphasis() -> None:
    prompt = build_report_page_prompt("02", {})
    assert "Markdown **굵게**" in COMMON_RULES
    assert "문장마다 1~2개" in prompt
    assert "JSON 키, ID, 제목" in V2_SYSTEM_PROMPT


def test_pdf_renders_ai_bold_markdown_and_escapes_markup() -> None:
    html = build_report_v2_html({
        "00": {
            "page_id": "00",
            "title": "Cover",
            "status": "complete",
            "data": {
                "brand_name": "Sample",
                "key_sentence": "**시간 절약**이 핵심입니다.",
                "brand_promise": "<script>**안심 배송**</script>",
                "industry": "서비스",
            },
        },
    })
    assert '<strong class="emphasis">시간 절약</strong>' in html
    assert '&lt;script&gt;<strong class="emphasis">안심 배송</strong>&lt;/script&gt;' in html
    assert "<script>" not in html


def test_full_report_compact_pdf_keeps_named_page_breaks_and_bold_emphasis() -> None:
    html = build_report_v2_compact_html({
        "00": {"page_id": "00", "title": "Cover", "status": "complete", "confidence": "medium", "data": {"brand_name": "Sample", "key_sentence": "**다정한 살림**"}},
        "02": {"page_id": "02", "title": "Brand Foundation", "status": "to_validate", "confidence": "low", "data": {"brand_essence": "가벼운 원룸을 만드는 **다정한 살림**"}, "validation_notes": ["**검증 필요**"]},
    })
    assert "@page report_00 { size: A4 portrait; margin: 0mm;" in html
    assert "@page report_02 { size: A4 portrait; margin: 12mm; @bottom-left" in html
    assert 'style="page: report_02; font-size:' in html
    assert '<strong class="emphasis">다정한 살림</strong>' in html
    assert '<strong class="emphasis">검증 필요</strong>' in html
    assert "**다정한 살림**" not in html


def test_compact_pdf_uses_readable_page_components_and_single_flow_footer() -> None:
    html = build_report_v2_compact_html({
        "07": {"page_id": "07", "title": "Personas", "status": "to_validate", "confidence": "low", "data": {
            "personas": [{"persona_id": "P1", "name": "첫 고객", "segment": "1인 가구", "pains": ["정리 시간이 부족함"]}]
        }, "validation_notes": ["인터뷰로 검증 필요"]},
        "16": {"page_id": "16", "title": "Business Model Canvas", "status": "to_validate", "confidence": "low", "data": {
            "customer_segments": ["1인 가구"], "value_propositions": [], "channels": [], "revenue_streams": [],
            "cost_structure": [], "key_partners": [], "key_activities": [], "key_resources": [], "customer_relationships": [],
        }},
    })
    assert 'class="persona-card"' in html
    assert 'class="canvas-grid"' in html
    assert 'class="status-badge caution"' in html
    assert 'class="insight-bar"' not in html  # no unsupported insight is invented
    assert 'font-size:10.0pt' in html
    assert 'position:fixed' not in html
    assert '@bottom-left' in html
    assert '<footer' not in html
    assert 'industry:' not in html


def test_cover_pdf_page_uses_cover_json_fields_and_not_raw_json_dump() -> None:
    cover = FEW_SHOT_EXAMPLES["00"]["output"]
    validated = ReportPageSchema.model_validate(cover).model_dump(mode="json")
    html = build_report_v2_html({"00": validated})

    assert validated["field_guidance"] == REPORT_PAGE_SPECS["00"]["fields"]
    assert "BUILD A BRAND THAT MEANS BUSINESS" in html
    assert cover["data"]["brand_name"] in html
    assert cover["data"]["key_sentence"] in html
    assert cover["data"]["report_date"] in html
    assert "<pre>" not in html


def test_brand_pages_use_the_editorial_layout_and_notion_frameworks() -> None:
    pages = {
        "02": {"page_id": "02", "title": "Brand Foundation", "status": "complete", "data": {
            "golden_circle": {"why": "WHY", "how": "HOW", "what": "WHAT"},
            "brand_essence": "Essence", "customer_connection": "Customer connection",
        }, "evidence_type": "user_input", "confidence": "medium"},
        "03": {"page_id": "03", "title": "Brand Identity", "status": "complete", "data": {
            "identity_prism": {key: key for key in ("physique", "personality", "culture", "relationship", "reflection", "self_image")},
            "archetype": "Creator", "core_values_3_to_5": ["trust"], "behavior_definitions": ["act clearly"],
        }, "evidence_type": "ai_estimate", "confidence": "medium"},
        "04": {"page_id": "04", "title": "Brand Story", "status": "complete", "data": {
            "naming_origin_meaning_pronunciation_symbolism": "Name", "story": {key: key for key in ("origin", "problem", "belief", "promise")},
            "slogan": "Slogan", "founder_experience_is_not_fabricated": "Not provided",
        }, "evidence_type": "user_input", "confidence": "medium"},
    }
    html = build_report_v2_html(pages)
    assert "BRAND ESSENCE" in html
    assert "BRAND IDENTITY PRISM" in html
    assert "ORIGIN" in html and "PROMISE" in html
    assert "--seed: #B78367" in html
    assert 'font-family: "Noto Sans KR"' in html
    assert "border-radius: 14px" in html
    assert ".cover-page { display: block; position: relative; background: linear-gradient" in html
    assert ".cover-main { margin-top: 22mm; }" in html
    assert ".cover-bottom { position: absolute;" in html
    assert "02 / 25" in html


def test_every_page_id_has_a_named_pdf_renderer() -> None:
    pages = {
        page_id: {
            "page_id": page_id,
            "title": REPORT_PAGE_SPECS[page_id]["title"],
            "status": "insufficient_data",
            "data": {},
            "evidence_type": "insufficient_data",
            "source_ids": [],
            "confidence": "low",
        }
        for page_id in REPORT_PAGE_ORDER
    }
    html = build_report_v2_html(pages)
    for page_id in REPORT_PAGE_ORDER:
        assert f"report_{page_id}" in html
    assert "<pre>" not in html


def test_pdf_request_schema_checks_page_key_and_layout_contract() -> None:
    cover = FEW_SHOT_EXAMPLES["00"]["output"]
    request = ReportV2PdfRequest.model_validate({
        "pages": {"00": cover},
        "page_layouts": [{"page_id": "00", "paper_size": "A4", "orientation": "portrait", "margins_mm": 12}],
        "brand_name": "NAME TAG",
    })
    assert request.pages["00"].page_id == "00"


def test_backend_calculates_vpc_coordinates_from_prompt_scores() -> None:
    result = {
        "data": {
            "value_fit_inputs": {
                "P1": {factor: {"score": 100, "reasoning": "근거"} for factor in "SF IAPGDC".replace(" ", "")}
            },
            "persona_vpcs": [{"persona_id": "P1"}],
        }
    }

    computed = apply_backend_calculations("10", result)

    assert computed["data"]["computed_coordinates"]["P1"] == {
        "x": 100.0,
        "y": 100.0,
        "quadrant": "high_problem_high_fit",
    }
    assert computed["data"]["persona_vpcs"][0]["computed_coordinates"]["x"] == 100.0


def test_page_10_validator_reports_malformed_value_fit_inputs_without_crashing() -> None:
    prior_pages = {
        "07": {"data": {"personas": [{"persona_id": "P1"}, {"persona_id": "P2"}]}},
        "08": {"data": {"personas": [{"persona_id": "P3"}, {"persona_id": "P4"}]}},
    }
    result = {
        "page_id": "10",
        "title": "Value Proposition",
        "status": "to_validate",
        "data": {"persona_vpcs": [], "value_fit_inputs": [{"persona_id": "P1"}]},
        "confidence": "low",
        "source_ids": [],
        "validation_notes": [],
    }

    errors = validate_page_result("10", result, prior_pages)

    assert "value_fit_inputs must be an object keyed by canonical persona ID" in errors


def test_backend_calculates_shared_positioning_coordinates() -> None:
    result = {
        "data": {
            "axis_x": {"evaluation_factors": [{"factor_id": "price", "weight": 1.0}]},
            "axis_y": {"evaluation_factors": [{"factor_id": "personalization", "weight": 1.0}]},
            "entities": [{
                "entity_id": "our_idea",
                "factor_scores": [
                    {"factor_id": "price", "score": 40},
                    {"factor_id": "personalization", "score": 80},
                ],
            }],
        }
    }

    computed = apply_backend_calculations("05", result)
    assert computed["data"]["computed_coordinates"]["our_idea"] == {"x": 40.0, "y": 80.0}


def test_v2_harness_uses_v2_system_instruction(monkeypatch) -> None:
    captured = {}

    def fake_request(prompt: str, *, system_instruction: str) -> dict:
        captured["prompt"] = prompt
        captured["system_instruction"] = system_instruction
        return {}

    monkeypatch.setattr(report_v2, "request_gemini_text", fake_request)
    harness = report_v2._harness({})
    harness.generate_json("V2 prompt")

    assert captured["prompt"] == "V2 prompt"
    assert "NAME TAG V2" in captured["system_instruction"]
