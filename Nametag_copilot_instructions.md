# 네임텍(NameTag) 패키지 A — Streamlit MVP 코파일럿 지침

## 프로젝트 개요

**네임텍(NameTag)** 은 초기 스타트업 및 1인 기업을 위한 마이크로 브랜딩 구독 서비스입니다.
이 프로젝트는 **패키지 A** — AI 기반 브랜드 정체성 설계 도구 — 의 Streamlit MVP입니다.

### 패키지 A 제공 항목
- 브랜드 네이밍 (3가지 후보 제안)
- 스토리텔링 + 슬로건
- 서체 추천 (한글 / 영문)
- 브랜드 캐릭터 컨셉

---

## 기술 스택

```
Python         3.11+
streamlit      1.35+
anthropic      0.28+
python-dotenv  1.0+
```

### 설치 명령어
```bash
pip install streamlit anthropic python-dotenv
```

### 환경 변수 (.env)
```
ANTHROPIC_API_KEY=your_api_key_here
```

---

## 프로젝트 파일 구조

```
nametag-package-a/
├── .env
├── .gitignore
├── requirements.txt
├── app.py                  # 메인 Streamlit 진입점
├── pages/                  # 멀티페이지 (선택)
│   └── result.py
├── components/
│   ├── step_input.py       # Step 1: 업종 입력 컴포넌트
│   ├── step_vibe.py        # Step 2: 감성 선택 컴포넌트
│   ├── step_target.py      # Step 3: 타겟 고객 컴포넌트
│   └── result_view.py      # 결과 렌더링 컴포넌트
├── services/
│   └── brand_generator.py  # Anthropic API 호출 로직
└── utils/
    └── parser.py           # JSON 파싱 유틸리티
```

---

## 핵심 구현 패턴

### 1. 세션 상태 관리 (st.session_state)

Streamlit은 리렌더링마다 상태를 초기화하므로 반드시 `st.session_state`로 상태를 관리합니다.

```python
# app.py 상단에서 초기화
def init_session():
    defaults = {
        "step": 1,                  # 현재 단계 (1~5)
        "business_type": "",        # 업종/서비스 설명
        "keywords": "",             # 핵심 키워드
        "selected_vibes": [],       # 선택한 감성 태그 (최대 4개)
        "target": "",               # 타겟 고객 설명
        "result": None,             # API 응답 결과 dict
        "selected_brand": 0,        # 선택한 브랜드 인덱스 (0~2)
        "error": None,              # 에러 메시지
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
```

### 2. 스텝 진행 흐름

```
Step 1 (업종 입력) → Step 2 (감성 선택) → Step 3 (타겟 고객)
→ Step 4 (AI 생성 중) → Step 5 (결과 표시)
```

각 단계는 `st.session_state.step` 값에 따라 조건부 렌더링합니다.

```python
# app.py 메인 렌더링 패턴
if st.session_state.step == 1:
    render_step1()
elif st.session_state.step == 2:
    render_step2()
elif st.session_state.step == 3:
    render_step3()
elif st.session_state.step == 4:
    run_generation()   # API 호출 후 자동으로 step 5로 이동
elif st.session_state.step == 5:
    render_result()
```

### 3. 단계별 유효성 검사

```python
def can_proceed(step: int) -> bool:
    if step == 1:
        return len(st.session_state.business_type.strip()) > 2
    if step == 2:
        return len(st.session_state.selected_vibes) >= 1
    if step == 3:
        return len(st.session_state.target.strip()) > 2
    return False
```

---

## Anthropic API 연동 (services/brand_generator.py)

```python
import anthropic
import json
import re
from typing import Optional

client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 자동 인식

SYSTEM_PROMPT = """당신은 전문 브랜드 디렉터입니다.
사용자의 정보를 바탕으로 초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다.
반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."""

def build_user_prompt(business_type: str, vibes: list, target: str, keywords: str) -> str:
    return f"""업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

아래 JSON 형식으로만 응답하세요:

{{
  "brands": [
    {{
      "name": "브랜드명",
      "meaning": "이름의 의미와 어원 1-2문장",
      "story": "고객 감성을 자극하는 스토리 2-3문장",
      "slogan": "핵심 슬로건 10단어 이내"
    }},
    {{ "name": "두번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }},
    {{ "name": "세번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }}
  ],
  "typography": {{
    "korean": "추천 한글 폰트명 (나눔명조, 프리텐다드, 고도체 등)",
    "english": "추천 영문 폰트명 (Playfair Display, DM Sans 등)",
    "reason": "선택 이유 2문장"
  }},
  "character": {{
    "name": "캐릭터 이름",
    "concept": "컨셉 한 줄",
    "personality": "성격 특징 3가지, 쉼표로 구분",
    "visual": "외형 묘사 2-3문장"
  }}
}}"""


def extract_json(text: str) -> Optional[dict]:
    """다양한 형태로 반환되는 JSON을 안전하게 파싱"""
    # 1. 코드블록 안의 JSON 추출
    match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    # 2. 텍스트에서 { ... } 추출
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    # 3. 전체 파싱 시도
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def generate_brand_identity(
    business_type: str,
    vibes: list[str],
    target: str,
    keywords: str = ""
) -> dict:
    """
    브랜드 정체성 생성 메인 함수.
    성공 시 파싱된 dict 반환, 실패 시 예외 발생.
    """
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_user_prompt(business_type, vibes, target, keywords)
            }
        ]
    )

    raw_text = message.content[0].text
    result = extract_json(raw_text)

    if result is None:
        raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_text[:500]}")

    required_keys = {"brands", "typography", "character"}
    if not required_keys.issubset(result.keys()):
        raise ValueError(f"응답에 필수 키가 없습니다: {required_keys - result.keys()}")

    return result
```

---

## UI 컴포넌트 구현 가이드

### 진행 상태 표시 (Progress Bar)

```python
def render_progress(current_step: int):
    step_labels = ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "결과"]
    cols = st.columns(5)
    for i, (col, label) in enumerate(zip(cols, step_labels), start=1):
        with col:
            if i < current_step:
                st.markdown(f"✓ ~~{label}~~")
            elif i == current_step:
                st.markdown(f"**{label}**")
            else:
                st.markdown(f"<span style='color:gray'>{label}</span>", unsafe_allow_html=True)
```

### Step 1 — 업종 입력

```python
def render_step1():
    st.subheader("어떤 업종 · 서비스인가요?")
    st.caption("구체적일수록 더 정확한 브랜드를 만들 수 있어요")

    st.session_state.business_type = st.text_input(
        label="업종/서비스",
        value=st.session_state.business_type,
        placeholder="예: 20대를 위한 감성 소품 온라인 셀렉샵",
        label_visibility="collapsed"
    )

    st.session_state.keywords = st.text_input(
        label="핵심 키워드 (선택)",
        value=st.session_state.keywords,
        placeholder="예: 따뜻함, 일상, 발견",
        label_visibility="collapsed",
        help="브랜드에 담고 싶은 키워드를 쉼표로 구분해 입력하세요"
    )

    if st.button("다음 →", disabled=not can_proceed(1), use_container_width=True):
        st.session_state.step = 2
        st.rerun()
```

### Step 2 — 감성 태그 선택

```python
VIBE_OPTIONS = [
    "따뜻한", "차가운", "모던한", "클래식한", "자연친화적",
    "럭셔리한", "미니멀한", "활기찬", "유머러스한", "진지한",
    "감성적인", "신뢰감있는", "트렌디한", "레트로한"
]

def render_step2():
    st.subheader("브랜드 감성을 선택해주세요")
    st.caption("최대 4개까지 선택 가능합니다")

    # 3열 그리드로 체크박스 나열
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
        if st.button("← 이전", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("다음 →", disabled=not can_proceed(2), use_container_width=True):
            st.session_state.step = 3
            st.rerun()
```

### Step 3 — 타겟 고객 입력

```python
def render_step3():
    st.subheader("주요 타겟 고객은 누구인가요?")
    st.caption("나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요")

    if st.session_state.error:
        st.error(st.session_state.error)

    st.session_state.target = st.text_area(
        label="타겟 고객",
        value=st.session_state.target,
        placeholder="예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들",
        height=120,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", use_container_width=True):
            st.session_state.step = 2
            st.session_state.error = None
            st.rerun()
    with col2:
        if st.button("✦ 브랜드 생성", disabled=not can_proceed(3), use_container_width=True, type="primary"):
            st.session_state.step = 4
            st.rerun()
```

### Step 4 — AI 생성 (자동 실행)

```python
def run_generation():
    with st.spinner("브랜드 정체성을 설계하고 있어요..."):
        progress = st.progress(0, text="업종 · 키워드 분석 중")
        import time

        progress.progress(25, text="브랜드 네임 도출 중")
        time.sleep(0.5)
        progress.progress(50, text="스토리텔링 작성 중")

        try:
            result = generate_brand_identity(
                business_type=st.session_state.business_type,
                vibes=st.session_state.selected_vibes,
                target=st.session_state.target,
                keywords=st.session_state.keywords
            )
            progress.progress(100, text="완료!")
            st.session_state.result = result
            st.session_state.error = None
            st.session_state.step = 5

        except Exception as e:
            st.session_state.error = f"생성 중 오류가 발생했습니다: {str(e)}"
            st.session_state.step = 3

        st.rerun()
```

### Step 5 — 결과 표시

```python
def render_result():
    result = st.session_state.result
    brands = result["brands"]
    typography = result["typography"]
    character = result["character"]

    # 브랜드 네임 선택
    st.subheader("브랜드 네임 — 3가지 제안")
    brand_names = [b["name"] for b in brands]
    selected = st.radio(
        "브랜드를 선택하세요",
        options=range(3),
        format_func=lambda i: brand_names[i],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.selected_brand = selected
    brand = brands[selected]

    # 선택한 브랜드 상세
    with st.container(border=True):
        st.markdown(f"### {brand['name']}")
        st.caption(brand["meaning"])
        st.markdown(brand["story"])
        st.markdown(f"*\"{brand['slogan']}\"*")

    # 서체 추천
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

    # 캐릭터 컨셉
    st.subheader("브랜드 캐릭터 컨셉")
    with st.container(border=True):
        st.markdown(f"### {character['name']}")
        st.caption(character["concept"])
        st.markdown(f"**성격** {character['personality']}")
        st.markdown(character["visual"])

    # 다시 시작
    if st.button("↺ 다시 시작하기", use_container_width=True):
        for key in ["step","business_type","keywords","selected_vibes","target","result","selected_brand","error"]:
            del st.session_state[key]
        st.rerun()
```

---

## 전체 app.py 조립 예시

```python
import streamlit as st
from dotenv import load_dotenv
from services.brand_generator import generate_brand_identity

load_dotenv()

st.set_page_config(
    page_title="네임텍 패키지 A",
    page_icon="🏷️",
    layout="centered"
)

init_session()

# 헤더
st.markdown("### 🏷️ NAMETAG · 패키지 A")
st.title("나만의 브랜드 정체성 만들기")
st.caption("브랜드 네이밍 · 스토리텔링 · 서체 · 캐릭터를 AI가 함께 설계합니다")
st.divider()

render_progress(st.session_state.step)
st.divider()

if st.session_state.step == 1:
    render_step1()
elif st.session_state.step == 2:
    render_step2()
elif st.session_state.step == 3:
    render_step3()
elif st.session_state.step == 4:
    run_generation()
elif st.session_state.step == 5:
    render_result()
```

---

## 코드 작성 규칙 (Copilot 지침)

### 반드시 지켜야 하는 패턴
- 모든 UI 상태는 `st.session_state`로 관리한다
- 단계 이동 후에는 항상 `st.rerun()`을 호출한다
- API 호출은 `services/brand_generator.py`에만 위치시킨다
- 에러는 `st.session_state.error`에 저장하고 Step 3에서 표시한다
- `st.button()`의 `disabled` 파라미터로 유효성 검사를 UI에 반영한다

### 피해야 하는 패턴
- `st.session_state` 없이 파이썬 변수로 상태 관리 (리렌더링 시 초기화됨)
- 전역 변수에 사용자 입력 저장
- API 호출 결과를 캐싱 없이 반복 호출 (`@st.cache_data` 또는 session_state 활용)
- `st.experimental_rerun()` 사용 (deprecated → `st.rerun()` 사용)

### 성능 최적화
```python
# API 결과 캐싱 (같은 입력 재호출 방지)
@st.cache_data(show_spinner=False)
def cached_generate(business_type, vibes_tuple, target, keywords):
    return generate_brand_identity(business_type, list(vibes_tuple), target, keywords)

# 호출 시
result = cached_generate(
    st.session_state.business_type,
    tuple(st.session_state.selected_vibes),   # 리스트는 hashable하지 않으므로 tuple로 변환
    st.session_state.target,
    st.session_state.keywords
)
```

---

## 실행 방법

```bash
# 개발 서버 실행
streamlit run app.py

# 포트 지정
streamlit run app.py --server.port 8501

# 자동 새로고침 비활성화 (안정성)
streamlit run app.py --server.runOnSave false
```

---

## 확장 고려사항 (패키지 B/C 연계)

- **패키지 B** 진입점: 결과 화면에 "목업 제작하기 →" 버튼 추가
- **저장 기능**: `st.download_button`으로 결과를 JSON/PDF로 다운로드
- **히스토리**: `st.session_state`에 생성 이력 리스트 유지
- **다국어**: `st.selectbox`로 언어 선택 후 프롬프트 분기