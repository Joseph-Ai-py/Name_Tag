import time
import uuid
import re

import streamlit as st
from dotenv import load_dotenv

from components.result_view import render_result
from components.step_input import render_step1
from components.step_target import render_step3
from components.step_vibe import render_step2
from services.brand_generator import (
    generate_brand_identity,
    generate_logo_variables,
    generate_logo_image,
)
from utils.logger import get_logger, get_tracker

load_dotenv()

# Initialize logger
logger = get_logger("NameTag.App")

# 한글 색상명을 HEX 코드로 매핑
COLOR_NAME_MAP = {
    "흰색": "#FFFFFF",
    "검은색": "#000000",
    "빨강": "#FF0000",
    "초록": "#00AA00",
    "파랑": "#0000FF",
    "노랑": "#FFFF00",
    "주황": "#FFA500",
    "보라": "#800080",
    "핑크": "#FFC0CB",
    "회색": "#808080",
    "회색": "#A9A9A9",
    "베이지": "#F5F5DC",
    "올리브": "#808000",
    "검정": "#000000",
    "무색": "#FFFFFF",
    "투명": "#FFFFFF",
}

def is_valid_hex_color(color: str) -> bool:
    """HEX 색상 코드 유효성 검사"""
    if not color:
        return False
    # HEX 코드 패턴: #RRGGBB 또는 #RGB
    return bool(re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', str(color)))

def normalize_color(color: str) -> str:
    """색상 값을 유효한 HEX 코드로 정규화"""
    if not color:
        return "#000000"
    
    color = str(color).strip()
    
    # 이미 유효한 HEX 코드면 그대로 반환
    if is_valid_hex_color(color):
        return color
    
    # 한글 색상명을 찾아 변환
    for korean_color, hex_code in COLOR_NAME_MAP.items():
        if korean_color in color:
            return hex_code
    
    # 유효하지 않으면 기본값 반환
    return "#000000"

st.set_page_config(page_title="네임텍 패키지 A", page_icon="N", layout="centered")


def init_session() -> None:
    defaults = {
        "step": 1,
        "session_id": str(uuid.uuid4()),
        "business_type": "",
        "keywords": "",
        "selected_vibes": [],
        "target": "",
        "result": None,
        "logo_variables": None,
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
def cached_generate(business_type: str, vibes_tuple: tuple[str, ...], target: str, keywords: str, session_id: str):
    return generate_brand_identity(business_type, list(vibes_tuple), target, keywords, session_id=session_id)


@st.cache_data(show_spinner=False)
def cached_generate_logo_variables(
    business_type: str, vibes_tuple: tuple[str, ...], target: str, keywords: str, session_id: str
):
    return generate_logo_variables(business_type, list(vibes_tuple), target, keywords, session_id=session_id)


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
                st.session_state.session_id,
            )
            progress.progress(100, text="완료")
            st.session_state.result = result
            st.session_state.error = None
            
            # Step 2: Generate logo variables
            progress.progress(0, text="로고 변수 생성 중...")
            logo_vars = cached_generate_logo_variables(
                st.session_state.business_type,
                tuple(st.session_state.selected_vibes),
                st.session_state.target,
                st.session_state.keywords,
                st.session_state.session_id,
            )
            st.session_state.logo_variables = logo_vars
            progress.progress(100, text="완료")
            
            logger.info(f"✅ Generation completed for session: {st.session_state.session_id}")
            st.session_state.step = 5
        except Exception as exc:
            logger.error(f"❌ Generation error: {exc}", exc_info=True)
            st.session_state.error = f"생성 중 오류가 발생했습니다: {exc}"
            st.session_state.step = 3

        st.rerun()


init_session()

st.markdown("### NAMETAG - 패키지 A")
st.title("나만의 브랜드 정체성 만들기")
st.caption("브랜드 네이밍/스토리텔링/서체/캐릭터를 AI가 함께 설계합니다")

# Session ID 표시 (디버깅용)
with st.sidebar:
    st.markdown("#### 📊 Session Info")
    st.code(st.session_state.session_id, language="text")
    
    if st.button("🔄 로그 보기"):
        st.markdown("##### 📝 로그 확인:")
        st.markdown("""
        Docker 환경에서 다음 명령으로 로그를 확인할 수 있습니다:
        ```bash
        docker compose logs -f backend
        ```
        
        또는 로그 파일 위치:
        - `logs/nametag.log` - 모든 로그
        - `logs/variables.jsonl` - 변수별 로그
        """)
    
    # 로고 디자인 편집 사이드바 (결과 화면에서만 표시)
    if st.session_state.step == 5 and st.session_state.result:
        st.divider()
        st.markdown("### 🎨 로고 디자인 편집")
        
        brands = st.session_state.result.get("brands", [])
        if brands:
            # 브랜드 선택
            selected_brand_idx = st.radio(
                "추천 브랜드 선택",
                range(len(brands)),
                format_func=lambda i: brands[i].get("name", f"브랜드 {i+1}"),
                key="brand_selector"
            )
            
            # 선택된 브랜드의 logo_design 정보 표시 및 편집
            selected_brand = brands[selected_brand_idx]
            logo_design = selected_brand.get("logo_design", [{}])[0]
            
            if logo_design:
                st.markdown(f"#### {selected_brand.get('name')}")
                
                # 편집 가능한 필드들
                edited_logo_design = {}
                
                edited_logo_design["brand_name"] = st.text_input(
                    "브랜드 이름",
                    value=logo_design.get("brand_name", ""),
                    key=f"logo_brand_name_{selected_brand_idx}"
                )
                
                edited_logo_design["brand_topic"] = st.text_input(
                    "사업 주제/업종",
                    value=logo_design.get("brand_topic", ""),
                    key=f"logo_brand_topic_{selected_brand_idx}"
                )
                
                edited_logo_design["core_value"] = st.text_input(
                    "핵심 가치",
                    value=logo_design.get("core_value", ""),
                    key=f"logo_core_value_{selected_brand_idx}"
                )
                
                edited_logo_design["target_mood"] = st.text_input(
                    "타겟 감성",
                    value=logo_design.get("target_mood", ""),
                    key=f"logo_target_mood_{selected_brand_idx}"
                )
                
                edited_logo_design["symbol_type"] = st.selectbox(
                    "심볼 스타일",
                    ["기하학적", "유기적", "미니멀", "아이콘형", "레터마크", "추상적"],
                    index=["기하학적", "유기적", "미니멀", "아이콘형", "레터마크", "추상적"].index(
                        logo_design.get("symbol_type", "기하학적")
                    ) if logo_design.get("symbol_type") in ["기하학적", "유기적", "미니멀", "아이콘형", "레터마크", "추상적"] else 0,
                    key=f"logo_symbol_type_{selected_brand_idx}"
                )
                
                edited_logo_design["font_style"] = st.text_input(
                    "서체 스타일",
                    value=logo_design.get("font_style", ""),
                    key=f"logo_font_style_{selected_brand_idx}"
                )
                
                edited_logo_design["font_reference"] = st.text_input(
                    "참고 폰트",
                    value=logo_design.get("font_reference", ""),
                    key=f"logo_font_reference_{selected_brand_idx}"
                )
                
                edited_logo_design["font_weight"] = st.selectbox(
                    "폰트 굵기",
                    ["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"],
                    index=["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"].index(
                        logo_design.get("font_weight", "Regular")
                    ) if logo_design.get("font_weight") in ["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"] else 2,
                    key=f"logo_font_weight_{selected_brand_idx}"
                )
                
                # 색상 값 정규화 (한글 색상명을 HEX 코드로 변환)
                brand_color_value = normalize_color(logo_design.get("brand_color", "#000000"))
                edited_logo_design["brand_color"] = st.color_picker(
                    "브랜드 색상",
                    value=brand_color_value,
                    key=f"logo_brand_color_{selected_brand_idx}"
                )
                
                edited_logo_design["logo_type"] = st.selectbox(
                    "로고 구성",
                    ["심볼만", "텍스트만", "심볼+텍스트 조합", "배지형"],
                    index=["심볼만", "텍스트만", "심볼+텍스트 조합", "배지형"].index(
                        logo_design.get("logo_type", "심볼+텍스트 조합")
                    ) if logo_design.get("logo_type") in ["심볼만", "텍스트만", "심볼+텍스트 조합", "배지형"] else 2,
                    key=f"logo_logo_type_{selected_brand_idx}"
                )
                
                edited_logo_design["background"] = st.selectbox(
                    "배경 색상",
                    ["흰색", "검은색", "투명", "브랜드 색상"],
                    index=["흰색", "검은색", "투명", "브랜드 색상"].index(
                        logo_design.get("background", "흰색")
                    ) if logo_design.get("background") in ["흰색", "검은색", "투명", "브랜드 색상"] else 0,
                    key=f"logo_background_{selected_brand_idx}"
                )
                
                # 수정된 로고 디자인을 세션 상태에 저장
                if "edited_logo_designs" not in st.session_state:
                    st.session_state.edited_logo_designs = {}
                st.session_state.edited_logo_designs[selected_brand_idx] = edited_logo_design
                
                # 🎨 로고 생성 버튼
                st.divider()
                if st.button(
                    "🎨 로고 이미지 생성",
                    key=f"generate_logo_btn_{selected_brand_idx}",
                    use_container_width=True
                ):
                    with st.spinner("로고를 생성하고 있습니다..."):
                        try:
                            # 편집된 값이 있으면 사용, 없으면 원본 값 사용
                            logo_data = edited_logo_design
                            
                            image_bytes, filename = generate_logo_image(
                                brand_name=logo_data.get("brand_name", ""),
                                brand_topic=logo_data.get("brand_topic", ""),
                                core_value=logo_data.get("core_value", ""),
                                target_mood=logo_data.get("target_mood", ""),
                                symbol_type=logo_data.get("symbol_type", ""),
                                font_style=logo_data.get("font_style", ""),
                                font_reference=logo_data.get("font_reference", ""),
                                font_weight=logo_data.get("font_weight", ""),
                                brand_color=logo_data.get("brand_color", ""),
                                logo_type=logo_data.get("logo_type", ""),
                                background=logo_data.get("background", ""),
                                session_id=st.session_state.session_id,
                            )
                            
                            # 생성된 로고 저장
                            if "generated_logos" not in st.session_state:
                                st.session_state.generated_logos = {}
                            st.session_state.generated_logos[selected_brand_idx] = {
                                "image": image_bytes,
                                "filename": filename,
                            }
                            
                            st.success("✅ 로고 생성 완료!")
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ 로고 생성 실패: {str(e)}")
                            logger.error(f"Logo generation error: {str(e)}", exc_info=True)

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
    # Display brand identity results
    if st.session_state.result:
        result = st.session_state.result
        brands = result.get("brands", [])
        
        # 브랜드별 탭으로 표시
        if brands:
            tab_names = [brand.get("name", f"브랜드 {i+1}") for i, brand in enumerate(brands)]
            tabs = st.tabs(tab_names)
            
            for tab_idx, (tab, brand) in enumerate(zip(tabs, brands)):
                with tab:
                    col1, col2 = st.columns([2, 3])
                    
                    # 좌측: 기본 정보
                    with col1:
                        st.markdown(f"### {brand.get('name')}")
                        st.markdown(f"**의미**: {brand.get('meaning')}")
                        st.markdown(f"**스토리**: {brand.get('story')}")
                        st.markdown(f"**슬로건**: {brand.get('slogan')}")
                    
                    # 우측: 디자인 정보
                    with col2:
                        st.markdown("#### 🔤 타이포그래피")
                        typography = brand.get("typography", [{}])[0]
                        st.write(f"**한글**: {typography.get('korean')}")
                        st.write(f"**영문**: {typography.get('english')}")
                        st.caption(typography.get('reason'))
                        
                        st.markdown("#### 🌞 캠릭터")
                        character = brand.get("character", [{}])[0]
                        st.write(f"**이름**: {character.get('name')}")
                        st.write(f"**컨셉**: {character.get('concept')}")
                        st.write(f"**성격**: {character.get('personality')}")
                        st.caption(character.get('visual'))
                    
                    st.divider()
                    
                    # 로고 디자인 정보
                    st.markdown("#### 🎨 로고 디자인 (권장)")
                    logo_design = brand.get("logo_design", [{}])[0]
                    
                    if logo_design:
                        # 실시간으로 수정된 값을 표시
                        edited_values = st.session_state.edited_logo_designs.get(tab_idx, {}) if hasattr(st.session_state, 'edited_logo_designs') else {}
                        
                        cols = st.columns(2)
                        with cols[0]:
                            st.metric("🏷️ 브랜드 이름", edited_values.get("brand_name", logo_design.get("brand_name", "-")))
                            st.metric("🏢 사업 주제", edited_values.get("brand_topic", logo_design.get("brand_topic", "-")))
                            st.metric("💎 핵심 가치", edited_values.get("core_value", logo_design.get("core_value", "-")))
                            st.metric("😊 타겟 감성", edited_values.get("target_mood", logo_design.get("target_mood", "-")))
                            st.metric("✨ 심볼 스타일", edited_values.get("symbol_type", logo_design.get("symbol_type", "-")))
                        
                        with cols[1]:
                            st.metric("🔤 서체 스타일", edited_values.get("font_style", logo_design.get("font_style", "-")))
                            st.metric("📋 참고 폰트", edited_values.get("font_reference", logo_design.get("font_reference", "-")))
                            st.metric("⚖️ 폰트 굵기", edited_values.get("font_weight", logo_design.get("font_weight", "-")))
                            
                            # 색상은 정규화된 HEX 코드로 표시
                            brand_color_raw = edited_values.get("brand_color", logo_design.get("brand_color", "#000000"))
                            brand_color_hex = normalize_color(brand_color_raw)
                            st.markdown(f"**🎨 브랜드 색상**: <span style='color: {brand_color_hex}'>■</span> {brand_color_hex}", unsafe_allow_html=True)
                            
                            st.metric("🖼️ 로고 구성", edited_values.get("logo_type", logo_design.get("logo_type", "-")))
                            st.metric("🔲 배경 색상", edited_values.get("background", logo_design.get("background", "-")))
                    
                    # 생성된 로고 이미지 표시
                    st.divider()
                    if hasattr(st.session_state, 'generated_logos') and tab_idx in st.session_state.generated_logos:
                        st.markdown("#### 🎨 생성된 로고")
                        logo_image_data = st.session_state.generated_logos[tab_idx]
                        st.image(
                            logo_image_data["image"],
                            caption=f"로고: {brand.get('name')}",
                            use_container_width=True
                        )
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="📥 로고 다운로드",
                            data=logo_image_data["image"],
                            file_name=logo_image_data["filename"],
                            mime="image/png",
                            use_container_width=True
                        )

