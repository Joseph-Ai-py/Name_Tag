# 상세 로깅 & 변수 추적 시스템 가이드

## 🎯 개요
NameTag에 구축된 고급 로깅 시스템은 로고 생성 과정의 모든 변수를 추적하고 AI 응답을 기록합니다.

---

## 📊 로그 파일 위치

```
logs/
├── nametag.log          # 모든 로그 (JSON 형식)
└── variables.jsonl      # 변수별 추적 로그 (한 줄에 하나)
```

### 1. `nametag.log` - 전체 로그
- **형식**: JSON (한 줄에 하나의 JSON 객체)
- **내용**: 모든 시스템 로그, AI 응답, 변수 변경
- **용도**: 전체 실행 흐름 추적

**예시:**
```json
{
  "timestamp": "2026-05-18T10:30:45.123456",
  "level": "INFO",
  "logger": "NameTag.BrandGenerator",
  "message": "🚀 Starting logo variable generation",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "variables": {"BRAND_NAME": "Brewly", "BRAND_TOPIC": "수제 커피 구독"}
}
```

### 2. `variables.jsonl` - 변수 추적 로그
- **형식**: JSONL (한 줄에 하나)
- **내용**: 모든 변수의 이름, 값, 출처
- **용도**: 특정 변수의 생성 과정 추적

**예시:**
```json
{"timestamp": "2026-05-18T10:30:45.123456", "session_id": "a1b2c3d4-...", "variable_name": "BRAND_NAME", "variable_value": "Brewly", "source": "ai_response"}
{"timestamp": "2026-05-18T10:30:46.234567", "session_id": "a1b2c3d4-...", "variable_name": "LOGO_TARGET_MOOD", "variable_value": "모던 & 신뢰", "source": "ai_response"}
{"timestamp": "2026-05-18T10:30:46.345678", "session_id": "a1b2c3d4-...", "variable_name": "LOGO_BRAND_COLOR", "variable_value": "#333333", "source": "auto_inferred"}
```

---

## 🐳 Docker에서 로그 확인

### 1. 실시간 로그 보기
```bash
# 백엔드 로그만 보기
docker compose logs -f backend

# 모든 서비스 로그 보기
docker compose logs -f

# 마지막 50줄만 보기
docker compose logs --tail=50 backend
```

### 2. 로그 파일 직접 접근
```bash
# Docker 컨테이너 내부의 로그 파일 보기
docker compose exec backend cat /logs/nametag.log

# 실시간 추적
docker compose exec backend tail -f /logs/nametag.log

# 변수별 로그만 보기
docker compose exec backend cat /logs/variables.jsonl | jq '.'
```

### 3. 로그 필터링 및 분석
```bash
# 특정 세션의 로그만 보기
docker compose exec backend grep "세션ID" /logs/nametag.log

# ERROR 레벨 로그만 보기
docker compose exec backend grep '"level": "ERROR"' /logs/nametag.log

# JSON 형식으로 보기 (jq 필요)
docker compose exec backend cat /logs/nametag.log | jq '.[] | select(.level == "ERROR")'
```

---

## 🔍 로그 추적 변수 종류

### 브랜드 정체성 변수
| 변수명 | 설명 | 출처 |
|------|------|------|
| `BRAND_NAME` | 브랜드명 | ai_response |
| `BRAND_BRAND_NAME_MEANING` | 브랜드명의 의미 | ai_response |
| `BRAND_BRAND_TOPIC` | 사업 주제 | ai_response |
| `BRAND_CORE_VALUE` | 핵심 가치 | ai_response |
| `BRAND_SLOGAN` | 슬로건 | ai_response |

### 로고 생성 변수
| 변수명 | 설명 | 출처 |
|------|------|------|
| `LOGO_TARGET_MOOD` | 브랜드 감성 | ai_response |
| `LOGO_BRAND_COLOR` | 브랜드 색상 | ai_response 또는 auto_inferred |
| `LOGO_FONT_STYLE` | 폰트 스타일 | ai_response 또는 auto_inferred |
| `LOGO_SYMBOL_TYPE` | 심볼 스타일 | ai_response 또는 auto_inferred |
| `LOGO_LOGO_TYPE` | 로고 구성 방식 | ai_response |
| `LOGO_BACKGROUND` | 배경색 | ai_response |

### 변수 출처 (Source)
- **ai_response**: AI가 직접 추천한 값
- **auto_inferred**: 무드 테이블에서 자동 매핑된 값
- **user**: 사용자가 직접 입력한 값
- **system**: 시스템에서 설정한 값

---

## 📱 Streamlit UI에서 로그 확인

### 1. Session ID 확인
- 좌측 사이드바에 현재 세션 ID 표시
- 이 ID로 Docker 로그에서 해당 세션 검색 가능

### 2. 로고 변수 섹션
결과 화면 하단에 다음 섹션 표시:
- **📋 브랜드 정체성**: 추천된 브랜드명, 주제, 가치 등
- **🔧 로고 변수**: 모든 로고 생성 변수와 값
- **📊 변수 추적 정보**: JSON 형식의 전체 변수 정보
- **💡 추천 이유**: AI가 이 변수들을 추천한 이유

---

## 🎬 실제 사용 예시

### 시나리오: "커피 구독 서비스" 브랜드 만들기

1. **Streamlit 앱에서 입력**
   - 업종: "수제 커피 구독 서비스"
   - 감성: "따뜻 & 친근"
   - 타겟: "직장인 / 커피 애호가"

2. **생성 시작**
   - Streamlit: Session ID 기록 (e.g., `a1b2c3d4-...`)

3. **Docker 로그 모니터링**
   ```bash
   docker compose logs -f backend | grep "a1b2c3d4"
   ```

4. **결과 확인**
   - Streamlit에서 로고 변수 섹션 펼치기
   - 모든 변수와 값 확인

5. **상세 분석 (Docker)**
   ```bash
   # 이 세션의 모든 변수 추적
   docker compose exec backend grep "a1b2c3d4" /logs/variables.jsonl
   
   # JSON 형식으로 보기
   docker compose exec backend grep "a1b2c3d4" /logs/variables.jsonl | jq '.'
   ```

---

## 🛠️ 로그 관리

### 로그 파일 크기 확인
```bash
ls -lh logs/
```

### 로그 정리
```bash
# 모든 로그 삭제 (주의!)
rm logs/*.log logs/*.jsonl

# 또는 docker 컨테이너에서
docker compose exec backend rm -f /logs/nametag.log /logs/variables.jsonl
```

### 로그 백업
```bash
# 로그 파일 로컬에 복사
docker compose cp backend:/logs/nametag.log ./nametag.log.backup
docker compose cp backend:/logs/variables.jsonl ./variables.jsonl.backup
```

---

## 📈 성능 모니터링

### 실행 시간 측정
```bash
# 생성 시작과 완료 사이 시간 계산
docker compose exec backend \
  grep "Starting logo variable generation\|Logo variables generated successfully" /logs/nametag.log \
  | jq -r '.timestamp'
```

### 에러 추적
```bash
# 모든 에러 찾기
docker compose logs backend | grep -i error

# JSON 형식으로
docker compose exec backend grep '"level": "ERROR"' /logs/nametag.log | jq '.'
```

---

## 🔐 로그 분석 팁

### 변수 검증
```bash
# 특정 변수의 값이 예상과 맞는지 확인
docker compose exec backend \
  grep "LOGO_BRAND_COLOR" /logs/variables.jsonl | \
  jq '.variable_value'
```

### AI 응답 추적
```bash
# AI 응답이 정상적으로 파싱되었는지 확인
docker compose exec backend \
  grep "Variables extracted\|JSON 파싱 실패" /logs/nametag.log
```

### 무드별 자동 매핑 확인
```bash
# auto_inferred 변수만 보기
docker compose exec backend \
  grep '"source": "auto_inferred"' /logs/variables.jsonl | \
  jq '.'
```

---

## 🚀 개발 팁

### 로컬 개발 환경에서 로그 확인
```python
# Python 코드에서
from utils.logger import get_logger, get_tracker

logger = get_logger("MyModule")
logger.info("📝 로그 메시지")

# 변수 추적
tracker = get_tracker("session-id")
tracker.set_variable("MY_VAR", "value", source="user")
```

### 커스텀 로그 추가
```python
# step 로깅
tracker.log_step("my_step", {
    "input": "value",
    "output": "result"
})

# 세션 로그 내보내기
session_log = tracker.export_session_log()
```

---

## 📞 트러블슈팅

| 문제 | 해결책 |
|------|--------|
| 로그 파일이 없음 | `mkdir -p logs/` 실행 |
| 로그 파일이 너무 큼 | `rm logs/*.log` 로 초기화 |
| Docker에서 로그 안 보임 | `docker compose logs --no-log-prefix backend` |
| 변수가 기록되지 않음 | logger 초기화 확인, Python path 확인 |

---

## 📚 관련 문서
- [변수 시스템](../Prompt/네임텍%20로고%20캐릭터%20생성%20프롬프트.md)
- [Docker 설정](docker-compose.yml)
- [로거 구현](utils/logger.py)
