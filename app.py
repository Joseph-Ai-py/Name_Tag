import time

import streamlit as st
from dotenv import load_dotenv

from components.result_view import render_result
from components.step_input import render_step1
from components.step_target import render_step3
from components.step_vibe import render_step2
from services.brand_generator import generate_brand_identity

load_dotenv()

st.set_page_config(page_title="네임텍 패키지 A", page_icon="N", layout="centered")


def init_session() -> None:
    defaults = {
        "step": 1,
        "business_type": "",
        "keywords": "",
        "selected_vibes": [],
        "target": "",
        "result": None,
        "selected_brand": 0,
        "error": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def can_proceed(step: int) -> bool:
    if step == 1:
        return len(st.session_state.business_type.strip()) > 2
    if step == 2:
        return len(st.session_state.selected_vibes) >= 1
    if step == 3:
        return len(st.session_state.target.strip()) > 2
    return False


def render_progress(current_step: int) -> None:
    step_labels = ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "결과"]
    cols = st.columns(5)
    for i, (col, label) in enumerate(zip(cols, step_labels), start=1):
        with col:
            if i < current_step:
                st.markdown(f"OK ~~{label}~~")
            elif i == current_step:
                st.markdown(f"**{label}**")
            else:
                st.markdown(f"<span style='color:gray'>{label}</span>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def cached_generate(business_type: str, vibes_tuple: tuple[str, ...], target: str, keywords: str):
    return generate_brand_identity(business_type, list(vibes_tuple), target, keywords)


def run_generation() -> None:
    with st.spinner("브랜드 정체성을 설계하고 있어요..."):
        progress = st.progress(0, text="업종/키워드 분석 중")
        progress.progress(25, text="브랜드 네임 도출 중")
        time.sleep(0.3)
        progress.progress(50, text="스토리텔링 작성 중")

        try:
            result = cached_generate(
                st.session_state.business_type,
                tuple(st.session_state.selected_vibes),
                st.session_state.target,
                st.session_state.keywords,
            )
            progress.progress(100, text="완료")
            st.session_state.result = result
            st.session_state.error = None
            st.session_state.step = 5
        except Exception as exc:
            st.session_state.error = f"생성 중 오류가 발생했습니다: {exc}"
            st.session_state.step = 3

        st.rerun()


init_session()

st.markdown("### NAMETAG - 패키지 A")
st.title("나만의 브랜드 정체성 만들기")
st.caption("브랜드 네이밍/스토리텔링/서체/캐릭터를 AI가 함께 설계합니다")
st.divider()

render_progress(st.session_state.step)
st.divider()

if st.session_state.step == 1:
    render_step1(can_proceed)
elif st.session_state.step == 2:
    render_step2(can_proceed)
elif st.session_state.step == 3:
    render_step3(can_proceed)
elif st.session_state.step == 4:
    run_generation()
elif st.session_state.step == 5:
    render_result()
