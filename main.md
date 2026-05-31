# NameTag 백엔드 — Copilot 완전 재현 명령어
# 구현 스택: FastAPI (Python) + React 프론트엔드 + REST API

> 이 문서는 기존 코드베이스(`brand_director.py`, `nametag_prompts.py`, `nametag_pdf_builder.py`)의 로직을
> **FastAPI REST API 서버 + React 프론트엔드**로 완전히 재현하기 위한 단계별 명령어입니다.
> 노트북 코드는 참고용이며, 실제 구현 타겟은 웹 서비스입니다.

---

## 0. 전체 프로젝트 구조

```
nametag/
├── backend/                         # FastAPI 서버
│   ├── main.py                      # FastAPI 앱 진입점, 라우터 등록
│   ├── routers/
│   │   ├── section_o.py             # POST /api/section-o/*
│   │   ├── section_a.py             # POST /api/section-a/*
│   │   ├── section_b.py             # POST /api/section-b/*
│   │   ├── section_c.py             # POST /api/section-c/*
│   │   ├── section_de.py            # POST /api/section-de/*
│   │   └── pdf.py                   # POST /api/pdf/generate
│   ├── services/
│   │   ├── gemini_service.py        # Gemini API 호출 공통 로직
│   │   └── image_service.py         # 이미지 생성 및 저장 로직
│   ├── prompts/
│   │   └── nametag_prompts.py       # 모든 프롬프트 함수 (기존과 동일)
│   ├── pdf/
│   │   └── nametag_pdf_builder.py   # HTML 조립 및 PDF 생성 (기존과 동일)
│   ├── assets/
│   │   ├── logos/                   # 생성된 로고 PNG
│   │   └── characters/              # 생성된 캐릭터 PNG
│   ├── requirements.txt
│   └── .env
├── frontend/                        # React 앱
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── SectionO.jsx         # 브랜드 초기 정보 입력 + MVB 선택
│   │   │   ├── SectionA.jsx         # 철학·스토리·포지셔닝 인터뷰
│   │   │   ├── SectionB.jsx         # 타겟 페르소나·고객 여정 인터뷰
│   │   │   ├── SectionC.jsx         # 비주얼 아이덴티티 인터뷰
│   │   │   ├── SectionDE.jsx        # 로고·캐릭터 인터뷰 + 이미지 생성
│   │   │   └── Preview.jsx          # PDF 미리보기 + 다운로드
│   │   ├── components/
│   │   │   ├── InterviewCard.jsx    # 4지선다 인터뷰 공통 컴포넌트
│   │   │   ├── CandidateSelector.jsx # MVB 믹스앤매치 선택 컴포넌트
│   │   │   └── LoadingSpinner.jsx
│   │   ├── api/
│   │   │   └── client.js            # axios/fetch 기반 API 호출 모음
│   │   └── store/
│   │       └── brandStore.js        # 전역 상태 (brand_info, interview_data 등)
│   └── package.json
```

---

## 1. 공통 규칙 및 핵심 설계 원칙

### AI 모델
- 텍스트 생성: `gemini-3-flash-preview`
- 이미지 생성: `gemini-3.1-flash-image-preview`
- SYSTEM_PROMPT (고정):
  ```
  당신은 10년 경력의 브랜드 디렉터입니다.
  초기 창업자에게 최소 브랜드(MVB: Minimum Viable Brand)를 제공하는 것이 목표입니다.
  반드시 JSON만 출력하고 마크다운 코드블록이나 설명 텍스트를 절대 포함하지 마세요.
  각 후보는 서로 완전히 다른 방향성과 감성을 가져야 합니다.
  ```

### API 에러 재시도 로직
- 텍스트 API: 429/500/502/503 에러 → 90초 대기 후 재시도, 최대 10회
- 이미지 API: 동일 에러 → 30초 대기, 최대 3회
- 그 외 에러: 즉시 HTTPException 반환

### JSON 파싱
```python
import re, json
def parse_ai_response(raw_text: str) -> dict:
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if not match:
        raise ValueError("AI 응답에서 JSON을 찾을 수 없습니다.")
    return json.loads(match.group())
```

### 데이터 흐름 요약
```
사용자 입력
  → POST /api/section-o/interview  → AI 인터뷰 질문 반환
  → POST /api/section-o/candidates → MVB 후보 4개 반환
  → 프론트에서 믹스앤매치 선택 → brand_info 확정
  → POST /api/section-a/interview  → AI 인터뷰 질문 반환
  → 프론트에서 답변 선택 → interview_data_A 확정
  → POST /api/section-a/generate   → data_A (철학+스토리+포지셔닝) 반환
  → (B, C, DE 동일 패턴 반복)
  → POST /api/pdf/generate          → PDF 파일 반환 (FileResponse)
```

---

## 2. FastAPI 백엔드 구현

### 2-0. `requirements.txt`
```
fastapi
uvicorn[standard]
python-dotenv
google-genai
Pillow
weasyprint
python-multipart
```

### 2-1. `backend/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import section_o, section_a, section_b, section_c, section_de, pdf

app = FastAPI(title="NameTag API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(section_o.router, prefix="/api/section-o")
app.include_router(section_a.router, prefix="/api/section-a")
app.include_router(section_b.router, prefix="/api/section-b")
app.include_router(section_c.router, prefix="/api/section-c")
app.include_router(section_de.router, prefix="/api/section-de")
app.include_router(pdf.router, prefix="/api/pdf")

# 생성된 이미지 정적 파일 서빙
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
```

### 2-2. `backend/services/gemini_service.py`
```python
import os, re, json, time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """당신은 10년 경력의 브랜드 디렉터입니다.
초기 창업자에게 최소 브랜드(MVB: Minimum Viable Brand)를 제공하는 것이 목표입니다.
반드시 JSON만 출력하고 마크다운 코드블록이나 설명 텍스트를 절대 포함하지 마세요.
각 후보는 서로 완전히 다른 방향성과 감성을 가져야 합니다."""

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_IMAGE_API_KEY = os.getenv("GEMINI_IMAGE_API_KEY")


def request_gemini_text(prompt: str, max_retries: int = 10) -> dict:
    """
    Gemini 텍스트 API를 호출하고 파싱된 dict를 반환한다.
    429/500/502/503 에러 시 90초 대기 후 재시도, 최대 max_retries회.
    그 외 에러는 즉시 예외 발생.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    retries = 0
    while retries <= max_retries:
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            raw_text = response.text or ""
            return parse_ai_response(raw_text)
        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["429", "500", "502", "503"]):
                retries += 1
                if retries <= max_retries:
                    time.sleep(90)
                    continue
                else:
                    raise RuntimeError("최대 재시도 횟수 초과")
            else:
                raise


def request_gemini_image(prompt: str, max_retries: int = 3) -> bytes | None:
    """
    Gemini 이미지 API를 호출하고 이미지 바이트를 반환한다.
    429/500/502/503 에러 시 30초 대기 후 재시도, 최대 3회.
    """
    client = genai.Client(api_key=GEMINI_IMAGE_API_KEY)
    retries = 0
    while retries <= max_retries:
        try:
            result = client.models.generate_content(
                model="gemini-3.1-flash-image-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                ),
            )
            if hasattr(result, "parts") and len(result.parts) > 0:
                part = result.parts[0]
                if hasattr(part, "inline_data") and part.inline_data:
                    return part.inline_data.data
                elif hasattr(part, "image") and part.image:
                    return part.image.image_bytes
            return None
        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["429", "500", "502", "503"]):
                retries += 1
                if retries <= max_retries:
                    time.sleep(30)
                    continue
                else:
                    return None
            else:
                return None


def parse_ai_response(raw_text: str) -> dict:
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if not match:
        raise ValueError("AI 응답에서 JSON을 찾을 수 없습니다.")
    return json.loads(match.group())
```

### 2-3. `backend/services/image_service.py`
```python
import os
from pathlib import Path
from datetime import datetime
from services.gemini_service import request_gemini_image


def generate_logo_image(brand_name: str, de_section_data: dict) -> str | None:
    """
    data_DE['logo_identity']['concept']['direction_text']를 추출해
    로고 이미지를 생성하고 assets/logos/ 에 저장한다.
    반환: 저장된 파일의 절대 경로 문자열 (실패 시 None)
    """
    concept = de_section_data.get("logo_identity", {}).get("concept", {})
    direction_text = concept.get("direction_text", "모던하고 심플한 워드마크 또는 심볼 형태")

    prompt = f"""당신은 세계적인 수준의 브랜드 아이덴티티(BI) 전문 디자이너입니다.
다음 지시사항에 따라 브랜드 로고를 완벽하게 디자인해 주세요.

[브랜드명]: {brand_name}
[디자인 핵심 방향성]: {direction_text}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 3D 효과, 그림자, 그라데이션, 광택이 전혀 없는 완벽하게 플랫(Flat)한 2D 벡터 스타일.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경. 투명도나 다른 배경 요소 절대 금지.
- 디테일: 복잡한 스케치나 스머지(번짐) 효과 없이, 선명하고 또렷한 가장자리(Crisp edges) 유지.
- 텍스트 제어: '{brand_name}' 외에 의미를 알 수 없는 이상한 AI 문자나 기호가 절대 포함되지 않도록 할 것.
- 목적: 전문 브랜딩 에이전시의 포트폴리오에 들어갈 법한 세련되고 미니멀한 마스터 로고."""

    image_data = request_gemini_image(prompt)
    if not image_data:
        return None

    logo_dir = Path("assets/logos")
    logo_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logo_{brand_name.replace(' ', '_')}_{timestamp}.png"
    file_path = logo_dir / filename
    with open(file_path, "wb") as f:
        f.write(image_data)
    return str(file_path.resolve())


def generate_character_image(brand_name: str, de_section_data: dict) -> str | None:
    """
    data_DE['character_guide']['intro']를 추출해
    캐릭터 이미지를 생성하고 assets/characters/ 에 저장한다.
    반환: 저장된 파일의 절대 경로 문자열 (실패 시 None)
    """
    char_intro = de_section_data.get("character_guide", {}).get("intro", {})
    char_name = char_intro.get("name", "마스코트")
    char_appearance = char_intro.get("appearance", "브랜드 무드에 맞는 귀여운 마스코트")

    prompt = f"""당신은 세계적인 수준의 브랜드 캐릭터(마스코트) 전문 일러스트레이터입니다.
다음 지시사항에 따라 브랜드를 대변할 매력적인 캐릭터를 디자인해 주세요.

[브랜드명]: {brand_name}
[캐릭터 이름]: {char_name}
[캐릭터 외형 묘사]: {char_appearance}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 브랜드 로고와 시각적 일관성을 갖춘 깔끔한 2D 벡터 일러스트레이션.
- 구도: 캐릭터의 전신이나 상반신이 중앙에 명확하게 배치된 프로필 샷.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경.
- 텍스트 제어: 이미지 안에 어떤 텍스트나 글자도 포함하지 말 것."""

    image_data = request_gemini_image(prompt)
    if not image_data:
        return None

    char_dir = Path("assets/characters")
    char_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"char_{brand_name.replace(' ', '_')}_{timestamp}.png"
    file_path = char_dir / filename
    with open(file_path, "wb") as f:
        f.write(image_data)
    return str(file_path.resolve())
```

### 2-4. 라우터 구현 패턴

**모든 라우터는 아래 2가지 엔드포인트 패턴을 따릅니다.**

#### 패턴 A — 인터뷰 질문 생성
```
POST /api/section-{x}/interview
Request Body: { brand_info: {...}, [이전 섹션 interview_data: "..."] }
Response:     { reasoning: "...", questions: [{question_text, options}, ...] }
```

#### 패턴 B — 콘텐츠 생성
```
POST /api/section-{x}/generate
Request Body: { brand_info: {...}, interview_data_x: "...", [이전 섹션 데이터] }
Response:     { data_x: {...} }   ← parse_ai_response() 결과 그대로
```

---

### 2-5. `backend/routers/section_o.py`
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import request_gemini_text
from prompts.nametag_prompts import get_O_interview_prompt, get_O_mvb_prompt

router = APIRouter()


class BrandData(BaseModel):
    business_type: str
    vibes: list[str]
    target: str
    keywords: str = ""


class OInterviewRequest(BaseModel):
    brand_data: BrandData


class OMvbRequest(BaseModel):
    brand_data: BrandData
    interview_data: str  # format_interview_responses() 결과 텍스트


def build_base_prompt(brand_data: BrandData, core_prompt: str, brand_name: str = "브랜드명 미정") -> str:
    """brand_data를 프롬프트 앞에 삽입하는 헬퍼 (기존 get_prompt() 역할)"""
    return f"""
[기본 입력 정보]
- 업종/서비스: {brand_data.business_type}
- 브랜드 감성: {', '.join(brand_data.vibes)}
- 타겟 고객: {brand_data.target}
- 확정된 브랜드명: {brand_name}
""" + core_prompt


@router.post("/interview")
async def get_interview_questions(req: OInterviewRequest):
    """
    브랜드 초기 정보를 받아 MVB 도출을 위한 인터뷰 질문을 반환한다.
    반환: { reasoning, questions: [{question_text, options}] }
    """
    try:
        prompt = build_base_prompt(req.brand_data, get_O_interview_prompt())
        result = request_gemini_text(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/candidates")
async def get_mvb_candidates(req: OMvbRequest):
    """
    인터뷰 결과를 받아 브랜드 후보 4개를 반환한다.
    반환: { candidates: [{id, brand_name, brand_name_en, name_meaning,
                          slogan, story_summary, seed_color, seed_color_reason}] }
    """
    try:
        prompt = build_base_prompt(req.brand_data, get_O_mvb_prompt(req.interview_data))
        result = request_gemini_text(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-6. `backend/routers/section_a.py`
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import request_gemini_text
from prompts.nametag_prompts import (
    get_A_interview_prompt,
    get_A1_philosophy_prompt,
    get_A2_story_prompt,
    get_A3_positioning_prompt,
)

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class AInterviewRequest(BaseModel):
    brand_info: BrandInfo


class AGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str  # format_interview_responses() 결과 텍스트


@router.post("/interview")
async def get_interview_questions(req: AInterviewRequest):
    """
    확정된 brand_info를 받아 실행 전략(디자인·마케팅·고객경험) 인터뷰 질문을 반환한다.
    반환: { reasoning, questions: [{question_text, options}] }
    """
    try:
        result = request_gemini_text(get_A_interview_prompt(req.brand_info.model_dump()))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_section_a(req: AGenerateRequest):
    """
    brand_info + 인터뷰 결과를 받아 A1(철학), A2(스토리), A3(포지셔닝)을
    순차적으로 생성하고 병합하여 반환한다.

    반환:
    {
      data_a: {
        brand_philosophy, brand_essence, core_identity,   ← A1
        naming_expansion, slogan_expansion, brand_story_full, ← A2
        positioning, unbreakable_brand_promise             ← A3
      }
    }
    """
    try:
        brand = req.brand_info.model_dump()
        text = req.interview_data_a

        a1 = request_gemini_text(get_A1_philosophy_prompt(brand, text))
        a2 = request_gemini_text(get_A2_story_prompt(brand, text))
        a3 = request_gemini_text(get_A3_positioning_prompt(brand, text))

        # 3개 dict 병합 (PDF builder가 단일 dict로 받기 위해)
        merged = {}
        for part in [a1, a2, a3]:
            merged.update(part)

        return {"data_a": merged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-7. `backend/routers/section_b.py`
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import request_gemini_text
from prompts.nametag_prompts import (
    get_B_interview_prompt,
    get_B1_persona_prompt,
    get_B2_journey_prompt,
)

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class BInterviewRequest(BaseModel):
    brand_info: BrandInfo


class BGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str
    interview_data_b: str


@router.post("/interview")
async def get_interview_questions(req: BInterviewRequest):
    """
    brand_info를 받아 타겟 페르소나·고객 여정 인터뷰 질문을 반환한다.
    반환: { reasoning, questions: [{question_text, options}] }
    """
    try:
        result = request_gemini_text(get_B_interview_prompt(req.brand_info.model_dump()))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_section_b(req: BGenerateRequest):
    """
    brand_info + A/B 인터뷰 결과를 받아 B1(페르소나), B2(고객여정)을 생성하여 반환한다.

    반환:
    {
      data_b: {
        strategic_reasoning, core_target_group, primary_persona,
        secondary_personas, emotional_triggers,   ← B1
        customer_journey_map                       ← B2
      }
    }
    """
    try:
        brand = req.brand_info.model_dump()
        b1 = request_gemini_text(
            get_B1_persona_prompt(brand, req.interview_data_a, req.interview_data_b)
        )
        b2 = request_gemini_text(
            get_B2_journey_prompt(brand, req.interview_data_a, req.interview_data_b)
        )
        merged = {}
        for part in [b1, b2]:
            merged.update(part)
        return {"data_b": merged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-8. `backend/routers/section_c.py`
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import request_gemini_text
from prompts.nametag_prompts import get_C0_visual_interview_prompt, get_C1_visual_identity_prompt

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class CInterviewRequest(BaseModel):
    brand_info: BrandInfo


class CGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str
    interview_data_b: str
    interview_data_c: str


@router.post("/interview")
async def get_interview_questions(req: CInterviewRequest):
    """
    brand_info를 받아 레이아웃·타이포·무드 3가지 비주얼 인터뷰 질문을 반환한다.
    주의: 이 엔드포인트의 반환 구조는 다른 섹션과 다르다.
    반환: { reasoning, questions: [{question_text, options}] }  ← question_id 없음
    """
    try:
        result = request_gemini_text(get_C0_visual_interview_prompt(req.brand_info.model_dump()))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_section_c(req: CGenerateRequest):
    """
    brand_info + A/B/C 인터뷰 결과를 받아 비주얼 아이덴티티를 생성한다.
    previous_context = interview_data_a + " + " + interview_data_b (기존 코드와 동일)

    반환:
    {
      data_c: {
        color_palette, typography, visual_mood_guide, design_principles
      }
    }
    """
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b}"
        result = request_gemini_text(
            get_C1_visual_identity_prompt(brand, previous_context, req.interview_data_c)
        )
        return {"data_c": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-9. `backend/routers/section_de.py`
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import request_gemini_text
from services.image_service import generate_logo_image, generate_character_image
from prompts.nametag_prompts import get_DE_interview_prompt, get_DE_identity_prompt

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class DEInterviewRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_c: str


class DEGenerateRequest(BaseModel):
    brand_info: BrandInfo
    data_c: dict
    interview_data_a: str
    interview_data_b: str
    interview_data_c: str
    interview_data_de: str


@router.post("/interview")
async def get_interview_questions(req: DEInterviewRequest):
    """
    brand_info + C 인터뷰 결과를 받아 로고 심볼·선 디테일·캐릭터 인터뷰 질문을 반환한다.
    반환: { reasoning, questions: [{question_text, options}] }
    """
    try:
        result = request_gemini_text(
            get_DE_interview_prompt(req.brand_info.model_dump(), req.interview_data_c)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_section_de(req: DEGenerateRequest):
    """
    모든 이전 데이터를 받아 로고·캐릭터 기획안을 생성하고 이미지를 생성한다.
    previous_context = A+B+C 인터뷰 합산 (기존 코드와 동일)

    반환:
    {
      data_de: {
        logo_identity, character_guide,
        logo_path,  ← assets/logos/... 경로 (웹 서빙용 상대경로로 변환)
        char_path   ← assets/characters/... 경로
      }
    }
    """
    try:
        brand = req.brand_info.model_dump()
        previous_context = (
            f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}"
        )

        result = request_gemini_text(
            get_DE_identity_prompt(
                brand, req.data_c, previous_context, req.interview_data_de
            )
        )

        # 이미지 생성
        logo_path = generate_logo_image(brand["brand_name"], result)
        char_path = generate_character_image(brand["brand_name"], result)

        # 경로를 웹 서빙 가능한 상대경로로 변환 (/assets/logos/xxx.png)
        def to_url_path(abs_path: str | None) -> str | None:
            if not abs_path:
                return None
            p = abs_path.replace("\\", "/")
            idx = p.find("assets/")
            return "/" + p[idx:] if idx != -1 else None

        result["logo_path"] = to_url_path(logo_path)
        result["char_path"] = to_url_path(char_path)

        return {"data_de": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-10. `backend/routers/pdf.py`
```python
import os
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from weasyprint import HTML
from pdf.nametag_pdf_builder import assemble_html

router = APIRouter()


class PdfRequest(BaseModel):
    brand_info: dict
    data_a: dict
    data_b: dict
    data_c: dict
    data_de: dict


@router.post("/generate")
async def generate_pdf(req: PdfRequest):
    """
    모든 섹션 데이터를 받아 PDF를 생성하고 파일로 반환한다.
    반환: PDF 파일 (application/pdf)
    """
    try:
        html_content = assemble_html(
            req.brand_info,
            req.data_a,
            req.data_b,
            req.data_c,
            req.data_de,
        )

        # 임시 파일에 PDF 저장 후 FileResponse로 반환
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        HTML(string=html_content).write_pdf(tmp.name)
        tmp.close()

        brand_name = req.brand_info.get("brand_name", "brand")
        return FileResponse(
            path=tmp.name,
            media_type="application/pdf",
            filename=f"nametag_{brand_name}_guideline.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2-11. `backend/prompts/nametag_prompts.py`
```
기존 nametag_prompts.py 파일을 그대로 복사한다.
변경 없음. 함수 시그니처, 프롬프트 텍스트, JSON 스키마 모두 동일.
```

### 2-12. `backend/pdf/nametag_pdf_builder.py`
```
기존 nametag_pdf_builder.py 파일을 그대로 복사한다.
단, build_d_logo_identity()와 build_e_character_guide()의 이미지 렌더링 부분만 수정:

기존 (로컬 절대경로):
  src="file:///{safe_path}"

수정 (웹 서버 상대경로):
  src="http://localhost:8000{logo_image_path}"
  (logo_image_path = "/assets/logos/xxx.png" 형태로 전달됨)

WeasyPrint base_url 옵션 추가:
  HTML(string=html_content, base_url="http://localhost:8000").write_pdf(...)
```

---

## 3. React 프론트엔드 구현

### 3-1. 전역 상태 설계 (`src/store/brandStore.js`)
```javascript
// Zustand 또는 Context API 사용
// 저장해야 할 상태:

const initialState = {
  // Section O
  brandData: null,           // { business_type, vibes, target, keywords }
  interviewDataO: "",        // format_interview_responses() 결과 텍스트
  brandInfo: null,           // 확정된 { brand_name, brand_name_en, ... } dict

  // Section A
  interviewDataA: "",
  dataA: null,               // { brand_philosophy, brand_essence, ... 병합 dict }

  // Section B
  interviewDataB: "",
  dataB: null,               // { strategic_reasoning, primary_persona, ... 병합 dict }

  // Section C
  interviewDataC: "",
  dataC: null,               // { color_palette, typography, ... }

  // Section DE
  interviewDataDE: "",
  dataDE: null,              // { logo_identity, character_guide, logo_path, char_path }

  // UI
  currentStep: 0,            // 0=O, 1=A, 2=B, 3=C, 4=DE, 5=Preview
  isLoading: false,
};
```

### 3-2. `src/api/client.js`
```javascript
const BASE_URL = "http://localhost:8000/api";

// 공통 fetch 래퍼
async function apiPost(endpoint, body) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "서버 오류가 발생했습니다.");
  }
  return res.json();
}

// Section O
export const getOInterview = (brandData) =>
  apiPost("/section-o/interview", { brand_data: brandData });

export const getOCandidates = (brandData, interviewData) =>
  apiPost("/section-o/candidates", { brand_data: brandData, interview_data: interviewData });

// Section A
export const getAInterview = (brandInfo) =>
  apiPost("/section-a/interview", { brand_info: brandInfo });

export const generateSectionA = (brandInfo, interviewDataA) =>
  apiPost("/section-a/generate", { brand_info: brandInfo, interview_data_a: interviewDataA });

// Section B
export const getBInterview = (brandInfo) =>
  apiPost("/section-b/interview", { brand_info: brandInfo });

export const generateSectionB = (brandInfo, interviewDataA, interviewDataB) =>
  apiPost("/section-b/generate", {
    brand_info: brandInfo,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
  });

// Section C
export const getCInterview = (brandInfo) =>
  apiPost("/section-c/interview", { brand_info: brandInfo });

export const generateSectionC = (brandInfo, interviewDataA, interviewDataB, interviewDataC) =>
  apiPost("/section-c/generate", {
    brand_info: brandInfo,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
  });

// Section DE
export const getDEInterview = (brandInfo, interviewDataC) =>
  apiPost("/section-de/interview", { brand_info: brandInfo, interview_data_c: interviewDataC });

export const generateSectionDE = (brandInfo, dataC, interviewDataA, interviewDataB, interviewDataC, interviewDataDE) =>
  apiPost("/section-de/generate", {
    brand_info: brandInfo,
    data_c: dataC,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
    interview_data_de: interviewDataDE,
  });

// PDF
export const generatePDF = async (brandInfo, dataA, dataB, dataC, dataDE) => {
  const res = await fetch(`${BASE_URL}/pdf/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      brand_info: brandInfo,
      data_a: dataA,
      data_b: dataB,
      data_c: dataC,
      data_de: dataDE,
    }),
  });
  if (!res.ok) throw new Error("PDF 생성 실패");
  // Blob으로 받아서 브라우저 다운로드
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `nametag_${brandInfo.brand_name}_guideline.pdf`;
  a.click();
  URL.revokeObjectURL(url);
};
```

### 3-3. `src/components/InterviewCard.jsx` — 4지선다 공통 컴포넌트
```
Props:
  - questions: array    ← API 응답의 questions 배열
  - reasoning: string   ← API 응답의 reasoning
  - onComplete: (formattedText: string) => void
                        ← 모든 질문 완료 시 format_interview_responses() 결과 텍스트 전달

동작:
  1. reasoning를 상단에 "💡 AI 분석" 형식으로 표시
  2. questions를 순서대로 1개씩 표시 (현재 질문 인덱스 관리)
  3. 각 질문의 question_text 출력
  4. options를 버튼 리스트로 렌더링
     - 앞의 "숫자. " 패턴을 정규식으로 제거: option.replace(/^\d+\.\s*/, "")
  5. 선택 시 다음 질문으로 이동
  6. 모든 질문 완료 시 답변을 아래 형식으로 직렬화하여 onComplete() 호출:
     "Q1. {question_text}\nA: {선택한 option}\n\nQ2. ..."
```

### 3-4. `src/components/CandidateSelector.jsx` — MVB 믹스앤매치 컴포넌트
```
Props:
  - candidates: array   ← /section-o/candidates 응답의 candidates 배열 (4개)
  - onComplete: (brandInfo: object) => void

동작:
  5개 항목을 각각 독립적으로 선택 (기존 select_item × 5 구조 그대로):
  1. 브랜드 이름 선택 → 표시: "{brand_name} ({brand_name_en})"
  2. 네이밍 의미 선택 → 표시: name_meaning
  3. 핵심 슬로건 선택 → 표시: slogan
  4. 스토리 요약 선택 → 표시: story_summary
  5. 브랜드 컬러 선택 → 표시: "{seed_color} ({seed_color_reason})" + 색상 칩

  모두 선택 완료 시 아래 형태로 조합하여 onComplete() 호출:
  {
    brand_name:        candidates[nameIdx].brand_name,
    brand_name_en:     candidates[nameIdx].brand_name_en,
    name_meaning:      candidates[meaningIdx].name_meaning,
    slogan:            candidates[sloganIdx].slogan,
    story_summary:     candidates[storyIdx].story_summary,
    seed_color:        candidates[colorIdx].seed_color,
    seed_color_reason: candidates[colorIdx].seed_color_reason,
  }
```

### 3-5. 각 페이지의 흐름 요약

#### `SectionO.jsx`
```
상태: brandData 입력 폼 (업종/감성/타겟/키워드)
      → "인터뷰 시작" 클릭 → getOInterview(brandData) 호출
      → InterviewCard 렌더링 (onComplete → interviewDataO 저장)
      → "후보 생성" 클릭 → getOCandidates(brandData, interviewDataO) 호출
      → CandidateSelector 렌더링 (onComplete → brandInfo 저장)
      → "다음 단계" 클릭 → currentStep = 1
```

#### `SectionA.jsx` ~ `SectionDE.jsx` (공통 패턴)
```
상태: 스토어에서 brandInfo, 이전 interviewData 읽기
      → "인터뷰 시작" 클릭 → get{X}Interview(brandInfo) 호출
      → InterviewCard 렌더링 (onComplete → interviewData_{X} 저장)
      → "생성 시작" 클릭 → generateSection{X}(...) 호출
      → 로딩 스피너 표시 (AI 처리 시간 최대 수십 초)
      → 완료 시 data_{X} 저장 + "다음 단계" 버튼 활성화
```

#### `SectionDE.jsx` 추가 처리
```
generate 완료 후:
  - data_de.logo_path → <img src="http://localhost:8000{logo_path}"> 로 미리보기
  - data_de.char_path → <img src="http://localhost:8000{char_path}"> 로 미리보기
```

#### `Preview.jsx`
```
스토어에서 모든 data 읽어서 요약 표시
"PDF 다운로드" 클릭 → generatePDF(brandInfo, dataA, dataB, dataC, dataDE) 호출
→ 브라우저 자동 다운로드
```

---

## 4. 로컬 실행 방법

```bash
# 백엔드
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 프론트엔드
cd frontend
npm install
npm run dev        # http://localhost:5173
```

---

## 5. 자주 발생하는 버그 체크리스트

- [ ] **CORS 오류**: `main.py`의 `allow_origins`에 React 개발 서버 주소(`http://localhost:5173`) 포함 확인
- [ ] **이미지 404**: `app.mount("/assets", ...)` 경로와 실제 `assets/` 폴더 위치가 `main.py` 기준인지 확인
- [ ] **PDF 이미지 깨짐**: `HTML(string=..., base_url="http://localhost:8000")` base_url 누락 확인
- [ ] **JSON 파싱 실패**: Gemini 응답에 마크다운 코드블록(` ```json `) 포함 시 `re.search(r'\{[\s\S]*\}', raw_text)` 로 추출
- [ ] **타임아웃**: AI 생성 API 응답이 최대 90초+ 걸릴 수 있으므로 프론트에서 로딩 상태 필수 처리
- [ ] **data_a 병합**: section_a/generate에서 A1+A2+A3를 `merged.update()` 로 병합하지 않으면 PDF builder에서 키를 못 찾음
- [ ] **C0 인터뷰 구조**: `question_id` 필드가 없음. InterviewCard에서 `q.question_id` 대신 인덱스로 처리할 것
- [ ] **Windows 경로**: 이미지 저장 경로의 역슬래시 → `replace("\\", "/")` 처리 후 URL로 변환