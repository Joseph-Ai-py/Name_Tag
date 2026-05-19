# 🎨 NameTag 백엔드 - 브랜드 정체성 및 로고 생성 시스템

AI 기반의 브랜드 정체성과 **SVG 형식의 로고를 자동 생성**하는 FastAPI 백엔드입니다.

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [주요 기능](#주요-기능)
3. [시스템 아키텍처](#시스템-아키텍처)
4. [설치 및 실행](#설치-및-실행)
5. [API 엔드포인트](#api-엔드포인트)
6. [SVG 로고 저장 시스템](#svg-로고-저장-시스템)
7. [데이터 흐름](#데이터-흐름)
8. [에러 처리](#에러-처리)
9. [사용 예시](#사용-예시)

---

## 🚀 프로젝트 개요

**NameTag**는 초기 스타트업과 1인 기업을 위한 AI 기반 브랜드 생성 플랫폼입니다.

### 핵심 기능
- 🤖 **Google Gemini AI**를 활용한 지능형 브랜드 정체성 생성
- 🎨 **SVG 벡터 형식**의 로고 자동 생성 및 저장
- 📊 구조화된 JSON 응답으로 프론트엔드와의 seamless 통합
- 📝 세션 기반 요청 추적 및 로깅

---

## ✨ 주요 기능

### 1️⃣ 브랜드 정체성 생성
```
입력: 업종, 브랜드 감성, 타겟 고객, 추가 키워드
출력: 
  • 3개의 브랜드 네이밍 옵션
  • 타이포그래피 추천
  • 마스코트 캐릭터 디자인
```

### 2️⃣ 로고 변수 추천
```
입력: 동일한 브랜드 정보
출력:
  • 로고 생성을 위한 최적화된 변수 세트
  • 색상 코드, 심볼 스타일, 폰트 스타일 등
  • MOOD_MAPPING을 통한 자동 변수 설정
```

### 3️⃣ **SVG 로고 생성 및 저장** ⭐
```
입력: 브랜드명, 로고 설정 변수
처리:
  • AI가 SVG 코드 직접 생성
  • 벡터 형식으로 저장 (확장 가능한 품질)
  • PNG 대신 SVG 사용으로 메모리 효율성 증가

저장 경로: logo/logo_{brand_name}_{timestamp}.svg
```

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     클라이언트 (Frontend)                          │
│                   (React + Vite + TypeScript)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI 백엔드 (main.py)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Router 계층 (routers/brand.py)              │  │
│  │  ✓ POST /api/v1/brand/generate                          │  │
│  │  ✓ POST /api/v1/brand/logo-variables                   │  │
│  │  ✓ GET /health                                          │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                              │
│  ┌────────────────▼─────────────────────────────────────────┐  │
│  │         Service 계층 (services/brand_generator.py)       │  │
│  │  ✓ generate_brand_identity()                            │  │
│  │  ✓ generate_logo_variables()                            │  │
│  │  ✓ generate_logo_svg() → **SVG 생성**                   │  │
│  │  ✓ generate_character_image()                           │  │
│  └────────────────┬──────────────────────────────────────────┘  │
│                   │                                              │
│  ┌────────────────▼─────────────────────────────────────────┐  │
│  │         외부 API 호출 (Google Gemini)                     │  │
│  │  • gemini-1.5-pro (텍스트 생성)                          │  │
│  │  • gemini-3.1-flash-image (SVG 코드 생성)               │  │
│  └────────────────┬──────────────────────────────────────────┘  │
│                   │                                              │
│  ┌────────────────▼─────────────────────────────────────────┐  │
│  │              Utility 계층 (utils/)                        │  │
│  │  • parser.py (JSON 추출)                                │  │
│  │  • logger.py (로깅 및 세션 추적)                        │  │
│  │  • svg_handler.py → **SVG 저장**                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│                  📁 저장소                                        │
│                  └─ logo/                                       │
│                     └─ logo_{brand_name}_{timestamp}.svg       │
└─────────────────────────────────────────────────────────────────┘
                         │ HTTP Response (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   클라이언트 (Frontend)                           │
│              (JSON 응답 수신 및 렌더링)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 설치 및 실행

### 필수 요구사항
- Python 3.9 이상
- Google Gemini API 키 2개 (텍스트용 + 이미지용)

### 설치 단계

1. **저장소 클론**
```bash
git clone <repository-url>
cd notebook_backend
```

2. **가상 환경 생성**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **.env 파일 설정**
```env
GEMINI_API_KEY=your_gemini_api_key_for_text
GEMINI_IMAGE_API_KEY=your_gemini_api_key_for_images
```

5. **백엔드 실행**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **API 문서 확인**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔌 API 엔드포인트

### 1. POST /api/v1/brand/generate
완전한 브랜드 정체성 생성 (3개 옵션)

**요청:**
```json
{
  "business_type": "온라인 친환경 쇼핑몰",
  "vibes": ["모던", "신뢰", "자연친화"],
  "target": "20-40대 환경 의식 있는 소비자",
  "keywords": "지속가능성, 투명성"
}
```

**응답:**
```json
{
  "session_id": "a1b2c3d4",
  "brands": [
    {
      "name": "지속가능마켓",
      "meaning": "지속가능한 가치와 시장의 만남",
      "story": "친환경 제품을 통해 일상을 바꾼다는 철학...",
      "slogan": "작은 선택이 만드는 큰 변화"
    },
    {...},
    {...}
  ],
  "typography": [...],
  "character": [...]
}
```

---

### 2. POST /api/v1/brand/logo-variables
로고 생성용 변수 추천

**요청:**
```json
{
  "business_type": "온라인 친환경 쇼핑몰",
  "vibes": ["모던", "신뢰"],
  "target": "20-40대 직장인",
  "keywords": "지속가능한"
}
```

**응답:**
```json
{
  "session_id": "a1b2c3d4",
  "brand_identity": {
    "brand_name": "지속가능마켓",
    "brand_topic": "친환경 제품 온라인 쇼핑몰",
    "core_value": "지속가능성, 투명성",
    "slogan": "작은 선택이 만드는 큰 변화"
  },
  "logo_variables": {
    "target_mood": "자연 & 지속가능",
    "brand_color": "#2D6A4F",
    "font_style": "유기적 산세리프",
    "symbol_type": "유기적",
    "logo_type": "심볼+텍스트 조합",
    "background": "흰색"
  },
  "recommendations_reason": "자연친화적인 감성을 표현하기 위해...",
  "logo_svg": "<svg>...</svg>"
}
```

---

### 3. GET /health
헬스 체크

**응답:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-19T10:30:00Z"
}
```

---

## 🎨 SVG 로고 저장 시스템

### SVG 생성 프로세스

```python
# 1️⃣ AI에게 SVG 코드 생성 요청
image_prompt = f"""
당신은 전문 로고 디자이너입니다.
브랜드명: {brand_name}
색상: {brand_color}
스타일: {symbol_type}

SVG 형식의 로고 코드를 생성하세요.
JSON 형식: {{"logo_svg": "<svg>...</svg>"}}
"""

# 2️⃣ Gemini API로부터 SVG 코드 수신
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[content],
    config=config
)

# 3️⃣ JSON에서 SVG 코드 추출
ai_response = json.loads(response)
# {
#   "logo_svg": "<svg>...</svg>"
# }
```

### SVG 파일 저장 코드 ⭐

```python
# 4️⃣ SVG 파일로 저장
if "logo_svg" in ai_response:
    svg_content = ai_response["logo_svg"]
    logo_path = f"logo/logo_{brand_name}_{timestamp}.svg"
    
    try:
        with open(logo_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"✅ SVG 파일이 성공적으로 저장되었습니다: {logo_path}")
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {e}")
```

### SVG 저장의 장점

| 특징 | SVG | PNG |
|------|-----|-----|
| **크기** | 매우 작음 (KB 단위) | 상대적으로 큼 (MB 단위) |
| **확장성** | 무한 확대 가능 | 품질 저하 발생 |
| **편집성** | 코드로 수정 가능 | 재생성 필요 |
| **인쇄** | 고해상도 인쇄 가능 | 픽셀화 우려 |
| **메모리** | 효율적 | 메모리 소비 큼 |
| **웹 최적화** | 반응형 디자인 지원 | 고정 크기만 가능 |

---

## 📊 데이터 흐름

### 요청-응답 사이클 (9단계)

```
[1️⃣] 클라이언트 → 서버: 원본 요청
    원본 요청 (JSON)
        ↓
[2️⃣] Router: Pydantic 검증
    검증된 요청 + 세션 ID
        ↓
[3️⃣] Service: generate_logo_variables() 호출
    Service 입력 변수
        ↓
[4️⃣] Service: 프롬프트 구성
    변수 → 프롬프트 텍스트
        ↓
[5️⃣] Gemini API: AI 모델 호출
    프롬프트 + 시스템 인스트럭션
        ↓
[6️⃣] Gemini API: JSON 응답 반환
    AI 생성 JSON (+ SVG 코드)
        ↓
[7️⃣] Service: JSON 파싱 및 변수 추출
    extract_json() → MOOD_MAPPING → 로그 저장
        ↓
[8️⃣] Router: SVG 파일 저장 후 Pydantic 직렬화
    Pydantic 모델 → JSON
        ↓
[9️⃣] FastAPI: HTTP 응답 반환
    HTTP 200 OK + JSON
        ↓
    클라이언트: 응답 수신 및 렌더링
```

### 변수 변환 흐름

```
원본 요청 (4개 필드)
  ├─ business_type: "온라인 쇼핑몰"
  ├─ vibes: ["모던", "신뢰"]
  ├─ target: "20-30대"
  └─ keywords: "지속가능한"
      ↓
Pydantic 검증 + 세션 ID 추가
  └─ session_id: "a1b2c3d4"
      ↓
프롬프트 구성
  └─ "당신은 브랜드 디렉터입니다. 다음 정보를 바탕으로..."
      ↓
Gemini API 호출
      ↓
JSON 응답 수신 (SVG 코드 포함)
  └─ {
       "brand_identity": {...},
       "logo_variables": {...},
       "logo_svg": "<svg>...</svg>"
     }
      ↓
변수 추출 & SVG 저장
  ├─ extract_json() - 텍스트에서 JSON 추출
  ├─ SVG 파일 저장 (logo/logo_*.svg)
  ├─ 필수 키 검증
  └─ MOOD_MAPPING - 무드에 따른 자동값 설정
      ↓
최종 응답 생성
  └─ LogoVariablesResponse 모델로 직렬화
      ↓
HTTP 응답 반환
```

---

## 🚨 에러 처리

### 에러 타입별 처리

| 에러 타입 | HTTP 코드 | 처리 방식 |
|----------|---------|---------|
| 요청 검증 실패 | 422 | Pydantic 자동 검증 |
| API 키 누락 | 500 | RuntimeError |
| JSON 파싱 실패 | 422 | ValueError |
| SVG 저장 실패 | 500 | IOError 처리 |
| Gemini API 에러 | 500 | Exception 캐치 |

### 에러 응답 예시

```json
{
  "detail": "ensure this value has at least 3 characters"
}
```

---

## 💡 사용 예시

### Python 예시

```python
import requests
import json

# API 요청
response = requests.post(
    "http://localhost:8000/api/v1/brand/logo-variables",
    json={
        "business_type": "온라인 친환경 쇼핑몰",
        "vibes": ["모던", "신뢰"],
        "target": "20-40대 직장인",
        "keywords": "지속가능한"
    }
)

# 응답 처리
if response.status_code == 200:
    result = response.json()
    brand_name = result["brand_identity"]["brand_name"]
    svg_content = result.get("logo_svg")
    
    # SVG 파일 저장 (필요시)
    if svg_content:
        with open(f"logo_{brand_name}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"✅ SVG 파일 저장 완료: logo_{brand_name}.svg")
else:
    print(f"Error: {response.status_code}")
```

### cURL 예시

```bash
curl -X POST "http://localhost:8000/api/v1/brand/logo-variables" \
  -H "Content-Type: application/json" \
  -d '{
    "business_type": "온라인 친환경 쇼핑몰",
    "vibes": ["모던", "신뢰"],
    "target": "20-40대 직장인",
    "keywords": "지속가능한"
  }'
```

### JavaScript 예시

```javascript
const response = await fetch('http://localhost:8000/api/v1/brand/logo-variables', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    business_type: "온라인 친환경 쇼핑몰",
    vibes: ["모던", "신뢰"],
    target: "20-40대 직장인",
    keywords: "지속가능한"
  })
});

const result = await response.json();
const svgContent = result.logo_svg;

// SVG 다운로드
const a = document.createElement('a');
a.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent);
a.download = `logo_${result.brand_identity.brand_name}.svg`;
a.click();
```

---

## 📁 디렉토리 구조

```
notebook_backend/
├── requirements.txt              # Python 의존성
├── README.md                     # 이 파일
├── BACKEND_FLOW_EXPLANATION.ipynb # 백엔드 동작 설명
├── logo/                         # SVG 로고 저장 디렉토리 ⭐
│   ├── logo_지속가능마켓_20260519_103000.svg
│   ├── logo_따뜻한마켓_20260519_110000.svg
│   └── ...
├── backend/
│   ├── main.py                   # FastAPI 앱 초기화
│   ├── routers/
│   │   └── brand.py              # 엔드포인트 정의
│   ├── services/
│   │   └── brand_generator.py    # 비즈니스 로직
│   └── utils/
│       ├── parser.py             # JSON 파싱
│       ├── logger.py             # 로깅 시스템
│       └── svg_handler.py        # SVG 저장 처리
└── logs/
    ├── ai_responses/             # AI 응답 저장
    └── session_logs/             # 세션 로그
```

---

## 🔧 주요 의존성

```
python-dotenv>=1.0.0      # 환경 변수 관리
google-genai>=2.0.0       # Google Gemini API
pillow>=10.2.0            # 이미지 처리
jupyter>=1.0.0            # Jupyter 노트북
pandas>=2.0.0             # 데이터 분석
numpy>=1.24.0             # 수치 계산
fastapi>=0.100.0          # 웹 프레임워크
pydantic>=2.0.0           # 데이터 검증
```

---

## 🎯 핵심 포인트

✅ **SVG 중심 설계** ⭐
- PNG 대신 SVG로 저장하여 확장성과 메모리 효율성 확보
- 무한 확대 가능한 벡터 로고
- 웹 최적화 및 반응형 디자인 지원

✅ **AI 기반 자동화**
- Gemini API로 완전 자동화된 로고 생성
- 사용자 입력만으로 프로페셔널한 로고 생성

✅ **구조화된 응답**
- JSON 기반 응답으로 프론트엔드와의 seamless 통합
- MOOD_MAPPING으로 일관된 디자인 유지

✅ **세션 기반 추적**
- 모든 요청에 고유한 session_id 부여
- 디버깅 및 문제 분석 용이

---

## 📖 추가 학습 자료

- [BACKEND_FLOW_EXPLANATION.ipynb](BACKEND_FLOW_EXPLANATION.ipynb) - 상세한 백엔드 동작 설명
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)
- [SVG 스펙](https://www.w3.org/TR/SVG2/)

---

## 👥 개발팀

**NameTag Development Team**

---

## 📄 라이선스

이 프로젝트는 NameTag에 의해 개발되었습니다.

---

## 💬 문의 및 피드백

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해주세요.

---

**마지막 업데이트**: 2026년 5월 19일  
**버전**: 1.0.0  
**상태**: 🟢 활성
