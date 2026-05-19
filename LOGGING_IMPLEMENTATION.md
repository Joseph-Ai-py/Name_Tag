# 🎯 NameTag 상세 로깅 & 변수 추적 시스템 구현 완료

## 📋 작업 요약

사용자 요청에 따라 NameTag 애플리케이션에 **매우 상세한 로깅 시스템**을 구축하였습니다.

---

## 🆕 새로 추가된 기능

### 1️⃣ **상세 로깅 시스템** (`utils/logger.py`)
- **JSON 기반 구조화된 로깅**: 모든 로그를 JSON 형식으로 저장
- **변수 추적 (VariableTracker)**: 각 변수의 값, 출처, 타임스탐프 기록
- **이중 로그**: 
  - `logs/nametag.log` - 전체 시스템 로그
  - `logs/variables.jsonl` - 변수별 추적 로그

### 2️⃣ **로고 변수 생성 기능** (`services/brand_generator.py`)
새로운 함수: `generate_logo_variables()`
- AI(Gemini)로부터 받는 데이터:
  - `BRAND_NAME` - 브랜드명
  - `BRAND_TOPIC` - 사업 주제
  - `CORE_VALUE` - 핵심 가치
  - `TARGET_MOOD` - 브랜드 감성
  - `BRAND_COLOR` - 색상
  - `FONT_STYLE` - 폰트
  - `SYMBOL_TYPE` - 심볼 스타일
  - `LOGO_TYPE` - 로고 구성
  - `BACKGROUND` - 배경색

**무드 기반 자동 매핑**:
- TARGET_MOOD에 따라 자동으로 색상, 폰트, 심볼 추천
- 8가지 무드별 기본값 테이블 구현

### 3️⃣ **새로운 API 엔드포인트** (`backend/routers/brand.py`)
```
POST /api/v1/brand/logo-variables
```
- 브랜드 입력 받음
- AI로부터 로고 생성 변수 추천
- 모든 변수를 추적하여 응답

### 4️⃣ **Streamlit UI 업데이트** (`app.py`)
- Session ID 추적: 각 사용자 세션 고유 ID
- 로고 변수 섹션 표시:
  - 📋 브랜드 정체성
  - 🔧 로고 변수 (실시간 표시)
  - 📊 변수 추적 정보
  - 💡 추천 이유
- 사이드바에 로그 확인 가이드

### 5️⃣ **Docker 환경 최적화**
- `docker-compose.yml` 업데이트:
  - 로그 디렉토리 마운트
  - JSON 로깅 드라이버 설정
  - Python 경로 설정
- `backend/Dockerfile` 수정:
  - 공유 모듈 복사 (utils, services)
  - 로그 디렉토리 생성
  - PYTHONPATH 설정

---

## 📁 수정/생성된 파일 목록

### 생성된 파일
| 파일 | 설명 |
|------|------|
| `utils/logger.py` | 로깅 시스템 (StructuredFormatter, VariableTracker 등) |
| `logs/` (디렉토리) | 로그 파일 저장 위치 |
| `LOGGING_GUIDE.md` | 로그 사용 가이드 (총 300+ 줄) |
| `LOGGING_IMPLEMENTATION.md` | 이 파일 |

### 수정된 파일
| 파일 | 변경 사항 |
|------|----------|
| `services/brand_generator.py` | `generate_logo_variables()` 함수 추가, MOOD_MAPPING 테이블 추가 |
| `backend/routers/brand.py` | 새 엔드포인트 `/api/v1/brand/logo-variables` 추가 |
| `app.py` | Session ID 추적, 로고 변수 섹션 표시 |
| `backend/main.py` | 로거 초기화, 경로 설정 개선 |
| `docker-compose.yml` | 로그 마운트, JSON 로깅 드라이버 |
| `backend/Dockerfile` | 공유 모듈 복사, PYTHONPATH 설정 |

---

## 🔄 실행 흐름 다이어그램

```
사용자 입력 (업종, 감성, 타겟)
        ↓
[Step 1-3] Streamlit 입력 수집 → Session ID 생성
        ↓
[Step 4] 생성 시작
        ├─ generate_brand_identity() 호출
        │  ├─ Gemini API 요청
        │  ├─ 로거: "AI Raw Response" 기록
        │  └─ Tracker: 브랜드 변수 추적
        │
        ├─ generate_logo_variables() 호출
        │  ├─ Gemini API 요청
        │  ├─ JSON 파싱
        │  ├─ Tracker: brand_identity 변수 추적
        │  ├─ Tracker: logo_variables 추적
        │  └─ MOOD_MAPPING으로 자동 추천값 채우기
        │
        └─ 모든 변수를 st.session_state에 저장
        ↓
[Step 5] 결과 표시
        ├─ 브랜드 정체성 (render_result)
        └─ 🎨 로고 생성 변수 섹션
           ├─ 📋 브랜드 정체성
           ├─ 🔧 로고 변수 (모든 값 표시)
           ├─ 📊 변수 추적 정보
           └─ 💡 추천 이유

로그 저장
    ├─ logs/nametag.log (JSON)
    └─ logs/variables.jsonl (한 줄에 하나)
```

---

## 📊 로그 예시

### nametag.log (JSON 형식)
```json
{
  "timestamp": "2026-05-18T10:30:45.123456",
  "level": "INFO",
  "logger": "NameTag.BrandGenerator",
  "message": "🚀 Starting logo variable generation",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "variables": {
    "business_type": "수제 커피 구독 서비스",
    "vibes": ["따뜻 & 친근"],
    "target": "직장인 / 커피 애호가"
  }
}
```

### variables.jsonl (JSONL 형식)
```json
{"timestamp": "2026-05-18T10:30:45.123456", "session_id": "a1b2c3d4-...", "variable_name": "BRAND_NAME", "variable_value": "Brewly", "source": "ai_response"}
{"timestamp": "2026-05-18T10:30:46.234567", "session_id": "a1b2c3d4-...", "variable_name": "LOGO_TARGET_MOOD", "variable_value": "따뜻 & 친근", "source": "ai_response"}
{"timestamp": "2026-05-18T10:30:46.345678", "session_id": "a1b2c3d4-...", "variable_name": "LOGO_BRAND_COLOR", "variable_value": "#C8553D", "source": "auto_inferred"}
```

---

## 🐳 Docker에서 로그 확인

### 기본 명령어
```bash
# 실시간 로그
docker compose logs -f backend

# 특정 세션 로그
docker compose logs backend | grep "a1b2c3d4-e5f6-7890"

# 변수 로그 보기
docker compose exec backend cat /logs/variables.jsonl
```

### 상세 분석
```bash
# JSON 형식으로 정렬
docker compose exec backend \
  cat /logs/nametag.log | jq '.'

# 에러만 필터링
docker compose exec backend \
  cat /logs/nametag.log | jq '.[] | select(.level == "ERROR")'

# 변수별 로그 분석
docker compose exec backend \
  cat /logs/variables.jsonl | jq '.[] | select(.variable_name == "LOGO_BRAND_COLOR")'
```

---

## 🎯 로고 변수 생성 예시

**사용자 입력:**
```
업종: "수제 커피 구독 서비스"
감성: "따뜻 & 친근"
타겟: "직장인 / 커피 애호가"
```

**AI 응답 (추적됨):**
```json
{
  "brand_identity": {
    "brand_name": "Brewly",
    "brand_name_meaning": "Brew(양조)와 Friendly의 합성. 따뜻하고 친근한 커피 경험",
    "brand_topic": "수제 커피 구독 서비스 - 매주 다른 원두와 로스팅 방식 제공",
    "core_value": "신뢰와 품질, 따뜻한 경험",
    "slogan": "매주 새로운 맛의 만남"
  },
  "logo_variables": {
    "target_mood": "따뜻 & 친근",
    "brand_color": "#C8553D",
    "font_style": "부드러운 산세리프",
    "symbol_type": "유기적",
    "logo_type": "심볼+텍스트 조합",
    "background": "흰색"
  },
  "recommendations_reason": "테라코타 색상은 커피의 따뜻함을 표현하고, 유기적 심볼은 자연스러운 커피 원두를 나타냅니다."
}
```

**자동 매핑 (무드 기반):**
```
TARGET_MOOD = "따뜻 & 친근" → MOOD_MAPPING 참고
├─ BRAND_COLOR: #C8553D (테라코타)
├─ FONT_STYLE: 부드러운 산세리프
└─ SYMBOL_TYPE: 유기적 곡선
```

---

## 📈 추적 가능한 정보

### 1. 모든 변수의 값
```bash
docker compose exec backend \
  grep "variable_value" /logs/variables.jsonl | jq '.variable_value'
```

### 2. 변수의 출처 (ai_response vs auto_inferred)
```bash
docker compose exec backend \
  grep '"source"' /logs/variables.jsonl | jq '.source' | sort | uniq -c
```

### 3. 세션 duration
```bash
docker compose exec backend \
  grep "Starting logo variable generation\|Generation completed" /logs/nametag.log | \
  jq -r '.timestamp'
```

### 4. AI 응답 추적
```bash
docker compose exec backend \
  grep "AI Raw Response\|JSON 파싱 실패" /logs/nametag.log
```

---

## 🔐 보안 고려사항

- 로그 파일에는 민감한 정보 미포함
- Docker 볼륨으로 로그 격리
- Session ID로 사용자 세션 추적 가능

---

## ✅ 체크리스트: 구현된 요구사항

- [x] 매우 상세한 로그 생성
- [x] AI 응답 추적 및 기록
- [x] 변수별 값 로깅
- [x] 로고 생성에 필요한 모든 변수 AI로부터 받기
- [x] 변수들을 로고에 작성할 수 있도록 UI 구성
- [x] 무드 기반 자동 추천 값 설정
- [x] Docker에서 로그 확인 가능
- [x] 실시간 로그 추적 가능

---

## 🚀 다음 단계 (선택사항)

1. **로고 생성 API 통합** - `generate_logo_variables`에서 받은 변수로 실제 로고 생성
2. **로그 시각화** - Grafana/ELK Stack으로 로그 대시보드 구성
3. **변수 내보내기** - 생성된 변수를 JSON/CSV로 다운로드
4. **A/B 테스팅** - 여러 변수 조합으로 로고 생성 비교
5. **캐싱** - 동일한 입력에 대한 캐시 로그

---

## 📚 참고 문서
- [상세 로깅 가이드](LOGGING_GUIDE.md)
- [프롬프트 시스템](Prompt/네임텍%20로고%20캐릭터%20생성%20프롬프트.md)
- [Docker 설정](docker-compose.yml)
