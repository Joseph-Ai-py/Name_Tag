from __future__ import annotations

import streamlit.components.v1 as components
from pdf_service import build_download_filename, generate_pdf_bytes, generate_a_only_html

import json
import base64
from pathlib import Path
from typing import Any

import streamlit as st

from logic_a import generate_a_interview_questions, generate_section_a, regenerate_a_field
from logic_b import generate_b_interview_questions, generate_section_b, regenerate_b_field
from logic_c import generate_c_interview_questions, generate_section_c, regenerate_c_field
from logic_de import (
    generate_character_only,
    generate_de_interview_questions,
    generate_logo_only,
    generate_section_de,
    regenerate_de_field,
)
from logic_o import apply_candidate_mix, generate_o_candidates, generate_o_interview_questions, regenerate_o_field
from models import BrandData, BrandInfo
from pdf_service import build_download_filename, generate_pdf_bytes
from state import get_state, initialize_session_state, reset_workflow_state, set_state

STEP_LABELS = ["O", "A", "B", "C", "DE", "Preview"]
STEP_TITLES = ["브랜드 초안", "철학/스토리", "타겟/여정", "비주얼", "로고/캐릭터", "PDF 미리보기"]


# -----------------------------
# 공통 유틸
# -----------------------------
def _set_error(message: str | None) -> None:
    set_state("error", message)


def _render_error() -> None:
    err = get_state("error")
    if err:
        st.error(err)


def _load_brand_info() -> BrandInfo | None:
    raw = get_state("brand_info")
    if not raw:
        st.info("먼저 Section O에서 브랜드를 확정해 주세요.")
        return None
    return BrandInfo(**raw)


def _ensure_list_state(key: str, length: int) -> list[str]:
    current = get_state(key)
    if not isinstance(current, list) or len(current) != length:
        current = [""] * length
        set_state(key, current)
    return list(current)


def _format_interview_answers(questions: list[dict[str, Any]], answers: list[str]) -> str:
    lines: list[str] = []
    for i, q in enumerate(questions, start=1):
        question_text = q.get("question_text", "")
        answer_text = answers[i - 1] if i - 1 < len(answers) else ""
        lines.append(f"{i}. {question_text}\nA: {answer_text}")
    return "\n\n".join(lines)


def _strip_option_prefix(text: str) -> str:
    parts = text.split(". ", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return text


def _render_progress_header() -> None:
    current_step = int(get_state("current_step") or 0)
    st.title("나만의 브랜드 정체성 만들기")
    st.caption("섹션 O -> A -> B -> C -> DE를 순서대로 진행한 뒤 PDF를 생성합니다.")

    progress = (current_step + 1) / len(STEP_LABELS)
    st.progress(progress)
    cols = st.columns(len(STEP_LABELS))
    for idx, col in enumerate(cols):
        active = "[현재]" if idx == current_step else ""
        col.markdown(f"**{STEP_LABELS[idx]}**\n\n{STEP_TITLES[idx]} {active}")


def render_sidebar_navigation() -> None:
    with st.sidebar:
        st.header("탐색")
        current_step = int(get_state("current_step") or 0)
        st.caption(f"현재 단계: {STEP_LABELS[current_step]} - {STEP_TITLES[current_step]}")

        for idx, label in enumerate(STEP_LABELS):
            if st.button(f"{label} 이동", use_container_width=True, key=f"nav_{label}"):
                set_state("current_step", idx)
                st.rerun()

        st.divider()
        if st.button("워크플로우 초기화", use_container_width=True):
            reset_workflow_state()
            st.rerun()

# -----------------------------
# 인터뷰 카드 렌더
# -----------------------------
def render_interview_card(section: str, question_pack: dict[str, Any], output_state_key: str) -> None:
    questions = question_pack.get("questions") or []
    if not questions:
        return

    # --- 🎨 커스텀 CSS 주입 ---
    # 선택된 버튼(primary)의 배경색을 지우고, 테마에 맞는 텍스트 색상(var(--text-color))으로 테두리를 칠합니다.
    # 라이트모드에서는 검은색 계열, 다크모드에서는 흰색 계열로 자동 변경됩니다.
    st.markdown(
        """
        <style>
        /* 확실한 색상을 직접 주입하여 눈이 편안한 꽉 찬 버튼으로 만듭니다 */
        button[kind="primary"] {
            background-color: #5C6B73 !important; /* 차분한 블루 그레이 색상 */
            border: 1px solid #5C6B73 !important;
            border-radius: 8px !important;        /* 모서리를 살짝 둥글게 */
        }
        
        /* 버튼 내부 글자 색상 강제 고정 */
        button[kind="primary"] p {
            color: #FFFFFF !important;            /* 글자는 무조건 흰색 */
            font-weight: bold !important;
        }

        button[kind="primary"]:hover {
            background-color: #4A565C !important; /* 마우스를 올리면 살짝 더 어두워짐 */
            border: 1px solid #4A565C !important;
        }
        
        button[kind="primary"]:active {
            background-color: #384247 !important; /* 클릭 시 더 진한 색상으로 타격감 추가 */
            border: 1px solid #384247 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    answers_key = f"{section}_answers"
    idx_key = f"{section}_current_idx"
    custom_key = f"{section}_custom_input"

    answers = _ensure_list_state(answers_key, len(questions))
    current_idx = int(get_state(idx_key) or 0)
    current_idx = max(0, min(current_idx, len(questions) - 1))
    set_state(idx_key, current_idx)

    q = questions[current_idx]
    reasoning = question_pack.get("reasoning", "")

    with st.container(border=True):
        st.markdown("### 인터뷰 카드")
        if reasoning:
            with st.expander("AI 질문 생성 이유", expanded=False):
                st.write(reasoning)

        st.write(f"질문 {current_idx + 1} / {len(questions)}")
        st.markdown(f"**{q.get('question_text', '')}**")

        options = q.get("options") or []
        col1, col2 = st.columns(2)
        for i, option in enumerate(options):
            stripped = _strip_option_prefix(str(option))
            target_col = col1 if i % 2 == 0 else col2
            
            is_selected = (answers[current_idx] == stripped)
            button_type = "primary" if is_selected else "secondary"
            
            if target_col.button(stripped, key=f"{section}_opt_{current_idx}_{i}", use_container_width=True, type=button_type):
                answers[current_idx] = stripped
                set_state(answers_key, answers)
                st.rerun()

        st.text_input(
            "직접 입력(선택)",
            value=str(get_state(custom_key) or ""),
            key=f"{section}_custom_field",
            placeholder="선택지가 아니라 직접 작성하고 싶으면 입력",
        )

        c1, c2, c3 = st.columns(3)
        if c1.button("직접 입력 저장", key=f"{section}_custom_save"):
            value = st.session_state.get(f"{section}_custom_field", "").strip()
            if value:
                answers[current_idx] = value
                set_state(answers_key, answers)
                set_state(custom_key, value)
                st.success("현재 질문 답변으로 저장했습니다.")
                st.rerun()

        if c2.button("이전", key=f"{section}_prev", use_container_width=True, disabled=current_idx == 0):
            set_state(idx_key, current_idx - 1)
            st.rerun()

        next_label = "인터뷰 완료" if current_idx == len(questions) - 1 else "다음"
        if c3.button(next_label, key=f"{section}_next", use_container_width=True):
            if not answers[current_idx]:
                st.warning("현재 질문의 답변을 먼저 선택하거나 입력해 주세요.")
            elif current_idx < len(questions) - 1:
                set_state(idx_key, current_idx + 1)
                st.rerun()
            else:
                formatted = _format_interview_answers(questions, answers)
                set_state(output_state_key, formatted)
                st.success("인터뷰 답변 저장 완료")
                if section == "O":
                    try:
                        brand_data_raw = get_state("brand_data") or {}
                        brand_data = BrandData(**brand_data_raw)
                        resp = generate_o_candidates(brand_data, formatted)
                        set_state("section_o_candidates", resp.get("candidates", []))
                        st.success("인터뷰 기반 후보 생성을 완료했습니다.")
                    except Exception as exc:
                        _set_error(str(exc))


# -----------------------------
# 후보 재생성/적용
# -----------------------------
def _render_regen_panel(
    section: str,
    target_keys: list[str],
    regenerate_fn,
    context_data: dict[str, Any],
    brand_info: BrandInfo,
    apply_target_data_key: str | None = None,
) -> None:
    with st.expander("필드 재생성", expanded=False):
        target = st.selectbox("재생성 대상", options=target_keys, key=f"regen_target_{section}")

        if st.button("재생성 실행", key=f"regen_run_{section}"):
            try:
                _set_error(None)
                result = regenerate_fn(brand_info, {"existing": context_data}, target)
                cands = result.get("result", {}).get("candidates", [])
                set_state(f"regen_cands_{section}", cands)
                set_state(f"regen_target_{section}_picked", target)
            except Exception as exc:
                _set_error(str(exc))

        cands = get_state(f"regen_cands_{section}") or []
        chosen_target = get_state(f"regen_target_{section}_picked")
        if cands:
            st.write(f"재생성 후보 - {chosen_target}")
            for i, cand in enumerate(cands):
                text = cand.get("text") if isinstance(cand, dict) else str(cand)
                rationale = cand.get("rationale") if isinstance(cand, dict) else ""
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**후보 {i + 1}**: {text}")
                    if rationale:
                        st.caption(rationale)
                with col2:
                    if st.button("적용", key=f"regen_apply_{section}_{i}"):
                        value = text
                        if apply_target_data_key:
                            data = dict(get_state(apply_target_data_key) or {})
                            data[chosen_target] = value
                            set_state(apply_target_data_key, data)
                        if chosen_target in ["brand_name", "name_meaning", "slogan", "story_summary"]:
                            new_brand = dict(brand_info.model_dump())
                            new_brand[chosen_target] = value
                            set_state("brand_info", new_brand)
                        st.success("후보를 적용했습니다.")


# -----------------------------
# Section O
# -----------------------------
def render_step_o() -> None:
    st.header("Section O - 브랜드 초안 입력과 MVB 선택")
    
    # --- 🎨 커스텀 CSS 주입 ---
    # 브랜드 감성 선택 버튼(primary)을 다크모드/라이트모드에 맞춰 테두리만 표시되도록 스타일 변경
    st.markdown(
        """
        <style>
        /* 확실한 색상을 직접 주입하여 눈이 편안한 꽉 찬 버튼으로 만듭니다 */
        button[kind="primary"] {
            background-color: #5C6B73 !important; /* 차분한 블루 그레이 색상 */
            border: 1px solid #5C6B73 !important;
            border-radius: 8px !important;        /* 모서리를 살짝 둥글게 */
        }
        
        /* 버튼 내부 글자 색상 강제 고정 */
        button[kind="primary"] p {
            color: #FFFFFF !important;            /* 글자는 무조건 흰색 */
            font-weight: bold !important;
        }

        button[kind="primary"]:hover {
            background-color: #4A565C !important; /* 마우스를 올리면 살짝 더 어두워짐 */
            border: 1px solid #4A565C !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    _render_error()

    raw = get_state("brand_data") or {}
    vibe_options = ["모던", "미니멀", "따뜻함", "프리미엄", "감성", "자연", "테크", "클래식"]

    c1, c2 = st.columns(2)
    with c1:
        business_type = st.text_input("업종 / 서비스", value=raw.get("business_type", ""), placeholder="예: 프리미엄 베이커리")
    with c2:
        target = st.text_input("타겟 고객", value=raw.get("target", ""), placeholder="예: 감도 높은 20~30대")

    keywords = st.text_input("추가 키워드", value=raw.get("keywords", ""), placeholder="예: 지속가능성, 감성, 세련됨")

    # --- 감성 키워드 버튼형 선택 UI ---
    st.markdown("**브랜드 감성 (최대 4개 선택)**")
    
    current_vibes = raw.get("vibes", [])
    if not isinstance(current_vibes, list):
        current_vibes = []
        
    # 4개의 열을 만들어 버튼을 격자 형태로 배치
    cols = st.columns(4)
    for i, vibe in enumerate(vibe_options):
        col = cols[i % 4]
        is_selected = vibe in current_vibes
        
        # 선택된 상태면 'primary', 아니면 'secondary'
        button_type = "primary" if is_selected else "secondary"
        
        # 4개가 이미 선택되었고, 현재 버튼이 선택되지 않은 버튼이라면 비활성화
        is_disabled = (not is_selected) and (len(current_vibes) >= 4)
        
        if col.button(vibe, key=f"vibe_btn_{vibe}", use_container_width=True, type=button_type, disabled=is_disabled):
            if is_selected:
                current_vibes.remove(vibe)
            else:
                current_vibes.append(vibe)
                
            raw["vibes"] = current_vibes
            set_state("brand_data", raw)
            st.rerun()

    vibes = current_vibes
    brand_data = BrandData(business_type=business_type, target=target, keywords=keywords, vibes=vibes)
    set_state("brand_data", brand_data.model_dump())

    can_interview = len(business_type.strip()) > 1 and len(target.strip()) > 1
    can_generate_candidates = len((get_state("interview_data_o") or "").strip()) > 0

    st.markdown("<br>", unsafe_allow_html=True) # 여백 추가
    b1, b2, b3 = st.columns(3)
    if b1.button("인터뷰 시작", disabled=not can_interview, use_container_width=True):
        try:
            _set_error(None)
            qpack = generate_o_interview_questions(brand_data)
            set_state("section_o_questions", qpack)
            set_state("O_answers", [])
            set_state("O_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))

    if b2.button("인터뷰 건너뛰고 후보 생성", disabled=not can_interview, use_container_width=True):
        try:
            _set_error(None)
            resp = generate_o_candidates(brand_data, "")
            set_state("section_o_candidates", resp.get("candidates", []))
        except Exception as exc:
            _set_error(str(exc))

    if b3.button("인터뷰 기반 후보 생성", disabled=not can_generate_candidates, use_container_width=True):
        try:
            _set_error(None)
            resp = generate_o_candidates(brand_data, get_state("interview_data_o") or "")
            set_state("section_o_candidates", resp.get("candidates", []))
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_o_questions") or {}
    if qpack.get("questions"):
        render_interview_card("O", qpack, "interview_data_o")

    interview_text = get_state("interview_data_o") or ""
    st.text_area("인터뷰 답변 요약", value=interview_text, height=140, disabled=True)

    candidates = get_state("section_o_candidates") or []
    if candidates:
        st.subheader("브랜드 후보 믹스앤매치")

        def _fmt(idx: int, field: str) -> str:
            c = candidates[idx]
            if field == "name":
                return f"{idx}. {c.get('brand_name', '')} ({c.get('brand_name_en', '')})"
            if field == "meaning":
                return f"{idx}. {c.get('name_meaning', '')}"
            if field == "slogan":
                return f"{idx}. {c.get('slogan', '')}"
            if field == "story":
                return f"{idx}. {c.get('story_summary', '')}"
            return f"{idx}. {c.get('seed_color', '')} · {c.get('seed_color_reason', '')}"

        options = list(range(len(candidates)))
        cc1, cc2, cc3, cc4, cc5 = st.columns(5)
        name_idx = cc1.selectbox("브랜드명", options=options, format_func=lambda x: _fmt(x, "name"), key="sel_name")
        meaning_idx = cc2.selectbox("의미", options=options, format_func=lambda x: _fmt(x, "meaning"), key="sel_meaning")
        slogan_idx = cc3.selectbox("슬로건", options=options, format_func=lambda x: _fmt(x, "slogan"), key="sel_slogan")
        story_idx = cc4.selectbox("스토리", options=options, format_func=lambda x: _fmt(x, "story"), key="sel_story")
        color_idx = cc5.selectbox("컬러", options=options, format_func=lambda x: _fmt(x, "color"), key="sel_color")

        if st.button("조합 확정", use_container_width=True):
            try:
                brand_info = apply_candidate_mix(
                    candidates,
                    {
                        "name": int(name_idx),
                        "meaning": int(meaning_idx),
                        "slogan": int(slogan_idx),
                        "story": int(story_idx),
                        "color": int(color_idx),
                    },
                )
                set_state("brand_info", brand_info.model_dump())
                st.success("브랜드 조합이 확정되었습니다.")
            except Exception as exc:
                _set_error(str(exc))

    brand_info_raw = get_state("brand_info")
    if brand_info_raw:
        st.subheader("현재 확정된 브랜드")
        st.json(brand_info_raw)
        _render_regen_panel(
            section="O",
            target_keys=["brand_name", "name_meaning", "slogan", "story_summary"],
            regenerate_fn=lambda b, c, t: regenerate_o_field(brand_data, c, t),
            context_data=brand_info_raw,
            brand_info=BrandInfo(**brand_info_raw),
            apply_target_data_key=None,
        )

    if st.button("다음 단계: Section A", disabled=brand_info_raw is None, use_container_width=True):
        set_state("current_step", 1)
        st.rerun()


# -----------------------------
# Section A/B/C/DE
# -----------------------------
def render_step_a() -> None:
    st.header("Section A - 철학, 스토리, 포지셔닝")
    _render_error()
    brand_info = _load_brand_info()
    if not brand_info:
        return

    c1, c2 = st.columns(2)
    if c1.button("인터뷰 시작", use_container_width=True):
        try:
            _set_error(None)
            set_state("section_a_questions", generate_a_interview_questions(brand_info))
            set_state("A_answers", [])
            set_state("A_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            res = generate_section_a(brand_info, get_state("interview_data_a") or "")
            set_state("data_a", res.get("data_a") or {})
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_a_questions") or {}
    if qpack.get("questions"):
        render_interview_card("A", qpack, "interview_data_a")

    if get_state("data_a"):
        st.subheader("생성 결과 미리보기")
        
        try:
            html_content = generate_a_only_html(brand_info.model_dump(), get_state("data_a"))
            
            components.html(html_content, height=800, scrolling=True)
            
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(get_state("data_a"))


def render_step_b() -> None:
    st.header("Section B - 타겟 페르소나, 여정")
    _render_error()
    brand_info = _load_brand_info()
    if not brand_info:
        return

    c1, c2 = st.columns(2)
    if c1.button("인터뷰 시작", use_container_width=True):
        try:
            _set_error(None)
            set_state("section_b_questions", generate_b_interview_questions(brand_info))
            set_state("B_answers", [])
            set_state("B_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            res = generate_section_b(brand_info, get_state("interview_data_a") or "", get_state("interview_data_b") or "")
            set_state("data_b", res.get("data_b") or {})
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_b_questions") or {}
    if qpack.get("questions"):
        render_interview_card("B", qpack, "interview_data_b")

    if get_state("data_b"):
        st.subheader("생성 결과")
        st.json(get_state("data_b"))
        _render_regen_panel(
            section="B",
            target_keys=["target_audience", "key_characteristics", "primary_need", "pain_points", "awareness", "consideration", "decision", "retention"],
            regenerate_fn=regenerate_b_field,
            context_data=get_state("data_b") or {},
            brand_info=brand_info,
            apply_target_data_key="data_b",
        )

    n1, n2 = st.columns(2)
    if n1.button("이전: A", use_container_width=True):
        set_state("current_step", 1)
        st.rerun()
    if n2.button("다음: C", disabled=get_state("data_b") is None, use_container_width=True):
        set_state("current_step", 3)
        st.rerun()


def render_step_c() -> None:
    st.header("Section C - 비주얼 아이덴티티")
    _render_error()
    brand_info = _load_brand_info()
    if not brand_info:
        return

    c1, c2 = st.columns(2)
    if c1.button("인터뷰 시작", use_container_width=True):
        try:
            _set_error(None)
            set_state("section_c_questions", generate_c_interview_questions(brand_info))
            set_state("C_answers", [])
            set_state("C_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            res = generate_section_c(
                brand_info,
                get_state("interview_data_a") or "",
                get_state("interview_data_b") or "",
                get_state("interview_data_c") or "",
            )
            set_state("data_c", res.get("data_c") or {})
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_c_questions") or {}
    if qpack.get("questions"):
        render_interview_card("C", qpack, "interview_data_c")

    if get_state("data_c"):
        st.subheader("생성 결과")
        st.json(get_state("data_c"))
        _render_regen_panel(
            section="C",
            target_keys=["primary_color", "secondary_color", "accent_color", "primary_font", "secondary_font", "photography_style", "illustration_style", "graphic_elements"],
            regenerate_fn=regenerate_c_field,
            context_data=get_state("data_c") or {},
            brand_info=brand_info,
            apply_target_data_key="data_c",
        )

    n1, n2 = st.columns(2)
    if n1.button("이전: B", use_container_width=True):
        set_state("current_step", 2)
        st.rerun()
    if n2.button("다음: DE", disabled=get_state("data_c") is None, use_container_width=True):
        set_state("current_step", 4)
        st.rerun()


def render_step_de() -> None:
    st.header("Section DE - 로고/캐릭터")
    _render_error()
    brand_info = _load_brand_info()
    if not brand_info:
        return

    data_c = get_state("data_c")
    if not data_c:
        st.warning("Section C 결과를 먼저 생성해 주세요.")
        return

    c1, c2 = st.columns(2)
    if c1.button("인터뷰 시작", use_container_width=True):
        try:
            _set_error(None)
            set_state("section_de_questions", generate_de_interview_questions(brand_info, get_state("interview_data_c") or ""))
            set_state("DE_answers", [])
            set_state("DE_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))

    if c2.button("전체 생성 시작", use_container_width=True):
        try:
            _set_error(None)
            res = generate_section_de(
                brand_info,
                data_c,
                get_state("interview_data_a") or "",
                get_state("interview_data_b") or "",
                get_state("interview_data_c") or "",
                get_state("interview_data_de") or "",
            )
            set_state("data_de", res.get("data_de") or {})
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_de_questions") or {}
    if qpack.get("questions"):
        render_interview_card("DE", qpack, "interview_data_de")

    r1, r2 = st.columns(2)
    if r1.button("로고만 재생성", use_container_width=True):
        try:
            _set_error(None)
            res = generate_logo_only(
                brand_info,
                data_c,
                get_state("interview_data_a") or "",
                get_state("interview_data_b") or "",
                get_state("interview_data_c") or "",
                get_state("interview_data_de") or "",
            )
            merged = dict(get_state("data_de") or {})
            merged.update(res.get("data_de") or {})
            set_state("data_de", merged)
        except Exception as exc:
            _set_error(str(exc))

    if r2.button("캐릭터만 재생성", use_container_width=True):
        try:
            _set_error(None)
            res = generate_character_only(
                brand_info,
                data_c,
                get_state("interview_data_a") or "",
                get_state("interview_data_b") or "",
                get_state("interview_data_c") or "",
                get_state("interview_data_de") or "",
            )
            merged = dict(get_state("data_de") or {})
            merged.update(res.get("data_de") or {})
            set_state("data_de", merged)
        except Exception as exc:
            _set_error(str(exc))

    data_de = get_state("data_de")
    if data_de:
        st.subheader("생성 결과")
        st.json(data_de)

        logo_path = data_de.get("logo_path")
        char_path = data_de.get("char_path")
        image_cols = st.columns(2)
        if logo_path and Path(logo_path).exists():
            image_cols[0].image(logo_path, caption="생성된 로고", use_container_width=True)
        if char_path and Path(char_path).exists():
            image_cols[1].image(char_path, caption="생성된 캐릭터", use_container_width=True)

        _render_regen_panel(
            section="DE",
            target_keys=["logo_identity", "character_guide"],
            regenerate_fn=regenerate_de_field,
            context_data=data_de,
            brand_info=brand_info,
            apply_target_data_key="data_de",
        )

    n1, n2 = st.columns(2)
    if n1.button("이전: C", use_container_width=True):
        set_state("current_step", 3)
        st.rerun()
    if n2.button("다음: Preview", disabled=data_de is None, use_container_width=True):
        set_state("current_step", 5)
        st.rerun()


# -----------------------------
# Preview
# -----------------------------
def render_step_preview() -> None:
    st.header("Preview - PDF 미리보기와 다운로드")
    _render_error()

    brand_info = get_state("brand_info")
    data_a = get_state("data_a")
    data_b = get_state("data_b")
    data_c = get_state("data_c")
    data_de = get_state("data_de")

    if not brand_info:
        st.info("브랜드 정보가 없습니다. Section O를 먼저 완료해 주세요.")
        return

    is_ready = all([
        isinstance(data_a, dict) and len(data_a) > 0,
        isinstance(data_b, dict) and len(data_b) > 0,
        isinstance(data_c, dict) and len(data_c) > 0,
        isinstance(data_de, dict) and len(data_de) > 0,
    ])

    left, right = st.columns([2, 1])
    with left:
        st.subheader("확정 브랜드")
        st.write(f"브랜드명: {brand_info.get('brand_name', '-')}")
        st.write(f"스토리: {brand_info.get('story_summary', '-')}")

        st.subheader("내보내기 체크리스트")
        if is_ready:
            st.success("Section A/B/C/DE 데이터 준비 완료")
        else:
            st.warning("일부 섹션 데이터가 누락되어 있습니다.")

    with right:
        st.subheader("데이터 요약")
        st.json({
            "A": bool(data_a),
            "B": bool(data_b),
            "C": bool(data_c),
            "DE": bool(data_de),
        })

    if st.button("PDF 생성", disabled=not is_ready, use_container_width=True):
        try:
            _set_error(None)
            pdf_bytes = generate_pdf_bytes(brand_info, data_a, data_b, data_c, data_de)
            set_state("pdf_bytes", pdf_bytes)
            st.success("PDF 생성 완료")
        except Exception as exc:
            _set_error(str(exc))

    pdf_bytes = get_state("pdf_bytes")
    if pdf_bytes:
        filename = build_download_filename(brand_info.get("brand_name", "brand"))
        st.download_button(
            label="PDF 다운로드",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
        )

    if st.button("이전: DE", use_container_width=True):
        set_state("current_step", 4)
        st.rerun()


def run_app() -> None:
    st.set_page_config(page_title="NameTag Streamlit", layout="wide")
    initialize_session_state()

    render_sidebar_navigation()
    _render_progress_header()
    st.divider()

    step = int(get_state("current_step") or 0)
    if step == 0:
        render_step_o()
    elif step == 1:
        render_step_a()
    elif step == 2:
        render_step_b()
    elif step == 3:
        render_step_c()
    elif step == 4:
        render_step_de()
    else:
        render_step_preview()


if __name__ == "__main__":
    run_app()
