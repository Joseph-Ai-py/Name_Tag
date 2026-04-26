import streamlit as st


def render_step1(can_proceed) -> None:
    st.subheader("어떤 업종 · 서비스인가요?")
    st.caption("구체적일수록 더 정확한 브랜드를 만들 수 있어요")

    st.session_state.business_type = st.text_input(
        label="업종/서비스",
        value=st.session_state.business_type,
        placeholder="예: 20대를 위한 감성 소품 온라인 셀렉샵",
        label_visibility="collapsed",
    )

    st.session_state.keywords = st.text_input(
        label="핵심 키워드 (선택)",
        value=st.session_state.keywords,
        placeholder="예: 따뜻함, 일상, 발견",
        label_visibility="collapsed",
        help="브랜드에 담고 싶은 키워드를 쉼표로 구분해 입력하세요",
    )

    if st.button("다음 ->", disabled=not can_proceed(1), use_container_width=True):
        st.session_state.step = 2
        st.rerun()
