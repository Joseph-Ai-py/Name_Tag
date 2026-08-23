from __future__ import annotations

import streamlit.components.v1 as components
from pdf_service import build_download_filename, generate_pdf_bytes, generate_o_only_html, generate_a_only_html, generate_b_only_html, generate_c_only_html, generate_de_only_html

import json
import base64
from pathlib import Path
from typing import Any

import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

def inject_global_css():
    """앱 전체 버튼 테마 변경 및 전체 화면 로딩(Spinner) UI 커스텀"""
    st.markdown(
        """
        <style>
        /* 1. 켜져있는 버튼 (현재 스텝 등 Primary) : 기본 회색 + 눌렀을 때 더 짙은 회색 */
        button[kind="primary"] {
            background-color: #737373 !important;
            border-color: #737373 !important;
        }
        button[kind="primary"] p {
            color: #FFFFFF !important;
            font-weight: bold !important;
        }
        button[kind="primary"]:hover {
            background-color: #595959 !important;
            border-color: #595959 !important;
        }
        button[kind="primary"]:active, button[kind="primary"]:focus {
            background-color: #404040 !important;
            border-color: #404040 !important;
            box-shadow: 0 0 0 0.2rem rgba(115, 115, 115, 0.5) !important;
        }

        /* 2. 안 켜져있는 일반 버튼 (Secondary) */
        button[kind="secondary"]:hover {
            border-color: #737373 !important;
            color: #737373 !important;
        }
        button[kind="secondary"]:hover p {
            color: #737373 !important;
        }
        button[kind="secondary"]:active, button[kind="secondary"]:focus {
            border-color: #595959 !important;
            color: #595959 !important;
            box-shadow: 0 0 0 0.2rem rgba(115, 115, 115, 0.25) !important;
        }
        button[kind="secondary"]:active p, button[kind="secondary"]:focus p {
            color: #595959 !important;
        }

        /* 🌟 3. 전체 화면 로딩(Spinner) UI 커스텀 🌟 */
        /* 화면 전체를 반투명한 검은색으로 덮어버림 */
        [data-testid="stSpinner"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: rgba(0, 0, 0, 0.65) !important; /* 뒷배경 어둡게 */
            z-index: 99999 !important; /* 무조건 화면 맨 위에 오도록 */
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        /* 가운데 뜨는 로딩 박스 디자인 */
        [data-testid="stSpinner"] > div {
            background-color: var(--background-color) !important; /* 라이트/다크 테마 자동 맞춤 */
            padding: 40px 50px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important; /* 그림자 효과 */
            border: 1px solid var(--secondary-background-color) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 15px !important;
        }

        /* 로딩 텍스트(문구) 크기 키우기 */
        [data-testid="stSpinner"] > div > div:last-child {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            color: var(--text-color) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
    
    # --- 텍스트 대신 클릭 가능한 이동 버튼으로 변경 ---
    cols = st.columns(len(STEP_LABELS))
    for idx, col in enumerate(cols):
        # 현재 스텝이면 우리가 꾸며둔 primary(블루그레이) 적용, 아니면 일반 secondary
        button_type = "primary" if idx == current_step else "secondary"
        
        # 버튼 텍스트 예: "O (브랜드 초안)"
        btn_label = f"{STEP_LABELS[idx]}" 
        if col.button(btn_label, key=f"top_nav_{idx}", use_container_width=True, type=button_type):
            set_state("current_step", idx)
            st.rerun()


def render_sidebar_editor() -> None:
    with st.sidebar:
        st.header("📝 직접 수정하기")
        st.caption("수정 후 저장하면 메인 화면의 미리보기에 즉시 반영됩니다.")
        
        current_step = int(get_state("current_step") or 0)
        
        # ==========================================
        # [Section O] 브랜드 기본 정보 수정
        # ==========================================
        if current_step == 0:
            brand_info = get_state("brand_info")
            if brand_info:
                st.subheader("Section O 필드")
                new_name = st.text_input("브랜드명", value=brand_info.get("brand_name", ""))
                new_meaning = st.text_area("의미", value=brand_info.get("name_meaning", ""), height=100)
                new_slogan = st.text_area("슬로건", value=brand_info.get("slogan", ""), height=100)
                
                # --- 🎨 색상 조절(Color Picker) 추가 ---
                # 주의: st.color_picker는 반드시 '#RRGGBB' 형태의 HEX 코드를 요구합니다.
                raw_color = str(brand_info.get("seed_color", "#000000")).strip()
                # AI가 가끔 색상 코드가 아닌 글자를 줄 때 앱이 멈추는 것을 방지하는 안전 코드
                if not raw_color.startswith("#") or len(raw_color) != 7:
                    raw_color = "#000000"
                
                new_color = st.color_picker("브랜드 컬러 (Seed Color)", value=raw_color)
                # --------------------------------------

                if st.button("Section O 저장", use_container_width=True, type="primary"):
                    brand_info["brand_name"] = new_name
                    brand_info["name_meaning"] = new_meaning
                    brand_info["slogan"] = new_slogan
                    brand_info["seed_color"] = new_color # 🌟 변경된 색상 저장 로직 추가
                    
                    set_state("brand_info", brand_info)
                    st.success("저장 완료!")
                    st.rerun()
            else:
                st.info("아직 조합이 확정되지 않았습니다.")

        elif current_step == 1:
            data_a = get_state("data_a")
            if data_a:
                st.subheader("Section A 필드 전체 수정")
                
                target_a = data_a.get("data_a", data_a) if isinstance(data_a, dict) else data_a
                
                # 1. 철학 및 에센스
                with st.expander("1. 철학 및 에센스", expanded=False):
                    phil = target_a.get("brand_philosophy", {})
                    ess = target_a.get("brand_essence", {})
                    new_manifesto = st.text_area("Manifesto (철학 선언문)", value=phil.get("manifesto", ""), height=150)
                    new_raison = st.text_input("Raison d'être (존재 이유)", value=phil.get("raison_detre", ""))
                    new_ess_kw = st.text_input("Core Essence (핵심 키워드)", value=ess.get("keyword", ""))
                
                # 2. 미션 및 비전
                with st.expander("2. 기업 아이덴티티", expanded=False):
                    ci = target_a.get("core_identity", {})
                    new_mission = st.text_area("Mission (사명)", value=ci.get("mission", ""), height=100)
                    new_vision = st.text_area("Vision (비전)", value=ci.get("vision", ""), height=100)
                
                # 3. 브랜드 스토리
                with st.expander("3. 브랜드 스토리", expanded=False):
                    # AI 버전에 따라 키 이름이 다를 수 있으므로 방어적 호출
                    story_text = target_a.get("brand_story_full", target_a.get("brand_story", ""))
                    if isinstance(story_text, dict):
                        story_text = story_text.get("brand_story", "")
                    new_story = st.text_area("스토리 전문", value=story_text, height=250)

                # 4. 언어적 자산 (슬로건 등)
                with st.expander("4. 슬로건 & 네이밍 서사", expanded=False):
                    ne = target_a.get("naming_expansion", {})
                    se = target_a.get("slogan_expansion", {})
                    new_name_story = st.text_area("네이밍 서사", value=ne.get("name_story", ""), height=150)
                    new_main_slogan_en = st.text_input("메인 슬로건 (영문)", value=se.get("main_slogan_en", ""))

                # 5. 포지셔닝 및 약속
                with st.expander("5. 포지셔닝 & 약속", expanded=False):
                    pos = target_a.get("positioning", {})
                    bp = target_a.get("unbreakable_brand_promise", {})
                    new_pos_stmt = st.text_area("포지셔닝 선언문", value=pos.get("statement", ""), height=100)
                    new_promise_decl = st.text_input("타협 불가능한 약속", value=bp.get("declaration", ""))
                
                if st.button("Section A 전체 저장", use_container_width=True, type="primary"):
                    # 데이터 덮어쓰기
                    target_a.setdefault("brand_philosophy", {})["manifesto"] = new_manifesto
                    target_a.setdefault("brand_philosophy", {})["raison_detre"] = new_raison
                    target_a.setdefault("brand_essence", {})["keyword"] = new_ess_kw
                    
                    target_a.setdefault("core_identity", {})["mission"] = new_mission
                    target_a.setdefault("core_identity", {})["vision"] = new_vision
                    
                    target_a["brand_story_full"] = new_story
                    
                    target_a.setdefault("naming_expansion", {})["name_story"] = new_name_story
                    target_a.setdefault("slogan_expansion", {})["main_slogan_en"] = new_main_slogan_en
                    
                    target_a.setdefault("positioning", {})["statement"] = new_pos_stmt
                    target_a.setdefault("unbreakable_brand_promise", {})["declaration"] = new_promise_decl
                    
                    # 껍질 유지하며 저장
                    if isinstance(data_a, dict) and "data_a" in data_a:
                        data_a["data_a"] = target_a
                    else:
                        data_a = target_a
                        
                    set_state("data_a", data_a)
                    st.success("Section A 전체 저장 완료!")
                    st.rerun()
            else:
                st.info("Section A 데이터가 생성되지 않았습니다.")

        # ==========================================
        # [Section B] 타겟 페르소나, 여정 전체 수정
        # ==========================================
        elif current_step == 2:
            data_b = get_state("data_b")
            if data_b:
                st.subheader("Section B 필드 전체 수정")
                
                target_b = data_b.get("data_b", data_b) if isinstance(data_b, dict) else data_b
                
                # 1. 타겟 설정 근거 및 그룹 정의
                with st.expander("1. 타겟 정의 및 근거", expanded=False):
                    group = target_b.get("core_target_group", {})
                    new_reasoning = st.text_area("타겟 설정 근거", value=target_b.get("strategic_reasoning", ""), height=100)
                    new_target_def = st.text_input("타겟 정의", value=group.get("definition", ""))
                    new_demographics = st.text_input("인구통계학적 특성", value=group.get("demographics", ""))
                    new_behavior = st.text_area("소비 행동 특징", value=group.get("consumption_behavior", ""), height=100)
                
                # 2. 메인 페르소나 (Primary Persona)
                with st.expander("2. 1순위 핵심 고객 (페르소나)", expanded=False):
                    prim = target_b.get("primary_persona", {})
                    new_persona_name = st.text_input("핵심 고객 이름", value=prim.get("name", ""))
                    new_persona_desc = st.text_input("나이 및 직업", value=prim.get("age_and_job", ""))
                    new_scene = st.text_area("일상의 한 장면", value=prim.get("daily_scene", ""), height=100)
                    new_pain = st.text_area("결핍과 욕망", value=prim.get("pain_point_and_desire", ""), height=120)
                    new_deal = st.text_input("구매 포기 트리거 (Deal Breaker)", value=prim.get("deal_breaker", ""))

                if st.button("Section B 전체 저장", use_container_width=True, type="primary"):
                    # 1. 타겟 정의 및 근거 저장
                    target_b["strategic_reasoning"] = new_reasoning
                    target_b.setdefault("core_target_group", {})["definition"] = new_target_def
                    target_b.setdefault("core_target_group", {})["demographics"] = new_demographics
                    target_b.setdefault("core_target_group", {})["consumption_behavior"] = new_behavior
                    
                    # 2. 메인 페르소나 저장
                    target_b.setdefault("primary_persona", {})["name"] = new_persona_name
                    target_b.setdefault("primary_persona", {})["age_and_job"] = new_persona_desc
                    target_b.setdefault("primary_persona", {})["daily_scene"] = new_scene
                    target_b.setdefault("primary_persona", {})["pain_point_and_desire"] = new_pain
                    target_b.setdefault("primary_persona", {})["deal_breaker"] = new_deal
                    
                    # 껍질 유지하며 저장
                    if isinstance(data_b, dict) and "data_b" in data_b:
                        data_b["data_b"] = target_b
                    else:
                        data_b = target_b
                        
                    set_state("data_b", data_b)
                    st.success("Section B 전체 저장 완료!")
                    st.rerun()
            else:
                st.info("Section B 데이터가 생성되지 않았습니다.")

        # ==========================================
        # [Section C] 비주얼 아이덴티티 전체 수정
        # ==========================================
        elif current_step == 3:
            data_c = get_state("data_c")
            if data_c:
                st.subheader("Section C 필드 전체 수정")
                
                target_c = data_c.get("data_c", data_c) if isinstance(data_c, dict) else data_c
                
                # 1. 타이포그래피 (서체)
                with st.expander("1. 타이포그래피 (Typography)", expanded=False):
                    typo = target_c.get("typography", {})
                    prim_font = typo.get("primary_font", {})
                    sec_font = typo.get("secondary_font", {})
                    
                    new_prim_font = st.text_input("메인 폰트 (KR)", value=prim_font.get("font_name_kr", ""))
                    new_prim_usage = st.text_area("메인 폰트 사용 기준", value=prim_font.get("usage_and_reason", ""), height=80)
                    
                    new_sec_font = st.text_input("서브 폰트 (KR)", value=sec_font.get("font_name_kr", ""))
                    new_sec_usage = st.text_area("서브 폰트 사용 기준", value=sec_font.get("usage_and_reason", ""), height=80)
                
                # 2. 디자인 원칙 및 에셋 가이드
                with st.expander("2. 디자인 원칙 및 가이드", expanded=False):
                    prin = target_c.get("design_principles", {})
                    new_layout = st.text_area("레이아웃 방향성 (Layout & UI)", value=prin.get("layout_direction", ""), height=100)
                    new_img_proc = st.text_area("이미지 보정 규칙 (Image Processing)", value=prin.get("image_processing", ""), height=100)
                
                if st.button("Section C 전체 저장", use_container_width=True, type="primary"):
                    target_c.setdefault("typography", {}).setdefault("primary_font", {})["font_name_kr"] = new_prim_font
                    target_c.setdefault("typography", {}).setdefault("primary_font", {})["usage_and_reason"] = new_prim_usage
                    target_c.setdefault("typography", {}).setdefault("secondary_font", {})["font_name_kr"] = new_sec_font
                    target_c.setdefault("typography", {}).setdefault("secondary_font", {})["usage_and_reason"] = new_sec_usage
                    
                    target_c.setdefault("design_principles", {})["layout_direction"] = new_layout
                    target_c.setdefault("design_principles", {})["image_processing"] = new_img_proc
                    
                    if isinstance(data_c, dict) and "data_c" in data_c:
                        data_c["data_c"] = target_c
                    else:
                        data_c = target_c
                        
                    set_state("data_c", data_c)
                    st.success("Section C 전체 저장 완료!")
                    st.rerun()
            else:
                st.info("Section C 데이터가 생성되지 않았습니다.")

        # ==========================================
        # [Section DE] 로고 및 캐릭터 전체 수정
        # ==========================================
        elif current_step == 4:
            data_de = get_state("data_de")
            if data_de:
                st.subheader("Section DE 필드 전체 수정")
                
                target_data = data_de
                if 'candidates' in target_data and len(target_data['candidates']) > 0:
                    target_data = target_data['candidates'][0]
                
                logo_data = target_data.get('logo_identity', target_data)
                concept = logo_data.get('concept', target_data.get('concept', {}))
                
                guide = target_data.get('character_guide', {})
                intro = guide.get('intro', {})
                story = guide.get('story', {})
                
                # 1. 로고 아이덴티티
                with st.expander("1. 로고 아이덴티티", expanded=False):
                    new_symbol = st.text_area("심볼 모티브 (Symbol Motif)", value=concept.get("symbol_reason", ""), height=100)
                    new_color_reason = st.text_area("컬러 아이덴티티", value=concept.get("color_reason", ""), height=80)
                    new_msg = st.text_area("로고 철학 (Overall Message)", value=concept.get("overall_message", ""), height=100)
                
                # 2. 캐릭터 가이드
                with st.expander("2. 캐릭터 가이드", expanded=False):
                    new_char_name = st.text_input("캐릭터 이름", value=intro.get("name", ""))
                    new_appearance = st.text_area("외형 및 디자인 특징", value=intro.get("appearance", ""), height=100)
                    new_char_role = st.text_area("캐릭터 세계관 및 역할", value=story.get("brand_role", ""), height=100)
                    new_sym_value = st.text_input("상징 가치", value=intro.get("symbolic_value", ""))
                
                if st.button("Section DE 전체 저장", use_container_width=True, type="primary"):
                    update_target = data_de['candidates'][0] if 'candidates' in data_de and len(data_de['candidates']) > 0 else data_de
                    
                    if 'logo_identity' in update_target:
                        update_target['logo_identity'].setdefault('concept', {})['symbol_reason'] = new_symbol
                        update_target['logo_identity'].setdefault('concept', {})['color_reason'] = new_color_reason
                        update_target['logo_identity'].setdefault('concept', {})['overall_message'] = new_msg
                    else:
                        update_target.setdefault('concept', {})['symbol_reason'] = new_symbol
                        update_target.setdefault('concept', {})['color_reason'] = new_color_reason
                        update_target.setdefault('concept', {})['overall_message'] = new_msg
                        
                    update_target.setdefault('character_guide', {}).setdefault('intro', {})['name'] = new_char_name
                    update_target.setdefault('character_guide', {}).setdefault('intro', {})['appearance'] = new_appearance
                    update_target.setdefault('character_guide', {}).setdefault('intro', {})['symbolic_value'] = new_sym_value
                    update_target.setdefault('character_guide', {}).setdefault('story', {})['brand_role'] = new_char_role
                    
                    set_state("data_de", data_de)
                    st.success("Section DE 전체 저장 완료!")
                    st.rerun()
            else:
                st.info("Section DE 데이터가 생성되지 않았습니다.")
        
        elif current_step == 5:
            st.info("미리보기 화면입니다. 수정할 내용이 있다면 상단 버튼을 통해 이전 단계로 이동해주세요.")
        
        st.divider()
        if st.button("워크플로우 전체 초기화", use_container_width=True, type="secondary"):
            reset_workflow_state()
            st.rerun()

        # ==========================================
        # 🚀 피드백 폼 고정 버튼 추가
        # ==========================================
        st.divider()
        st.markdown("### 💡 NameTag 개선 참여")
        st.caption("서비스가 마음에 드셨나요? 작은 의견이라도 큰 도움이 됩니다!")
        st.link_button(
            "📝 1분 의견 제출하기",
            url="https://docs.google.com/forms/d/e/1FAIpQLSeNkIQc2QpAsck_oYXrIg2KItSd7_oA00osOEClX-IZowRsPw/viewform?usp=preview",
            use_container_width=True,
            type="primary" # 버튼 색상을 강조하고 싶다면 추가
        )

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
                        
                        # 🚀 추가된 로딩 UI (스피너)
                        with st.spinner("AI가 인터뷰 답변을 분석하여 브랜드 초안 후보를 기획하고 있습니다... ⏳ (약 15~30초 소요)"):
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
                        st.rerun()


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
    vibe_options = ["모던", "미니멀", "따뜻함", "프리미엄",
    "자연", "테크", "클래식", "캐주얼",
    "에너지틱", "빈티지", "힐링", "아티스틱",
    "플레이풀", "다크", "스트릿", "한국·전통"]

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
    b1, b2 = st.columns(2)
    if b1.button("인터뷰 시작", disabled=not can_interview, use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI (인터뷰 질문 생성)
            with st.spinner("입력하신 키워드를 바탕으로 맞춤형 인터뷰 질문을 생성하고 있습니다... 🎙️"):
                qpack = generate_o_interview_questions(brand_data)
                
            set_state("section_o_questions", qpack)
            set_state("O_answers", [])
            set_state("O_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))

    if b2.button("인터뷰 건너뛰고 후보 생성", disabled=not can_interview, use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI (건너뛰고 바로 생성)
            with st.spinner("AI가 즉시 브랜드 초안 후보를 기획하고 있습니다... ⏳ (약 15~30초 소요)"):
                resp = generate_o_candidates(brand_data, "")
                
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
                st.rerun()
            except Exception as exc:
                _set_error(str(exc))

    brand_info_raw = get_state("brand_info")
    if brand_info_raw:
        st.subheader("현재 확정된 브랜드 미리보기")
        
        # --- HTML 뷰어로 교체된 부분 ---
        try:
            # 확정된 브랜드 정보를 넣어 HTML 생성
            html_content = generate_o_only_html(brand_info_raw)
            with st.container(height=800, border=True):
                st.html(html_content)
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(brand_info_raw)
        # -----------------------------

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
            
            # 🚀 추가된 로딩 UI
            with st.spinner("브랜드 철학과 스토리를 도출하기 위한 심층 질문을 준비하고 있습니다... 🎙️"):
                set_state("section_a_questions", generate_a_interview_questions(brand_info))
                
            set_state("A_answers", [])
            set_state("A_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI
            with st.spinner("AI가 브랜드 철학과 스토리를 기획하고 있습니다... ✍️ (약 15~30초 소요)"):
                res = generate_section_a(brand_info, get_state("interview_data_a") or "")
                
            set_state("data_a", res.get("data_a", res))
            st.rerun()
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_a_questions") or {}
    if qpack.get("questions"):
        render_interview_card("A", qpack, "interview_data_a")

    if get_state("data_a"):
        st.subheader("생성 결과 미리보기")
        
        try:
            html_content = generate_a_only_html(brand_info.model_dump(), get_state("data_a"))
            with st.container(height=800, border=True):
                st.html(html_content)
            
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(get_state("data_a"))

    n1, n2 = st.columns(2)
    if n1.button("이전: O", use_container_width=True):
        set_state("current_step", 0)
        st.rerun()
    if n2.button("다음: B", disabled=get_state("data_a") is None, use_container_width=True):
        set_state("current_step", 2)
        st.rerun()


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
            
            # 🚀 추가된 로딩 UI
            with st.spinner("타겟 고객과 여정을 구체화하기 위한 질문을 준비하고 있습니다... 🎙️"):
                set_state("section_b_questions", generate_b_interview_questions(brand_info))
                
            set_state("B_answers", [])
            set_state("B_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI
            with st.spinner("AI가 핵심 타겟 페르소나와 고객 여정을 분석하고 있습니다... 🔍 (약 15~30초 소요)"):
                res = generate_section_b(brand_info, get_state("interview_data_a") or "", get_state("interview_data_b") or "")
                
            set_state("data_b", res.get("data_b", res))
            st.rerun()
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_b_questions") or {}
    if qpack.get("questions"):
        render_interview_card("B", qpack, "interview_data_b")

    if get_state("data_b"):
        st.subheader("생성 결과 미리보기")
        try:
            html_content = generate_b_only_html(brand_info.model_dump(), get_state("data_b"))
            with st.container(height=800, border=True):
                st.html(html_content)
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(get_state("data_b"))

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
            
            # 🚀 추가된 로딩 UI
            with st.spinner("비주얼 아이덴티티 방향성을 잡기 위한 질문을 준비하고 있습니다... 🎙️"):
                set_state("section_c_questions", generate_c_interview_questions(brand_info))
                
            set_state("C_answers", [])
            set_state("C_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))
    if c2.button("생성 시작", use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI
            with st.spinner("AI가 브랜드에 어울리는 비주얼 가이드와 폰트를 도출하고 있습니다... 🎨 (약 15~30초 소요)"):
                res = generate_section_c(
                    brand_info,
                    get_state("interview_data_a") or "",
                    get_state("interview_data_b") or "",
                    get_state("interview_data_c") or "",
                )
                
            set_state("data_c", res.get("data_c", res))
            st.rerun()
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_c_questions") or {}
    if qpack.get("questions"):
        render_interview_card("C", qpack, "interview_data_c")

    if get_state("data_c"):
        st.subheader("생성 결과 미리보기")
        try:
            html_content = generate_c_only_html(brand_info.model_dump(), get_state("data_c"))
            with st.container(height=800, border=True):
                st.html(html_content)
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(get_state("data_c"))

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
    c1, c2 = st.columns(2)
    if c1.button("인터뷰 시작", use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI
            with st.spinner("로고와 캐릭터 컨셉을 도출하기 위한 질문을 준비하고 있습니다... 🎙️"):
                set_state("section_de_questions", generate_de_interview_questions(brand_info, get_state("interview_data_c") or ""))
                
            set_state("DE_answers", [])
            set_state("DE_current_idx", 0)
        except Exception as exc:
            _set_error(str(exc))

    if c2.button("전체 생성 시작", use_container_width=True):
        try:
            _set_error(None)
            
            # 🚀 추가된 로딩 UI
            with st.spinner("AI가 로고 컨셉과 캐릭터 가이드를 구체화하고 있습니다... ✨ (약 20~40초 소요)"):
                res = generate_section_de(
                    brand_info,
                    data_c,
                    get_state("interview_data_a") or "",
                    get_state("interview_data_b") or "",
                    get_state("interview_data_c") or "",
                    get_state("interview_data_de") or "",
                )
                
            set_state("data_de", res.get("data_de", res))
            st.rerun()
        except Exception as exc:
            _set_error(str(exc))

    qpack = get_state("section_de_questions") or {}
    if qpack.get("questions"):
        render_interview_card("DE", qpack, "interview_data_de")

    # r1, r2 = st.columns(2)
    # if r1.button("로고만 재생성", use_container_width=True):
    #     try:
    #         _set_error(None)
    #         res = generate_logo_only(
    #             brand_info,
    #             data_c,
    #             get_state("interview_data_a") or "",
    #             get_state("interview_data_b") or "",
    #             get_state("interview_data_c") or "",
    #             get_state("interview_data_de") or "",
    #         )
    #         merged = dict(get_state("data_de") or {})
    #         merged.update(res.get("data_de") or {})
    #         set_state("data_de", merged)
    #         st.rerun()
    #     except Exception as exc:
    #         _set_error(str(exc))

    # if r2.button("캐릭터만 재생성", use_container_width=True):
    #     try:
    #         _set_error(None)
    #         res = generate_character_only(
    #             brand_info,
    #             data_c,
    #             get_state("interview_data_a") or "",
    #             get_state("interview_data_b") or "",
    #             get_state("interview_data_c") or "",
    #             get_state("interview_data_de") or "",
    #         )
    #         merged = dict(get_state("data_de") or {})
    #         merged.update(res.get("data_de") or {})
    #         set_state("data_de", merged)
    #         st.rerun()
    #     except Exception as exc:
    #         _set_error(str(exc))

    data_de = get_state("data_de")
    if data_de:
        st.subheader("생성 결과 미리보기")
        try:
            # C의 데이터도 함께 전달하여 브랜드 색상 반영
            html_content = generate_de_only_html(brand_info.model_dump(), get_state("data_c") or {}, data_de)
            with st.container(height=800, border=True):
                st.html(html_content)
        except Exception as exc:
            st.warning(f"미리보기를 불러올 수 없어 텍스트로 표시합니다. (에러: {exc})")
            st.json(data_de)

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

    # 기존 PDF 다운로드 버튼 코드 아래에 추가
    with st.expander("📮 10초 설문 — 방금 만든 결과물이 어떠셨나요?"):
        # w1: 별점 피드백 (st.feedback은 0~4의 인덱스를 반환하므로 주의)
        w1 = st.feedback("stars")
        
        # w2: 아쉬운 점 다중 선택
        w2 = st.multiselect(
            "아쉬웠던 부분이 있다면 골라주세요.", 
            ["브랜드 정체성(질문·문구)", "로고 이미지", "캐릭터 이미지", "MVB 리포트", "PDF 파일", "생성 속도·오류", "괜찮았다"]
        )
        
        # 조건부 UI: '괜찮았다'가 없거나 아쉬운 점을 하나라도 선택했을 때만 연락처 입력칸 노출
        show_contact = len(w2) > 0 and "괜찮았다" not in w2
        w3 = ""
        if show_contact:
            w3 = st.text_input("개선 소식이나 알림을 받아보실까요? (이메일/오픈카톡 아이디)", placeholder="선택사항입니다.")

        # 제출 버튼
        if st.button("의견 제출하기", use_container_width=True):
            if w1 is None:
                st.warning("별점을 먼저 선택해 주세요!")
            else:
                # 피드백이 중복으로 들어가는 것을 방지 (세션 스테이트 활용)
                if "feedback_submitted" not in st.session_state:
                    st.session_state.feedback_submitted = True
                    
                    # 별점을 1~5점 척도로 보정 (0 -> 1점, 4 -> 5점)
                    star_score = w1 + 1
                    issues = ", ".join(w2) if w2 else "선택 안 함"
                    
                    # 저장할 데이터 프레임 구성
                    new_feedback = pd.DataFrame({
                        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        "Rating (Stars)": [star_score],
                        "Issues": [issues],
                        "Contact (Optional)": [w3]
                    })
                    
                    csv_file_path = "nametag_feedback.csv"
                    
                    # CSV 파일이 없으면 헤더 포함하여 생성, 있으면 맨 아래에 행 추가(append)
                    if not os.path.exists(csv_file_path):
                        new_feedback.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
                    else:
                        new_feedback.to_csv(csv_file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
                    
                    st.success("소중한 의견이 저장되었습니다! 다음 버전에 꼭 반영하겠습니다.")
                else:
                    st.info("이미 의견을 제출해주셨습니다. 감사합니다!")

    if st.button("이전: DE", use_container_width=True):
        set_state("current_step", 4)
        st.rerun()

def inject_global_css():
    """앱 전체 버튼에서 발생하는 Streamlit 기본 빨간색 테마를 회색으로 덮어씁니다."""
    st.markdown(
        """
        <style>
        /* 1. 켜져있는 버튼 (현재 스텝 등 Primary) : 기본 회색 + 눌렀을 때 더 짙은 회색 */
        button[kind="primary"] {
            background-color: #737373 !important;
            border-color: #737373 !important;
        }
        button[kind="primary"] p {
            color: #FFFFFF !important;
            font-weight: bold !important;
        }
        button[kind="primary"]:hover {
            background-color: #595959 !important;
            border-color: #595959 !important;
        }
        button[kind="primary"]:active, button[kind="primary"]:focus {
            background-color: #404040 !important;
            border-color: #404040 !important;
            box-shadow: 0 0 0 0.2rem rgba(115, 115, 115, 0.5) !important;
        }

        /* 2. 안 켜져있는 일반 버튼 (Secondary) : 평소엔 그대로, 마우스 올리거나 누를 때 빨간색 대신 회색 적용 */
        button[kind="secondary"]:hover {
            border-color: #737373 !important;
            color: #737373 !important;
        }
        button[kind="secondary"]:hover p {
            color: #737373 !important;
        }
        button[kind="secondary"]:active, button[kind="secondary"]:focus {
            border-color: #595959 !important;
            color: #595959 !important;
            box-shadow: 0 0 0 0.2rem rgba(115, 115, 115, 0.25) !important;
        }
        button[kind="secondary"]:active p, button[kind="secondary"]:focus p {
            color: #595959 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def run_app() -> None:
    st.set_page_config(page_title="NameTag Streamlit", layout="wide")
    initialize_session_state()

    # 🌟 1. 가장 먼저 글로벌 CSS를 주입해서 눈 아픈 빨간색을 모조리 회색으로 덮어버립니다!
    inject_global_css()

    # 🌟 2. 그 다음 사이드바와 헤더를 렌더링합니다. (이제 예쁜 회색으로 나옵니다)
    render_sidebar_editor()
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

    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**NameTag가 유용하셨나요? 1분 피드백으로 다음 버전을 함께 만들어주세요!**")
    with col2:
        st.link_button(
            "🚀 의견 제출하기",
            url="https://docs.google.com/forms/d/e/1FAIpQLSeNkIQc2QpAsck_oYXrIg2KItSd7_oA00osOEClX-IZowRsPw/viewform?usp=preview",
            use_container_width=True
        )


if __name__ == "__main__":
    run_app()
