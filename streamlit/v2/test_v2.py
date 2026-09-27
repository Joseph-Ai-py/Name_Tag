import unittest

from brand_document import build_brand_document, build_pdf_view_model
from conversation import apply_turn
from models import ConversationQuestion, ConversationState, ConversationTurn


class V2ConversationTests(unittest.TestCase):
    def test_turn_updates_history_and_raw_results(self):
        state = ConversationState(initial_idea="기록으로 나를 이해하는 서비스")
        turn = ConversationTurn(
            assistant_message="가장 먼저 얻고 싶은 변화는 무엇인가요?",
            question=ConversationQuestion(
                question_id="foundation_1",
                topic="foundation",
                question_text="가장 먼저 얻고 싶은 변화는 무엇인가요?",
                options=["발견", "정리", "추천", "표현"],
            ),
            extracted_facts=["기록을 통해 자기 이해를 돕고 싶다"],
            proposed_updates=[{"path": "foundation.core_idea", "value": "자기 발견", "interpretation": "기록의 목적"}],
        )
        updated = apply_turn(state, "내 취향을 발견하고 싶어요", turn)
        self.assertEqual(len(updated.messages), 2)
        self.assertEqual(updated.raw_results["conversation"][0]["next_focus"], "foundation")
        self.assertEqual(updated.structured_context["facts"], ["기록을 통해 자기 이해를 돕고 싶다"])

    def test_document_and_pdf_view_model_keep_separate_layers(self):
        state = ConversationState(raw_results={"O": {"brand_name": "알고맵"}})
        document = build_brand_document(state)
        view_model = build_pdf_view_model(document)
        self.assertEqual(document.identity["brand_name"], "알고맵")
        self.assertEqual(view_model["O"]["brand_name"], "알고맵")


if __name__ == "__main__":
    unittest.main()
