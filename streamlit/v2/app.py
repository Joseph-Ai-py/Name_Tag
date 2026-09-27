from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

V1_DIR = Path(__file__).resolve().parents[1]
V2_DIR = Path(__file__).resolve().parent
if str(V2_DIR) not in sys.path:
    sys.path.insert(0, str(V2_DIR))
if str(V1_DIR) not in sys.path:
    sys.path.append(str(V1_DIR))

from brand_dna import build_trace  # noqa: E402
from models import ConversationState  # noqa: E402

from brand_document import build_brand_document, build_pdf_view_model, refresh_integrity  # noqa: E402
from conversation import run_conversation_turn  # noqa: E402
from pipeline import confirm_brand_candidate, generate_full_pipeline, generate_o_candidates, generate_pdf  # noqa: E402


st.set_page_config(page_title="Name Tag v2", page_icon="✦", layout="wide")


def get_state() -> ConversationState:
    if "v2_conversation_state" not in st.session_state:
        st.session_state.v2_conversation_state = ConversationState()
    return st.session_state.v2_conversation_state


def set_state(state: ConversationState) -> None:
    st.session_state.v2_conversation_state = state


def conversation_text(state: ConversationState) -> str:
    return "\n\n".join(f"{message.role}: {message.content}" for message in state.messages)


def render_pipeline_controls(state: ConversationState) -> None:
    candidates = state.raw_results.get("O_candidates", [])
    brand_info = state.raw_results.get("O")
    st.divider()
    st.subheader("기존 Brand Pipeline 연결")
    st.caption("대화에서 충분히 방향이 잡히면 기존 O/A/B/B4/B5/C/DE 생성 파이프라인으로 이어집니다.")

    if not candidates and not brand_info:
        if st.button("대화에서 브랜드 초안 제안받기", type="primary"):
            try:
                with st.spinner("대화 내용을 바탕으로 브랜드 초안을 제안하는 중입니다..."):
                    generated = generate_o_candidates(state.initial_idea or "", conversation_text(state))
                state.raw_results["O_candidates"] = generated
                set_state(state)
                st.rerun()
            except Exception as exc:
                st.error(f"브랜드 초안을 만들지 못했습니다: {exc}")
        return

    if candidates and not brand_info:
        labels = [
            f"{index + 1}. {candidate.get('brand_name', '이름 없음')} · {candidate.get('slogan', '')}"
            for index, candidate in enumerate(candidates)
        ]
        selected = st.selectbox("브랜드 초안 선택", range(len(candidates)), format_func=lambda index: labels[index])
        if st.button("이 초안으로 브랜드 방향 확정"):
            try:
                state.raw_results["O"] = confirm_brand_candidate(candidates, selected)
                state.decision_traces.append({
                    "stage": "O",
                    "decision_type": "brand_foundation",
                    "user_input": labels[selected],
                    "ai_interpretation": "대화 context에서 제안된 브랜드 초안",
                    "brand_decision": state.raw_results["O"].get("brand_name", ""),
                    "status": "user_confirmed",
                })
                set_state(state)
                st.rerun()
            except Exception as exc:
                st.error(f"브랜드 방향을 확정하지 못했습니다: {exc}")
        return

    st.success(f"확정 브랜드: {brand_info.get('brand_name', '')}")
    if "A" not in state.raw_results and st.button("A/B/B4/B5/C/DE 전체 생성", type="primary"):
        try:
            with st.spinner("기존 Brand Strategy와 Identity pipeline을 실행하는 중입니다..."):
                results = generate_full_pipeline(brand_info, conversation_text(state))
            state.raw_results.update({key: value for key, value in results.items() if key != "brand_info"})
            set_state(state)
            st.success("기존 파이프라인 결과를 v2 BrandDocument에 연결했습니다.")
            st.rerun()
        except Exception as exc:
            st.error(f"전체 pipeline을 실행하지 못했습니다: {exc}")
    elif "A" in state.raw_results:
        if st.button("BrandDocument를 PDF로 렌더링"):
            try:
                with st.spinner("확정된 BrandDocument를 PDF로 렌더링하는 중입니다..."):
                    pdf_bytes = generate_pdf(state.raw_results, state.decision_traces)
                st.session_state.v2_pdf_bytes = pdf_bytes
                st.success("PDF 렌더링을 완료했습니다.")
            except Exception as exc:
                st.error(f"PDF를 만들지 못했습니다: {exc}")
        if st.session_state.get("v2_pdf_bytes"):
            st.download_button(
                "PDF 다운로드",
                data=st.session_state.v2_pdf_bytes,
                file_name="nametag_v2_guideline.pdf",
                mime="application/pdf",
            )


def render_snapshot(state: ConversationState) -> None:
    document = refresh_integrity(build_brand_document(state))
    st.subheader("현재까지 이해한 브랜드")
    facts = state.structured_context.get("facts", [])
    proposals = state.structured_context.get("proposals", [])
    if facts:
        st.markdown("**확인된 사용자 생각**")
        for fact in facts:
            st.write(f"- {fact}")
    if proposals:
        st.markdown("**AI 제안, 아직 확정 전**")
        for proposal in proposals[-6:]:
            st.write(f"- `{proposal.get('path', '')}`: {proposal.get('value', '')}")
    st.caption(f"현재 focus: {state.current_focus or 'foundation'} · Integrity: {document.integrity.get('status', 'NOT_CHECKED')}")
    with st.expander("BrandDocument preview", expanded=False):
        st.json(build_pdf_view_model(document))


def main() -> None:
    state = get_state()
    st.title("NAME TAG")
    st.caption("아이디어를 브랜드 DNA로 바꾸는 Conversation-First Brand Studio")
    st.write("브랜드에 대해 아직 정리되지 않은 생각도 괜찮습니다. 편하게 이야기해 주세요.")

    if not state.messages:
        initial = st.text_area(
            "첫 이야기",
            placeholder="예: 유튜브 시청 기록을 바탕으로 내가 어떤 사람인지 이해하는 서비스를 만들고 싶어요.",
            height=130,
        )
        if st.button("대화 시작", type="primary", disabled=not initial.strip()):
            state.initial_idea = initial.strip()
            try:
                with st.spinner("지금 가장 중요한 질문을 고르는 중입니다..."):
                    state, _ = run_conversation_turn(state, initial.strip())
                set_state(state)
                st.rerun()
            except Exception as exc:
                st.error(f"대화를 시작하지 못했습니다: {exc}")
        st.info("아직 정하지 못했다면 '브랜드를 만들고 싶은데 아무것도 정하지 못했어요'라고 시작해도 됩니다.")
        return

    for message in state.messages:
        with st.chat_message(message.role):
            st.write(message.content)

    pending = None
    if state.raw_results.get("conversation"):
        pending = state.raw_results["conversation"][-1].get("question")
    if pending:
        st.markdown(f"**{pending.get('question_text', '')}**")
        cols = st.columns(2)
        for index, option in enumerate(pending.get("options", [])):
            if cols[index % 2].button(option, key=f"v2_option_{pending.get('question_id')}_{index}"):
                try:
                    state, _ = run_conversation_turn(state, option)
                    set_state(state)
                    st.rerun()
                except Exception as exc:
                    st.error(f"답변을 처리하지 못했습니다: {exc}")

    direct = st.chat_input("직접 이야기해 주세요")
    if direct:
        try:
            with st.spinner("말씀하신 내용을 브랜드 context에 반영하는 중입니다..."):
                state, _ = run_conversation_turn(state, direct)
            set_state(state)
            st.rerun()
        except Exception as exc:
            st.error(f"대화를 처리하지 못했습니다: {exc}")

    render_snapshot(state)
    render_pipeline_controls(state)


if __name__ == "__main__":
    main()
