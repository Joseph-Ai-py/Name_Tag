import streamlit as st


def render_result() -> None:
    result = st.session_state.result
    brands = result["brands"]
    typography = result["typography"]
    character = result["character"]

    st.subheader("브랜드 네임 - 3가지 제안")
    brand_names = [b["name"] for b in brands]
    selected = st.radio(
        "브랜드를 선택하세요",
        options=range(3),
        format_func=lambda i: brand_names[i],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.selected_brand = selected
    brand = brands[selected]

    with st.container(border=True):
        st.markdown(f"### {brand['name']}")
        st.caption(brand["meaning"])
        st.markdown(brand["story"])
        st.markdown(f"*\"{brand['slogan']}\"*")

    st.subheader("추천 서체")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.caption("한글")
            st.markdown(f"**{typography['korean']}**")
    with col2:
        with st.container(border=True):
            st.caption("English")
            st.markdown(f"**{typography['english']}**")
    st.caption(typography["reason"])

    st.subheader("브랜드 캐릭터 컨셉")
    with st.container(border=True):
        st.markdown(f"### {character['name']}")
        st.caption(character["concept"])
        st.markdown(f"**성격** {character['personality']}")
        st.markdown(character["visual"])

    if st.button("다시 시작하기", use_container_width=True):
        for key in [
            "step",
            "business_type",
            "keywords",
            "selected_vibes",
            "target",
            "result",
            "selected_brand",
            "error",
        ]:
            del st.session_state[key]
        st.rerun()
