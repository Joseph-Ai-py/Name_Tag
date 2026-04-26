import streamlit as st

VIBE_OPTIONS = [
    "따뜻한",
    "차가운",
    "모던한",
    "클래식한",
    "자연친화적",
    "럭셔리한",
    "미니멀한",
    "활기찬",
    "유머러스한",
    "진지한",
    "감성적인",
    "신뢰감있는",
    "트렌디한",
    "레트로한",
]


def render_step2(can_proceed) -> None:
    st.subheader("브랜드 감성을 선택해주세요")
    st.caption("최대 4개까지 선택 가능합니다")

    cols = st.columns(3)
    for i, vibe in enumerate(VIBE_OPTIONS):
        with cols[i % 3]:
            checked = vibe in st.session_state.selected_vibes
            if st.checkbox(vibe, value=checked, key=f"vibe_{vibe}"):
                if vibe not in st.session_state.selected_vibes:
                    if len(st.session_state.selected_vibes) < 4:
                        st.session_state.selected_vibes.append(vibe)
                    else:
                        st.warning("최대 4개까지 선택 가능합니다.")
            else:
                if vibe in st.session_state.selected_vibes:
                    st.session_state.selected_vibes.remove(vibe)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("<- 이전", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("다음 ->", disabled=not can_proceed(2), use_container_width=True):
            st.session_state.step = 3
            st.rerun()
