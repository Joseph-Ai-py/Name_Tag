import unittest

from pdf_builder import assemble_html, build_a3_story, build_c2_typography
from pdf_service import build_pdf_integrity_report


class PdfBuilderRegressionTests(unittest.TestCase):
    def setUp(self):
        self.brand = {
            "brand_name": "실버노드",
            "brand_name_en": "SilverNode",
            "name_meaning": "업무의 흐름을 연결하는 지점",
            "slogan": "일의 맥락을 잇다",
            "story_summary": "실버노드는 반복되는 업무의 맥락을 정리하는 AI 비서입니다.",
            "seed_color": "#666666",
            "seed_color_reason": "차분한 업무 집중감",
        }
        self.data_a = {
            "data_a": {
                "brand_story_full": "실버노드는 흩어진 업무의 맥락을 하나로 연결하기 위해 시작되었습니다.\n반복되는 정리를 줄이고 중요한 판단에 집중하도록 돕습니다."
            }
        }
        self.data_b = {
            "data_b": {
                "customer_swot": {
                    "strategic_reasoning": "초기 고객의 반복 업무를 기준으로 정리한 가설입니다.",
                    "strengths": [{"point": "업무 맥락 정리", "evidence": "반복 입력이 많음", "implication": "초기 사용 장벽이 낮음"}],
                    "weaknesses": [{"point": "새 도구 학습 부담", "evidence": "도입 시간이 필요함", "implication": "온보딩 검증 필요"}],
                    "opportunities": [{"point": "팀 협업 증가", "evidence": "업무 도구가 분산됨", "implication": "연결 경험을 검증"}],
                    "threats": [{"point": "기존 도구 사용 습관", "evidence": "전환 비용이 있음", "implication": "작은 업무부터 검증"}],
                    "brand_responses": [{"swot_type": "Weakness", "customer_issue": "학습 부담", "brand_response": "짧은 시작 흐름 제공", "expected_effect": "첫 성공 경험 확보"}],
                },
                "business_model": {
                    "business_model_summary": "반복 업무 정리 경험을 검증하는 사업 모델 가설입니다.",
                    "customer_problem": {"title": "흩어진 업무", "description": "맥락이 여러 도구에 분산됨"},
                    "value_proposition": {"title": "업무 맥락 연결", "description": "중요한 정보를 한 흐름으로 정리"},
                    "free_experience": {"title": "첫 업무 정리", "description": "하나의 업무를 무료로 정리"},
                    "paid_value": {"title": "팀 업무 연결", "description": "반복 업무의 연결과 관리"},
                    "retention_loop": {"title": "주간 정리", "description": "매주 업무 맥락을 재정리"},
                    "referral_loop": {"title": "팀 공유", "description": "정리 결과를 팀에 공유"},
                    "business_hypotheses": [{"hypothesis": "초기 고객은 주간 업무 정리에 비용을 지불한다.", "why_it_matters": "반복 사용과 지불 의사를 함께 검증해야 합니다.", "validation_method": "5명 인터뷰와 유료 파일럿"}],
                },
            }
        }
        self.data_c = {
            "data_c": {
                "typography": {
                    "primary_font": {"font_name_kr": "고딕 A1", "google_fonts_family": "Gothic A1", "weight_recommendation": 800, "usage_and_reason": "명확한 정보 위계"},
                    "secondary_font": {"font_name_kr": "본고딕", "google_fonts_family": "Noto Sans KR", "weight_recommendation": 400, "usage_and_reason": "긴 본문 가독성"},
                }
            }
        }

    def test_nested_strategy_data_is_rendered(self):
        html = assemble_html(self.brand, self.data_a, self.data_b, self.data_c, {}, {}, {}, [])
        self.assertIn("업무 맥락 정리", html)
        self.assertIn("초기 고객은 주간 업무 정리에 비용을 지불한다.", html)
        self.assertNotIn("강점 데이터가 아직 없습니다.", html)
        self.assertNotIn("등록된 사업 가설이 없습니다.", html)

    def test_template_has_no_cross_brand_sample_copy(self):
        html = build_a3_story(self.data_a["data_a"]) + build_c2_typography(self.data_c["data_c"])
        for term in ["숲결", "폐플라스틱", "업사이클링", "자연 친화"]:
            self.assertNotIn(term, html)
        self.assertIn("실버노드는 흩어진 업무의 맥락을", html)

    def test_dna_and_trace_are_structured(self):
        html = assemble_html(
            self.brand,
            self.data_a,
            self.data_b,
            self.data_c,
            {},
            {"foundation": {"brand_name": "실버노드"}, "business": {"status": "가설"}},
            {"status": "PASS"},
            [{"stage": "B", "decision_type": "customer_strategy", "status": "ai_derived", "user_input": "반복 업무", "ai_interpretation": "정리 필요", "brand_decision": "주간 정리", "rationale": "검증 필요"}],
        )
        self.assertNotIn("'brand_name':", html)
        self.assertIn("Appendix · Internal Review", html)
        self.assertIn("User Input:", html)
        self.assertIn("Brand Decision:", html)

    def test_final_html_integrity_preflight_detects_contamination(self):
        contaminated = {"data_a": {"brand_story_full": "숲결 폐플라스틱 업사이클링 자연 친화"}}
        report = build_pdf_integrity_report(
            self.brand,
            contaminated,
            self.data_b,
            self.data_c,
            {},
            {"foundation": {"brand_name": "실버노드"}},
            {},
            [],
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(issue["category"] == "cross_brand_contamination" for issue in report["issues"]))


if __name__ == "__main__":
    unittest.main()
