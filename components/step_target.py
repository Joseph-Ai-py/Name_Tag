import streamlit as st


def render_step3(can_proceed) -> None:
    st.subheader("주요 타겟 고객은 누구인가요?")
    st.caption("나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요")

    if st.session_state.error:
        st.error(st.session_state.error)

    st.session_state.target = st.text_area(
        label="타겟 고객",
        value=st.session_state.target,
        placeholder="예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들",
        height=120,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("<- 이전", use_container_width=True):
            st.session_state.step = 2
            st.session_state.error = None
            st.rerun()
    with col2:
        if st.button("* 브랜드 생성", disabled=not can_proceed(3), use_container_width=True, type="primary"):
            st.session_state.step = 4
            st.rerun()
