from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel

V1_DIR = Path(__file__).resolve().parents[1]
V2_DIR = Path(__file__).resolve().parent
if str(V2_DIR) not in sys.path:
    sys.path.insert(0, str(V2_DIR))
if str(V1_DIR) not in sys.path:
    sys.path.append(str(V1_DIR))

from gemini_client import request_gemini_with_schema  # noqa: E402
from models import BrandData  # noqa: E402

from models import ConversationState, ConversationTurn  # noqa: E402


class ConversationTurnSchema(BaseModel):
    assistant_message: str
    question: dict[str, Any] | None = None
    extracted_facts: list[str] = []
    proposed_updates: list[dict[str, Any]] = []
    next_focus: str = "foundation"
    snapshot_ready: bool = False


def build_conversation_prompt(state: ConversationState, user_message: str) -> str:
    recent = [message.model_dump(mode="json") for message in state.messages[-8:]]
    return f"""당신은 Name Tag의 AI Brand Director입니다.
사용자가 브랜드를 대신 결정하도록 하지 말고, 필요한 질문을 골라 사용자가 직접 결정하도록 도와주세요.
응답은 반드시 JSON만 반환하세요.

[초기 아이디어]
{state.initial_idea or '아직 없음'}

[현재 구조화된 context]
{json.dumps(state.structured_context, ensure_ascii=False)}

[최근 대화]
{json.dumps(recent, ensure_ascii=False)}

[사용자의 새 메시지]
{user_message}

[지침]
- 한 번에 가장 중요한 질문 하나만 선택하세요.
- 질문에는 정확히 4개의 추천 선택지를 제공하거나, 질문이 더 필요 없다면 question을 null로 두세요.
- 사용자가 말하지 않은 인구통계, 시장 수치, 사실을 확정하지 마세요.
- proposed_updates는 AI 제안이며 사용자 확정 전에는 ai_suggested 상태로 표시하세요.
- 다음 focus는 foundation, strategy, customer, business, visual, identity 중 하나입니다.
- 정보가 충분히 쌓이면 snapshot_ready를 true로 설정하세요.

JSON 구조:
{{
  "assistant_message": "사용자에게 보여줄 자연스러운 응답",
  "question": {{
    "question_id": "고유 ID",
    "topic": "foundation|strategy|customer|business|visual|identity",
    "question_text": "질문",
    "options": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"]
  }},
  "extracted_facts": ["사용자 발화에서 확인된 사실"],
  "proposed_updates": [
    {{"path":"foundation.core_idea", "value":"제안값", "interpretation":"이렇게 해석한 이유", "status":"ai_suggested"}}
  ],
  "next_focus": "foundation",
  "snapshot_ready": false
}}"""


def apply_turn(state: ConversationState, user_message: str, turn: ConversationTurn) -> ConversationState:
    state.messages.append({"role": "user", "content": user_message})
    state.messages.append({
        "role": "assistant",
        "content": turn.assistant_message,
        "stage": turn.next_focus,
        "topic": turn.question.topic if turn.question else None,
    })
    state.current_focus = turn.next_focus
    state.raw_results.setdefault("conversation", []).append(turn.model_dump(mode="json"))
    for fact in turn.extracted_facts:
        if fact not in state.structured_context.setdefault("facts", []):
            state.structured_context["facts"].append(fact)
    for update in turn.proposed_updates:
        state.structured_context.setdefault("proposals", []).append(update.model_dump())
    if turn.question:
        state.missing_topics = [turn.question.topic]
    elif turn.next_focus not in state.covered_topics:
        state.covered_topics.append(turn.next_focus)
    return state


def run_conversation_turn(state: ConversationState, user_message: str) -> tuple[ConversationState, ConversationTurn]:
    prompt = build_conversation_prompt(state, user_message)
    response = request_gemini_with_schema(prompt, schema=ConversationTurnSchema)
    turn = ConversationTurn.model_validate(response)
    return apply_turn(state, user_message, turn), turn


def brand_data_from_state(state: ConversationState) -> BrandData:
    context = state.structured_context
    return BrandData(
        initial_idea=state.initial_idea or "",
        business_type=str(context.get("business_type", "")),
        target=str(context.get("target", "")),
        keywords=str(context.get("keywords", "")),
        vibes=list(context.get("vibes", [])),
    )
