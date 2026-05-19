# NameTag 로깅 시스템 - 종합 가이드 📋

> **마지막 업데이트**: 2026-05-18  
> **현재 상태**: ✅ 완성  
> **목표**: AI 응답 전체 추적 + 변수 자동 기록 + 파일 저장

---

## 📌 시스템 개요

### 전체 아키텍처
```
사용자 입력 (Streamlit)
    ↓
FastAPI 라우터 (backend/routers/)
    ↓
브랜드 생성 서비스 (services/brand_generator.py)
    ↓
Gemini AI API
    ↓
📄 응답 저장: logs/ai_responses/*.txt + *.json
📊 로그 출력: Docker에서 전체 응답 확인 가능
📈 변수 추적: logs/variables.jsonl에 기록
    ↓
완전히 가시화된 상태!
```

### 주요 기능
| 기능 | 설명 | 저장 위치 |
|------|------|---------|
| **응답 저장** | AI 응답을 TXT + JSON으로 저장 | `logs/ai_responses/` |
| **로그 기록** | 자세한 단계별 로깅 | Docker + `logs/nametag.log` |
| **변수 추적** | 모든 변수를 JSONL 형식으로 기록 | `logs/variables.jsonl` |
| **세션 관리** | 요청마다 고유 UUID 생성 | 모든 로그에 포함 |
| **logo_design** | 📌 **NEW**: 로고 설계 정보 추가 수신 | JSON 응답에 포함 |

---

## 🏗️ 파일 구조

### 1. **services/brand_generator.py** ⭐ (핵심 파일)

#### 임포트 및 초기화
```python
import json
from pathlib import Path
from datetime import datetime
from utils.logger import get_logger, get_tracker

# 응답 저장 디렉토리 자동 생성
RESPONSES_DIR = Path(__file__).parent.parent / "logs" / "ai_responses"
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
```

#### 응답 저장 함수 - `save_ai_response()`
```python
def save_ai_response(response_text: str, response_type: str, session_id: str) -> tuple[str, str]:
    """
    AI 응답을 txt와 JSON 파일로 저장
    
    역할:
    1. TXT 파일: 응답 원본 그대로 저장 (읽기 쉬움)
    2. JSON 파일: 예쁘게 포맷팅해서 저장 (분석 용이)
    
    반환:
    - (txt_파일_경로, json_파일_경로)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{response_type}_{timestamp}_{session_id[:8]}"
    
    # 예: logo_variables_20260518_185532_a1b2c3d4.txt
```

**저장되는 파일 예시:**
```
logs/ai_responses/
├── logo_variables_20260518_185532_a1b2c3d4.txt      # 전체 응답 원본
├── logo_variables_20260518_185532_a1b2c3d4.json     # 포맷팅된 JSON
├── brand_identity_20260518_185615_e5f6g7h8.txt
└── brand_identity_20260518_185615_e5f6g7h8.json
```

#### 함수별 역할

**a) `build_logo_variables_prompt()`**
```python
# 역할: AI에 보낼 프롬프트 생성
# 입력: business_type, vibes, target, keywords
# 출력: 상세한 JSON 형식 지정 프롬프트 문자열
# 예: "업종/서비스: 홈데코, 브랜드 감성: 따뜻 & 친근..."
```

**b) `build_user_prompt()`**
```python
# 역할: 브랜드 정체성 생성용 프롬프트
# 입력: business_type, vibes, target, keywords
# 출력: 브랜드명, 타이포그래피, 캐릭터 추천 프롬프트
# 예: "아래 JSON 형식으로만 응답하세요..."
```

**c) `generate_logo_variables()` 함수 흐름**

```
1️⃣ 세션 초기화
   └─ session_id 생성
   └─ tracker 초기화

2️⃣ AI 호출
   └─ Gemini API에 로고 변수 추천 요청

3️⃣ 응답 저장 ⭐
   ├─ save_ai_response()로 TXT + JSON 저장
   └─ 로그에 전체 응답 출력 (여러 줄로 분할)

4️⃣ JSON 파싱
   └─ extract_json()로 구조화된 데이터 추출

5️⃣ 변수 기록
   ├─ brand_identity 변수들 추적
   ├─ logo_variables 변수들 추적
   └─ tracker.set_variable()로 기록

6️⃣ 자동 매핑 (MOOD_MAPPING)
   ├─ target_mood 확인
   └─ 빈 값에 기본값 자동 할당

7️⃣ 반환
   └─ session_id, brand_identity, logo_variables 등
```

**d) `generate_brand_identity()` 함수 흐름**

```
1️⃣ 세션 초기화 + AI 호출
   └─ Gemini API에 브랜드 정체성 요청

2️⃣ 응답 저장 ⭐
   ├─ save_ai_response()로 TXT + JSON 저장
   └─ 로그에 전체 응답 출력

3️⃣ JSON 파싱 + 검증
   └─ 필수 키 확인: brands, typography, character

4️⃣ 변수 기록
   └─ BRAND_NAME, BRAND_SLOGAN 추적

5️⃣ 반환
   └─ 파싱된 결과 (brands, typography, character)
```

#### MOOD_MAPPING 테이블
```python
MOOD_MAPPING = {
    "모던 & 신뢰": {
        "brand_color": "#333333",
        "font_style": "기하학적 산세리프",
        "symbol_type": "기하학적",
    },
    "따뜻 & 친근": {
        "brand_color": "#C8553D",
        "font_style": "부드러운 산세리프",
        "symbol_type": "유기적",
    },
    # ... 총 8가지 무드
}
```

**역할**: target_mood가 선택되면, AI가 지정하지 않은 값들을 자동으로 채움

---

### 2. **utils/logger.py** (로깅 시스템)

```python
# 역할: 중앙 집중식 로거 관리
# 제공: get_logger(), get_tracker()

logger = get_logger("NameTag.BrandGenerator")
# JSON 형식 로그 + 콘솔 출력

tracker = get_tracker(session_id)
# 변수 추적 (JSONL 형식)
```

#### 로거 사용 예시
```python
logger.info("✅ 성공")      # INFO 레벨
logger.debug("디버그")      # DEBUG 레벨
logger.warning("⚠️ 경고")  # WARNING 레벨
logger.error("❌ 오류")     # ERROR 레벨
```

#### 변수 추적 예시
```python
tracker.set_variable("BRAND_NAME", "온연", source="ai_response")
tracker.set_variable("LOGO_COLOR", "#2D6A4F", source="auto_inferred")
tracker.log_step("ai_request", {"model": "gemini-1.5-pro"})
```

---

### 3. **backend/routers/brand.py** (API 엔드포인트)

```python
# POST /api/v1/brand/logo-variables
# 역할: 로고 생성 변수 추천 엔드포인트

@router.post("/logo-variables")
async def recommend_logo_variables(request: LogoVariablesRequest):
    # services/brand_generator.generate_logo_variables() 호출
    # → TXT + JSON 저장
    # → 로그 기록
    # → 변수 추적
    # → 결과 반환
```

---

### 4. **docker-compose.yml** (Docker 설정)

```yaml
backend:
  volumes:
    - ./logs:/logs  # ⭐ logs 디렉토리 마운트
  environment:
    - PYTHONUNBUFFERED=1  # 실시간 로그 출력
    - GEMINI_API_KEY=${GEMINI_API_KEY}
```

**역할**: 
- 호스트의 `logs/` 디렉토리를 컨테이너의 `/logs`로 마운트
- 컨테이너에서 저장된 파일이 호스트에서 접근 가능

---

## 🔄 데이터 흐름

### 1단계: 사용자 입력 (Streamlit)
```
business_type = "홈데코"
vibes = ["따뜻 & 친근"]
target = "직장인"
keywords = "소품"
```

### 2단계: API 호출
```python
POST /api/v1/brand/logo-variables
{
    "business_type": "홈데코",
    "vibes": ["따뜻 & 친근"],
    "target": "직장인",
    "keywords": "소품"
}
```

### 3단계: AI 호출
```python
# services/brand_generator.generate_logo_variables()
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents="...(프롬프트)...",
)
raw_text = response.text  # ← JSON 문자열
```

### 4단계: 파일 저장
```python
# save_ai_response() 호출
logo_variables_20260518_185532_a1b2c3d4.txt  # 원본
logo_variables_20260518_185532_a1b2c3d4.json # 포맷팅됨
```

### 5단계: 로그 출력
```
INFO:NameTag.BrandGenerator:====================================...
INFO:NameTag.BrandGenerator:📨 AI FULL RESPONSE (AI 전체 응답)
INFO:NameTag.BrandGenerator:====================================...
INFO:NameTag.BrandGenerator:{
INFO:NameTag.BrandGenerator:  "brand_identity": {
INFO:NameTag.BrandGenerator:    "brand_name": "오붓",
...
INFO:NameTag.BrandGenerator:  }
INFO:NameTag.BrandGenerator:}
INFO:NameTag.BrandGenerator:====================================...
```

### 6단계: 변수 추적
```jsonl
{"timestamp": "2026-05-18T18:55:32", "variable": "BRAND_NAME", "value": "오붓", "source": "ai_response"}
{"timestamp": "2026-05-18T18:55:32", "variable": "LOGO_COLOR", "value": "#C8553D", "source": "auto_inferred"}
```

---

## 📂 로그 파일 위치

```
logs/
├── nametag.log                  # 전체 시스템 로그 (JSON 형식)
├── variables.jsonl              # 변수 추적 (한 줄씩 JSON)
└── ai_responses/                # ⭐ AI 응답 저장
    ├── logo_variables_20260518_185532_a1b2c3d4.txt
    ├── logo_variables_20260518_185532_a1b2c3d4.json
    ├── brand_identity_20260518_185615_e5f6g7h8.txt
    └── brand_identity_20260518_185615_e5f6g7h8.json
```

---

## 🚀 사용 방법

### 1. Docker 시작
```bash
cd f:\workspace\Name_Tag
docker compose up -d
```

### 2. 실시간 로그 모니터링
```bash
# 전체 로그 (실시간)
docker compose logs -f backend

# AI 응답만 보기
docker compose logs -f backend | grep "FULL RESPONSE" -A 200

# 변수 추적 보기
docker compose logs -f backend | grep "set_variable\|log_step"
```

### 3. 저장된 파일 확인
```bash
# TXT 파일 보기 (원본)
cat logs/ai_responses/logo_variables_*.txt

# JSON 파일 보기 (포맷팅됨)
cat logs/ai_responses/logo_variables_*.json | jq '.'

# 변수 추적 보기
cat logs/variables.jsonl | jq '.'
```

### 4. Streamlit에서 테스트
```bash
streamlit run app.py
# http://localhost:8501에서 폼 작성 → 제출
```

---

## 🔍 각 응답의 구조

### AI Response 구조 (brand_identity) ⭐ **업데이트됨**
```json
{
  "brands": [
    {
      "name": "오붓",
      "meaning": "순우리말 '오붓하다'에서...",
      "story": "바쁜 업무를 마치고...",
      "slogan": "당신의 방에 심는 작은 온기"
    },
    {
      "name": "온연",
      "meaning": "...",
      "story": "...",
      "slogan": "..."
    },
    {
      "name": "온온",
      "meaning": "...",
      "story": "...",
      "slogan": "..."
    }
  ],
  "typography": {
    "korean": "나눔명조",
    "english": "Playfair Display",
    "reason": "따뜻하고 전통적인 감성을..."
  },
  "character": {
    "name": "따뜻이",
    "concept": "따뜻한 감정을 담은 캐릭터",
    "personality": "친근함, 위로, 따뜻함",
    "visual": "둥근 형태의..."
  },
  "logo_design": {
    "brand_name": "오붓",
    "brand_topic": "홈데코 소품",
    "core_value": "따뜻함, 위로",
    "target_mood": "따뜻 & 친근",
    "symbol_type": "유기적",
    "font_style": "부드러운 산세리프",
    "font_reference": "Playfair Display",
    "font_weight": "medium",
    "brand_color": "#C8553D",
    "logo_type": "심볼+텍스트 조합",
    "background": "흰색"
  }
}
```

### 변수 추적 구조 (variables.jsonl)
```json
{"timestamp": "2026-05-18T18:55:32.123456", "variable": "BRAND_NAME", "value": "오붓", "source": "ai_response"}
{"timestamp": "2026-05-18T18:55:33.234567", "variable": "BRAND_SLOGAN", "value": "당신의 방에...", "source": "ai_response"}
{"timestamp": "2026-05-18T18:55:34.345678", "variable": "LOGO_DESIGN_BRAND_COLOR", "value": "#C8553D", "source": "ai_response"}
{"timestamp": "2026-05-18T18:55:34.456789", "variable": "LOGO_DESIGN_SYMBOL_TYPE", "value": "유기적", "source": "ai_response"}
{"timestamp": "2026-05-18T18:55:34.567890", "variable": "LOGO_DESIGN_FONT_STYLE", "value": "부드러운 산세리프", "source": "ai_response"}
```

---

## ✨ 주요 개선사항

| 이전 | 현재 | 개선 |
|------|------|------|
| 응답이 로그에서 중간에 끊김 | TXT + JSON 파일로 저장 | 전체 응답 보존 |
| 로그가 한 줄로 긴 문자열 | 여러 줄로 분할해서 출력 | 읽기 쉬운 포맷 |
| 변수 추적 안 함 | JSONL 형식으로 모든 변수 기록 | 변수 변화 추적 가능 |
| 세션 구분 안 함 | UUID 기반 세션 관리 | 요청별 추적 가능 |
| 자동 매핑 없음 | MOOD_MAPPING으로 빈 값 자동 채움 | 일관성 있는 설정 |

---

## 🎯 문제 해결

### Q: 로그가 Docker에서 보이지 않음
```bash
# 확인
docker compose logs backend
# 또는
docker compose exec backend tail -f /logs/nametag.log
```

### Q: AI 응답 파일이 생성되지 않음
```bash
# 폴더 확인
docker compose exec backend ls -la /logs/ai_responses/

# 권한 확인
docker compose exec backend chmod 777 /logs/ai_responses/
```

### Q: JSON 파일이 생성되었는데 내용이 이상함
```bash
# 원본 TXT 파일 확인
docker compose exec backend cat /logs/ai_responses/logo_variables_*.txt
```

---

## 📊 시스템 상태 확인 체크리스트

- [ ] Docker 컨테이너 실행 중
- [ ] `logs/` 디렉토리 존재
- [ ] `logs/ai_responses/` 디렉토리 생성됨
- [ ] TXT + JSON 파일 생성됨
- [ ] 로그에서 AI 응답 전체 출력됨
- [ ] `variables.jsonl` 파일에 변수 기록됨
- [ ] Streamlit에서 결과 표시됨

---

## 🔗 관련 파일

| 파일 | 역할 |
|------|------|
| [services/brand_generator.py](services/brand_generator.py) | AI 호출 + 응답 저장 + 로깅 |
| [utils/logger.py](utils/logger.py) | 중앙 로거 관리 |
| [backend/routers/brand.py](backend/routers/brand.py) | API 엔드포인트 |
| [docker-compose.yml](docker-compose.yml) | Docker 설정 |
| [app.py](app.py) | Streamlit 프론트엔드 |

---

## 📝 최종 정리

✅ **이 시스템은:**
1. **전체 AI 응답을 파일로 저장** (중간에 끊기지 않음)
2. **모든 변수를 자동으로 추적** (누가, 언제, 어디서 설정했는지)
3. **예쁜 로그 포맷** (읽기 쉽고 분석 가능)
4. **자동 값 매핑** (mood에 따라 기본값 자동 할당)
5. **세션 기반 관리** (요청별로 독립적 추적)
6. **📌 logo_design 정보 수신** (로고 설계 상세 정보)

🎉 **결과**: AI가 어떤 응답을 하는지, 어떤 변수가 어떤 값을 가지는지 **전부** 볼 수 있습니다!

---

## 📊 logo_design 필드 상세 정보

### 필드별 설명
| 필드 | 설명 | 예시 |
|------|------|------|
| `brand_name` | 로고에 표시될 브랜드 이름 | "오붓" |
| `brand_topic` | 사업 주제/업종 | "홈데코 소품" |
| `core_value` | 브랜드 핵심 가치 | "따뜻함, 위로" |
| `target_mood` | 원하는 브랜드 감성 | "따뜻 & 친근" |
| `symbol_type` | 심볼 스타일 | "유기적" |
| `font_style` | 서체 느낌 | "부드러운 산세리프" |
| `font_reference` | 참고할 폰트 | "Playfair Display" |
| `font_weight` | 폰트 굵기 | "medium" |
| `brand_color` | 메인 색상 (컬러 코드) | "#C8553D" |
| `logo_type` | 로고 구성 방식 | "심볼+텍스트 조합" |
| `background` | 배경 색상 | "흰색" |

### 로고 설계 정보 사용 사례
```python
# 로고 생성에 필요한 모든 정보가 한 곳에!
logo_design = result["logo_design"]

# 로고 이미지 생성 호출
generate_logo_image(
    brand_name=logo_design["brand_name"],
    brand_story=logo_design["brand_topic"],
    vibes=[logo_design["target_mood"]],
    symbol_type=logo_design["symbol_type"],
    brand_color=logo_design["brand_color"],
    logo_type=logo_design["logo_type"],
    background=logo_design["background"]
)
```
