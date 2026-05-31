# 🏷️ Name Tag — 개발 플랜 & VS Code Copilot 프롬프트 가이드

> **총 기간:** 52주 (약 13개월) | **개발자:** 1인 기준 (하루 4~6시간)
> **LLM:** `gemini-3-flash-preview` | **이미지 생성:** `gemini-3.1-flash-image-preview`

---

## 📌 Copilot 사용법

VS Code에서 `Ctrl+Shift+I` → Copilot Chat 열기
각 일차의 **Copilot 프롬프트** 블록을 그대로 복붙해서 사용하세요.

---

## 🛠️ 기술 스택

```
언어:          Python 3.11 / TypeScript
LLM:           Google Gemini API — gemini-3-flash-preview
이미지 생성:    Google Gemini API — gemini-3.1-flash-image-preview
프론트 (초기):  Streamlit 1.35
프론트 (이후):  React 18 + Tailwind CSS
백엔드:         FastAPI
DB:             PostgreSQL + SQLAlchemy + Alembic
인증:           Supabase Auth
결제:           Stripe + Stripe Connect
캐싱:           Redis
저장소:         AWS S3 / Cloudflare R2
PDF 생성:       WeasyPrint + Jinja2
배포:           Vercel (프론트) + Railway (백엔드)
분석:           PostHog + Google Analytics
이메일:         Resend
테스트:         pytest + React Testing Library
```

---

## 🗓️ 전체 마일스톤

| 마일스톤 | 일차 | 내용 |
|---------|------|------|
| ✅ M0 | 15일차 | 개발 환경 완성 + CI/CD 동작 |
| ✅ M1 | 50일차 | 패키지 A Streamlit MVP 베타 배포 |
| ✅ M2 | 100일차 | React 전환 + 회원/저장 기능 |
| ✅ M3 | 150일차 | Stripe 구독 결제 → 수익 발생 |
| ✅ M4 | 225일차 | 패키지 B·C·D 가이드 제안서 출시 |
| ✅ M5 | 260일차 | B2B 중개 플랫폼 완성 |

---

# PHASE 0 — 환경 세팅 & 구조 확립
### 📆 1일차 ~ 15일차 (3주)

---

## WEEK 1 — 개발 환경 세팅 (1일차 ~ 5일차)

---

### 📅 1일차
**목표:** GitHub 레포 생성 + 브랜치 전략 확립
**태스크:** 레포 초기화, 브랜치 규칙 설정, README 초안

```
Copilot 프롬프트:

GitHub 레포지토리를 새로 만들고 있어. 아래 조건에 맞는 초기 세팅 파일들을 만들어줘.

프로젝트: Name Tag (AI 브랜딩 플랫폼)
언어: Python 3.11, 이후 TypeScript 추가 예정

만들어줄 파일:
1. .gitignore (Python + Node + 환경변수 파일 제외)
2. README.md (프로젝트 개요, 로컬 실행 방법, 기술 스택 표 포함)
3. .github/copilot-instructions.md (LLM: gemini-3-flash-preview, 이미지: gemini-3.1-flash-image-preview 명시)

브랜치 전략도 README에 포함해줘:
- main: 배포용
- dev: 개발 통합
- feature/기능명: 기능 개발
```

---

### 📅 2일차
**목표:** Python 환경 + 의존성 관리 설정
**태스크:** requirements.txt 작성, 가상환경 구성, 핵심 패키지 설치

```
Copilot 프롬프트:

Python 3.11 프로젝트의 requirements.txt를 작성해줘.
아래 패키지들을 버전 고정해서 정리해줘:

필수 (requirements.txt):
- streamlit==1.35.0
- google-generativeai (최신 버전)
- python-dotenv
- fastapi
- uvicorn
- sqlalchemy
- alembic
- psycopg2-binary
- redis
- tenacity
- boto3
- Pillow
- weasyprint
- stripe
- ruff

dev only (requirements-dev.txt):
- pytest
- pytest-mock
- httpx

requirements.txt와 requirements-dev.txt로 분리해줘.
```

---

### 📅 3일차
**목표:** 폴더 구조 확립
**태스크:** 전체 프로젝트 디렉터리 구조 생성 + 각 파일 역할 정의

```
Copilot 프롬프트:

Name Tag 프로젝트의 폴더 구조를 만들어줘.
아래 구조로 빈 파일들을 생성하고, 각 파일 상단에 역할 주석을 달아줘.

nametag/
├── app.py                     # Streamlit 메인 진입점
├── .env.example               # 환경변수 템플릿
├── components/
│   ├── __init__.py
│   ├── step_input.py          # Step 1: 업종 입력
│   ├── step_vibe.py           # Step 2: 감성 선택
│   ├── step_target.py         # Step 3: 타겟 고객
│   └── result_view.py         # 결과 화면
├── services/
│   ├── __init__.py
│   ├── brand_generator.py     # Gemini API 텍스트 생성
│   └── image_generator.py     # Gemini 이미지 생성
├── utils/
│   ├── __init__.py
│   └── parser.py              # JSON 파싱 유틸
└── tests/
    ├── __init__.py
    ├── test_brand_generator.py
    └── test_parser.py

각 __init__.py에는 모듈 설명 docstring을 넣어줘.
```

---

### 📅 4일차
**목표:** .env 관리 체계 + Gemini API 키 연결 테스트
**태스크:** 환경변수 로딩 구조 작성, API 연결 확인 스크립트

```
Copilot 프롬프트:

아래 환경변수를 관리하는 config.py 파일을 만들어줘.
파일 위치: nametag/config.py

필요한 환경변수:
- GOOGLE_API_KEY (Gemini API)
- SUPABASE_URL
- SUPABASE_KEY
- DATABASE_URL (PostgreSQL)
- REDIS_URL
- STRIPE_SECRET_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- S3_BUCKET_NAME

조건:
- python-dotenv로 .env 파일 로딩
- 환경변수 없으면 명확한 에러 메시지 출력
- 개발/운영 환경 분리 (ENV=dev|prod)
- 타입 힌트 포함

그리고 scripts/test_api_connection.py 파일도 만들어줘.
Gemini API (gemini-3-flash-preview) 연결이 정상인지 확인하는 테스트 스크립트.
```

---

### 📅 5일차
**목표:** GitHub Actions CI 파이프라인 구성
**태스크:** push 시 자동 lint + test 실행 워크플로우

```
Copilot 프롬프트:

GitHub Actions 워크플로우 파일을 만들어줘.
파일 위치: .github/workflows/ci.yml

동작 조건: main, dev 브랜치로 push 또는 PR 생성 시

실행 순서:
1. Python 3.11 환경 세팅
2. pip install -r requirements-dev.txt
3. ruff check . (린트 검사, 실패 시 중단)
4. pytest tests/ -v (테스트 실행)

추가 조건:
- 환경변수는 GitHub Secrets에서 주입 (GOOGLE_API_KEY 등)
- 테스트 실패 시 Slack 알림 (webhook URL은 SLACK_WEBHOOK secret으로)
- 캐싱: pip 캐시 적용해서 속도 개선
```

**🔖 주간 회고:**
- [ ] GitHub 레포 생성
- [ ] requirements.txt 버전 고정
- [ ] 폴더 구조 완성
- [ ] .env 환경변수 로딩 확인
- [ ] CI 파이프라인 동작 확인

---

## WEEK 2 — 프로젝트 구조 확립 (6일차 ~ 10일차)

---

### 📅 6일차
**목표:** Streamlit 앱 뼈대 + 세션 상태 초기화
**태스크:** app.py 메인 구조 + init_session() 함수

```
Copilot 프롬프트:

Streamlit 앱의 메인 파일 app.py를 작성해줘.

조건:
- 세션 상태 초기화 함수 init_session() 작성
  관리할 상태: step(1~5), business_type, keywords, selected_vibes(list),
               target, result(dict), selected_brand(int), error
- 5단계 진행 바 render_progress(step) 함수:
  단계: 업종입력 / 감성선택 / 타겟고객 / 생성중 / 결과
  현재 단계는 볼드, 완료 단계는 취소선, 미완료는 회색
- step 값에 따라 컴포넌트 분기하는 메인 렌더링 로직
- st.set_page_config: 타이틀 "Name Tag · 패키지 A", 아이콘 🏷️, layout="centered"

기술: Streamlit 1.35, Python 3.11, 타입 힌트 포함
```

---

### 📅 7일차
**목표:** pytest 테스트 기반 구축
**태스크:** brand_generator.py 단위 테스트 + mock 설정

```
Copilot 프롬프트:

tests/test_brand_generator.py 파일을 작성해줘.

테스트 대상: nametag/services/brand_generator.py의 generate_brand_identity() 함수

테스트 케이스:
1. test_normal_input: 정상 입력 → dict 반환 (brands, typography, character 키 포함)
2. test_json_extraction_codeblock: ```json ... ``` 형식 응답 파싱
3. test_json_extraction_plain: 순수 JSON 텍스트 파싱
4. test_missing_key_raises: 필수 키 누락 시 ValueError 발생
5. test_empty_response_raises: 빈 응답 시 에러 처리
6. test_extract_json_fallback: 텍스트 앞뒤에 설명이 붙은 경우도 파싱 성공

Gemini API 호출은 pytest-mock으로 mock 처리해줘.
conftest.py에 공통 fixture 분리.
```

---

### 📅 8일차
**목표:** utils/parser.py 완성
**태스크:** JSON 추출 함수 3단계 방어 로직

```
Copilot 프롬프트:

nametag/utils/parser.py 파일을 완성해줘.

핵심 함수: extract_json(text: str) -> dict | None

3단계 추출 전략:
1. 코드블록 안 JSON 추출: ```json ... ``` 패턴 정규식
2. 텍스트에서 { } 가장 바깥 JSON 추출: text.find('{') ~ text.rfind('}')
3. 전체 텍스트 직접 json.loads() 시도

각 단계 실패 시 다음 단계로 넘어가고, 모두 실패 시 None 반환.

추가 함수:
- validate_brand_result(data: dict) -> bool
  필수 키: brands(list, 3개), typography(dict), character(dict) 검증

모든 함수에 docstring + 타입 힌트 포함.
pytest 테스트도 tests/test_parser.py에 함께 작성해줘.
```

---

### 📅 9일차
**목표:** 린트 설정 + 코드 스타일 통일
**태스크:** ruff 설정, pre-commit hooks 구성

```
Copilot 프롬프트:

Python 코드 품질 관리 도구를 설정해줘.

1. pyproject.toml에 ruff 설정 추가:
   - line-length: 100
   - target-version: py311
   - 활성화 규칙: E, W, F, I (isort 포함)
   - 제외 폴더: migrations/, .venv/

2. .pre-commit-config.yaml 작성:
   - ruff check --fix 자동 실행
   - trailing whitespace 제거
   - 파일 끝 newline 추가
   - Python 디버그 구문(breakpoint, pdb) 커밋 방지

3. Makefile 작성:
   - make lint: ruff check
   - make test: pytest -v
   - make run: streamlit run app.py
   - make clean: __pycache__ 삭제
```

---

### 📅 10일차
**목표:** Week 2 통합 점검 + 문서화
**태스크:** 전체 코드 lint 통과, README 업데이트

```
Copilot 프롬프트:

현재까지 작성된 nametag/ 프로젝트 전체를 점검해줘.

점검 항목:
1. 모든 Python 파일에 타입 힌트가 있는지 확인
2. 모든 public 함수에 docstring이 있는지 확인
3. __init__.py에 __all__ 목록이 정의되어 있는지
4. import 순서가 ruff 기준에 맞는지

README.md 업데이트:
- 로컬 개발 환경 세팅 방법 (단계별)
- 환경변수 설정 방법 (.env.example 기반)
- 테스트 실행 방법
- 브랜치 전략
```

---

## WEEK 3 — 마무리 & QA (11일차 ~ 15일차)

---

### 📅 11일차
**목표:** 전체 구조 최종 점검 + 누락 파일 보완

```
Copilot 프롬프트:

nametag 프로젝트에 아래 파일들이 빠져있는지 확인하고 생성해줘.

1. .env.example — 모든 환경변수 키를 빈 값으로 정리한 템플릿
2. CONTRIBUTING.md — 기여 가이드 (브랜치 네이밍, 커밋 메시지 규칙)
3. scripts/seed_test_data.py — 개발용 테스트 데이터 생성 스크립트
4. docs/architecture.md — 시스템 구조 다이어그램 (ASCII)

커밋 메시지 규칙 (Conventional Commits):
feat: 기능 추가 / fix: 버그 수정 / docs: 문서
test: 테스트 / refactor: 리팩터링 / chore: 빌드/설정
```

---

### 📅 12일차
**목표:** CI 파이프라인 실제 동작 검증

```
Copilot 프롬프트:

GitHub Actions CI가 올바르게 동작하는지 확인하기 위한 검증 태스크를 도와줘.

1. tests/ 폴더의 모든 테스트를 pytest -v로 실행했을 때 예상 통과 목록
2. 현재 테스트 커버리지가 낮은 부분 분석 (아직 구현 안 된 부분 제외)
3. ruff check . 실행 결과 예상 경고 미리 수정
4. CI 워크플로우에서 secrets 없이도 lint+test 통과하게 분리
```

---

### 📅 13일차
**목표:** 개발 환경 문서화 완료

```
Copilot 프롬프트:

신규 개발자가 처음 클론했을 때 30분 안에 로컬 실행이 가능하도록
onboarding 체크리스트를 만들어줘. 파일: docs/onboarding.md

포함 내용:
1. 사전 요구사항 (Python 3.11, Git, VS Code)
2. 레포 클론 + 가상환경 생성
3. 패키지 설치
4. .env 파일 설정 (각 환경변수 어디서 발급받는지 링크 포함)
   - Google AI Studio (GOOGLE_API_KEY)
   - Supabase 대시보드
   - Stripe 대시보드
5. 로컬 실행 명령어
6. 첫 테스트 실행 확인
7. 자주 발생하는 에러 & 해결법 FAQ
```

---

### 📅 14일차
**목표:** Phase 0 최종 정리 + Phase 1 준비

```
Copilot 프롬프트:

Phase 1 Streamlit UI 개발을 시작하기 전에 준비 작업을 도와줘.

1. components/step_input.py의 함수 시그니처 설계
   - render_step1() → None
   - can_proceed_step1() → bool

2. services/brand_generator.py 스켈레톤 작성
   - generate_brand_identity(business_type, vibes, target, keywords) -> dict
   - gemini-3-flash-preview 모델 사용
   - 타입 힌트 + docstring만 (실제 구현은 비워둠)

3. 결과 데이터 구조를 TypedDict로 정의
   - BrandOption: name, meaning, story, slogan
   - Typography: korean, english, reason
   - Character: name, concept, personality, visual
   - BrandResult: brands(list), typography, character
```

---

### 📅 15일차

**🏁 마일스톤 M0 달성 — 개발 환경 완성**

```
Copilot 프롬프트:

Phase 0 완료 체크리스트를 확인해줘.

- [ ] GitHub Actions CI 정상 동작 (lint + test 통과)
- [ ] 폴더 구조 완성 (모든 __init__.py 존재)
- [ ] .env.example 완성
- [ ] README 로컬 실행 가이드 완성
- [ ] pytest 기본 테스트 5개 이상 통과
- [ ] ruff 경고 0개
- [ ] 커밋 히스토리 정리

부족한 항목이 있으면 오늘 안에 처리할 수 있는 우선순위를 잡아줘.
```

---

# PHASE 1 — 패키지 A Streamlit MVP
### 📆 16일차 ~ 50일차 (7주)

---

## WEEK 4 — Step 1·2·3 UI (16일차 ~ 20일차)

---

### 📅 16일차
**목표:** Step 1 — 업종 입력 화면 완성
**태스크:** components/step_input.py 완성

```
Copilot 프롬프트:

nametag/components/step_input.py를 완성해줘.

함수: render_step1() -> None

UI 구성:
1. 제목: "어떤 업종 · 서비스인가요?"
2. 설명: "구체적일수록 더 정확한 브랜드를 만들 수 있어요"
3. st.text_input — business_type
   placeholder 5가지 예시 중 랜덤:
   "20대를 위한 감성 소품 온라인 셀렉샵", "동네 수제 베이커리",
   "IT 프리랜서 1인 스튜디오", "반려동물 간식 브랜드", "홈트레이닝 코칭 서비스"
4. st.text_input — keywords (선택)
   placeholder: "예: 따뜻함, 일상, 발견 (쉼표로 구분)"
5. "다음 →" 버튼 — business_type 2글자 미만이면 disabled

모든 입력은 st.session_state에 즉시 저장.
버튼 클릭 시 step=2로 변경 후 st.rerun().
```

---

### 📅 17일차
**목표:** Step 2 — 감성 태그 선택 화면
**태스크:** components/step_vibe.py 완성

```
Copilot 프롬프트:

nametag/components/step_vibe.py를 완성해줘.

함수: render_step2() -> None

UI 구성:
1. 제목: "브랜드 감성을 선택해주세요"
2. 설명: "최대 4개까지, 이 감성이 브랜드 이름과 스토리에 반영됩니다"
3. 감성 태그 목록 (3열 체크박스 그리드):
   따뜻한, 차가운, 모던한, 클래식한, 자연친화적, 럭셔리한,
   미니멀한, 활기찬, 유머러스한, 진지한, 감성적인, 신뢰감있는, 트렌디한, 레트로한
4. 선택 수 실시간 표시: "2 / 4개 선택됨"
5. 4개 초과 선택 시도 시 st.warning (선택 막기)
6. 이전/다음 버튼 (selected_vibes 1개 이상이면 다음 활성화)

모든 상태는 st.session_state.selected_vibes 리스트로 관리.
```

---

### 📅 18일차
**목표:** Step 3 — 타겟 고객 입력 화면
**태스크:** components/step_target.py 완성

```
Copilot 프롬프트:

nametag/components/step_target.py를 완성해줘.

함수: render_step3() -> None

UI 구성:
1. 제목: "주요 타겟 고객은 누구인가요?"
2. 설명: "나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요"
3. 에러 메시지 영역 (st.session_state.error가 있으면 st.error로 표시)
4. st.text_area — target (height=120)
   placeholder: "예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들"
5. 이전 버튼 / "✦ 브랜드 생성" 버튼 (target 2글자 이상이면 활성화)

"✦ 브랜드 생성" 클릭 시:
- st.session_state.step = 4
- st.session_state.error = None
- st.rerun()
```

---

### 📅 19일차
**목표:** 진행 바 + 앱 메인 라우팅 완성
**태스크:** app.py 완성 (render_progress + 분기 로직)

```
Copilot 프롬프트:

nametag/app.py를 완성해줘.

함수 1: render_progress(current_step: int) -> None
- 5단계 진행 표시, st.columns(5)로 구성
- 단계 레이블: ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "완성"]
- 완료 단계: ~~취소선~~ / 현재 단계: **볼드** / 미완료: 회색

메인 로직:
- init_session() 호출
- 헤더: "🏷️ NAMETAG · 패키지 A"
- 서브타이틀: "나만의 브랜드 정체성 만들기"
- st.divider()
- render_progress(st.session_state.step)
- st.divider()
- step 값에 따라 render_step1() ~ run_generation() ~ render_result() 분기

from components 임포트 구조도 포함해줘.
```

---

### 📅 20일차
**목표:** 로컬 실행 + UI 흐름 전체 테스트

```
Copilot 프롬프트:

현재 Streamlit 앱을 로컬에서 실행했을 때 UI 흐름을 점검해줘.

점검 시나리오:
1. 앱 실행 → Step 1 화면 정상 표시
2. 빈 입력으로 "다음" 클릭 → 버튼 비활성화 확인
3. 업종 입력 후 "다음" → Step 2 이동
4. 감성 5개 선택 시도 → 경고 메시지 확인
5. 감성 1개 이상 선택 → "다음" 활성화
6. Step 3에서 "이전" → Step 2로 돌아가기
7. "브랜드 생성" 클릭 → Step 4(로딩)으로 이동

위 시나리오에서 발생할 수 있는 버그를 예측하고 방어 코드를 미리 작성해줘.
```

---

## WEEK 5 — Gemini API 텍스트 생성 (21일차 ~ 25일차)

---

### 📅 21일차
**목표:** brand_generator.py — Gemini API 텍스트 생성 구현

```
Copilot 프롬프트:

nametag/services/brand_generator.py를 완성해줘.

사용 모델: gemini-3-flash-preview (google-generativeai 패키지)
함수: generate_brand_identity(business_type, vibes, target, keywords) -> dict

시스템 프롬프트:
"당신은 전문 브랜드 디렉터입니다. 사용자의 정보를 바탕으로
초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다.
반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."

JSON 구조 요청:
{
  "brands": [{"name","meaning","story","slogan"} × 3],
  "typography": {"korean","english","reason"},
  "character": {"name","concept","personality","visual"}
}

응답은 utils/parser.py의 extract_json()으로 파싱.
validate_brand_result()로 검증. 실패 시 ValueError 발생.
google.generativeai 초기화, 모델 호출, 에러 처리 포함.
```

---

### 📅 22일차
**목표:** API 응답 캐싱 + 재시도 로직
**태스크:** @st.cache_data 적용 + 타임아웃 처리

```
Copilot 프롬프트:

brand_generator.py에 아래 기능을 추가해줘.

1. Streamlit 캐싱 적용:
   @st.cache_data(show_spinner=False)
   def cached_generate(business_type, vibes_tuple, target, keywords):
   - vibes는 tuple로 받아야 해시 가능
   - 캐시 TTL: 1시간

2. 재시도 로직 (tenacity 라이브러리):
   - 최대 3회 재시도
   - 재시도 간격: 2초, 4초, 8초 (exponential backoff)
   - 재시도 대상: APIError, TimeoutError

3. 타임아웃 설정:
   - API 호출 최대 30초
   - 초과 시 TimeoutError 발생
```

---

### 📅 23일차
**목표:** Step 4 — 로딩 화면 구현

```
Copilot 프롬프트:

nametag/components/loading_view.py를 만들어줘.

함수: run_generation() -> None

이 함수는 Step 4에서 호출되어:
1. st.spinner("브랜드 정체성을 설계하고 있어요...")
2. st.progress()로 4단계 진행 표시:
   - 25%: "업종 · 키워드 분석 중"
   - 50%: "브랜드 네임 도출 중"
   - 75%: "스토리텔링 작성 중"
   - 100%: "서체 · 캐릭터 설계 중"
3. 진행 메시지 변경마다 0.5초 딜레이

내부에서:
- services/brand_generator.py의 cached_generate() 호출
- 성공: st.session_state.result = result, step = 5
- 실패: st.session_state.error = 에러 메시지, step = 3
- st.rerun()

"예상 소요 시간: 10~15초" 안내 문구 포함.
```

---

### 📅 24일차
**목표:** API 연동 통합 테스트

```
Copilot 프롬프트:

Gemini API 연동 통합 테스트를 작성해줘.
파일: tests/test_integration.py

테스트 시나리오 (API mock 사용):
1. 정상 플로우: 입력 → generate_brand_identity() → dict 반환
2. API 타임아웃: TimeoutError → 재시도 3회 후 ValueError
3. JSON 파싱 실패: 잘못된 응답 → extract_json 3단계 시도
4. 네트워크 에러: ConnectionError → 에러 메시지 반환

실제 API 연결 테스트 스크립트:
scripts/test_real_api.py
- 실제 GOOGLE_API_KEY로 간단한 브랜드 생성 요청
- 응답 시간, 구조, 파싱 성공 여부 출력
```

---

### 📅 25일차
**목표:** 에러 처리 체계화

```
Copilot 프롬프트:

API 에러 종류별 사용자 메시지를 정의하고 에러 핸들링을 만들어줘.
파일: nametag/utils/error_handler.py

에러 종류별 메시지:
- TimeoutError: "응답이 지연되고 있어요. 잠시 후 다시 시도해주세요."
- ValueError (JSON 파싱): "결과 형식을 인식하지 못했어요. 다시 시도해주세요."
- ConnectionError: "네트워크 연결을 확인해주세요."
- APIError (429): "요청이 너무 많아요. 잠시 후 다시 시도해주세요."
- 기타: "알 수 없는 오류가 발생했어요. 다시 시도해주세요."

함수: handle_api_error(error: Exception) -> str
```

---

## WEEK 6 — 결과 화면 구현 (26일차 ~ 30일차)

---

### 📅 26일차
**목표:** 결과 화면 — 브랜드 네임 선택 + 스토리텔링

```
Copilot 프롬프트:

nametag/components/result_view.py를 작성해줘. (1/2)

섹션 1 — 브랜드 네임 선택:
- st.subheader("브랜드 네임 — 3가지 제안")
- st.radio로 3개 브랜드 선택 (horizontal=True)
- 선택 변경 시 st.session_state.selected_brand 업데이트

섹션 2 — 선택한 브랜드 스토리텔링:
- st.container(border=True) 안에:
  - 브랜드명 (h3 크기)
  - meaning (caption 스타일)
  - story (본문)
  - slogan (이탤릭, 따옴표 포함)

선택된 브랜드가 바뀌면 섹션 2 내용이 즉시 업데이트.
st.session_state.result["brands"][selected_brand]로 참조.
```

---

### 📅 27일차
**목표:** 결과 화면 — 서체 + 캐릭터 컨셉

```
Copilot 프롬프트:

nametag/components/result_view.py에 이어서 작성해줘. (2/2)

섹션 3 — 추천 서체:
- st.subheader("추천 서체")
- col1, col2 = st.columns(2)
  - col1: 한글 폰트명 / col2: 영문 폰트명
- 서체 선택 이유 (st.caption)

섹션 4 — 브랜드 캐릭터:
- st.subheader("브랜드 캐릭터 컨셉")
- st.container(border=True) 안에:
  - 캐릭터 이름, 컨셉, 성격, 외형 묘사

섹션 5 — 하단 버튼:
- "↺ 다시 시작하기" → 모든 session_state 초기화, step=1, st.rerun()
- "📄 PDF 저장하기" → Phase 2에서 구현, 지금은 st.info로 "곧 제공 예정" 표시
```

---

### 📅 28일차
**목표:** 전체 UI 흐름 통합 테스트 + 스타일 개선

```
Copilot 프롬프트:

현재까지 구현된 전체 Streamlit 앱 UI를 개선해줘.

개선 항목:
1. 일관된 여백: 모든 섹션 사이 st.divider() 통일
2. 모바일 레이아웃: st.columns() 비율 조정
3. 색상 일관성: 주요 CTA 버튼은 type="primary" 통일
4. 로딩 중 버튼 비활성화: st.button의 disabled 파라미터 활용
5. 세션 만료 처리: result=None인데 step=5이면 자동으로 step=1로 리셋

전체 앱을 streamlit run app.py로 실행했을 때 콘솔 경고 없도록 수정.
```

---

### 📅 29일차
**목표:** 사용성 개선 — 예시 입력 + 가이드

```
Copilot 프롬프트:

사용자 경험을 개선하는 기능들을 추가해줘.

1. 예시 자동 입력 버튼:
   Step 1에 "예시로 시작해보기" 버튼 추가
   클릭 시 랜덤 예시 데이터로 Step 1~3 자동 채우기

2. 입력 가이드 툴팁:
   각 입력 필드 옆에 st.expander("💡 작성 팁") 추가
   - 업종 팁: 구체적인 타겟과 가치 포함 예시
   - 감성 팁: 경쟁사와 반대 방향 감성 고려
   - 타겟 팁: 1명의 구체적인 고객을 상상하기

3. 글자 수 카운터:
   business_type, target 필드에 글자 수 표시 (예: "23 / 200자")
```

---

### 📅 30일차
**목표:** 코드 정리 + 테스트 커버리지 확인

```
Copilot 프롬프트:

현재까지 작성한 코드의 품질을 점검하고 리팩터링해줘.

1. components/ 폴더의 중복 코드 추출 → components/common.py로 분리
2. services/brand_generator.py 테스트 업데이트 (현재 구현에 맞게 mock 업데이트)
3. 전체 테스트 실행: pytest tests/ -v --tb=short
4. 복잡도가 높은 함수 (10줄 이상) 분리 또는 단순화 제안
```

---

## WEEK 7 — 이미지 생성 연동 (31일차 ~ 35일차)

---

### 📅 31일차
**목표:** image_generator.py — Gemini 이미지 생성 구현

```
Copilot 프롬프트:

nametag/services/image_generator.py를 작성해줘.

사용 모델: gemini-3.1-flash-image-preview (google-generativeai 패키지)

함수: generate_logo_concepts(brand_name, vibes, colors) -> list[str]
- 로고 시안 3종 생성
- 반환: 이미지 base64 문자열 리스트

함수: generate_character_image(character_name, visual_description, vibes) -> str
- 캐릭터 이미지 1종 생성
- 반환: 이미지 base64 문자열

이미지 생성 프롬프트 전략:
- 로고: "minimalist logo design, [brand_name], [vibe] style, vector art, white background"
- 캐릭터: "[visual_description], [vibe] mascot character, flat illustration"

에러 처리: 이미지 생성 실패 시 None 반환 (텍스트 결과는 유지)
```

---

### 📅 32일차
**목표:** 결과 화면에 이미지 표시 추가

```
Copilot 프롬프트:

result_view.py에 이미지 생성 결과를 표시하는 섹션을 추가해줘.

섹션 — 로고 시안:
- st.subheader("로고 시안 — AI 제안")
- st.caption("실제 로고 제작은 전문 디자이너에게 맡기세요. 방향성 참고용이에요.")
- 3개 이미지를 st.columns(3)으로 나란히 표시
- st.image()로 base64 또는 URL 표시
- 이미지 로딩 중에는 st.spinner("로고 시안 생성 중...")

섹션 — 캐릭터 이미지:
- st.subheader("캐릭터 이미지")
- 이미지 1개 (중앙 정렬, 너비 300px)

이미지 생성 실패 시:
- "이미지 생성에 실패했어요. 텍스트 컨셉을 참고해주세요." 표시
- 나머지 결과는 정상 표시
```

---

### 📅 33일차
**목표:** 이미지 생성 비동기 처리 + 캐싱

```
Copilot 프롬프트:

이미지 생성이 텍스트 생성보다 느릴 수 있어서 UX를 개선해줘.

전략: 텍스트 결과 먼저 표시 → 이미지는 별도 버튼으로

구현 방법:
1. 텍스트 생성 완료 시 step=5로 이동해서 결과 화면 즉시 표시
2. 이미지는 result_view.py 안에서 "🎨 로고 시안 생성하기" 버튼 클릭 시 생성
3. 이미지 결과는 st.session_state.images에 저장
4. @st.cache_data로 같은 브랜드 재생성 방지

이미지 캐싱 키: (brand_name, vibe_tuple) 조합 / 캐시 TTL: 24시간
```

---

### 📅 34일차
**목표:** 이미지 S3 업로드 로직 기반 코드 작성

```
Copilot 프롬프트:

생성된 이미지를 S3에 업로드하는 서비스를 만들어줘.
파일: nametag/services/storage.py

함수: upload_image(image_bytes: bytes, filename: str) -> str
- boto3로 S3 업로드
- 반환: 퍼블릭 URL (또는 presigned URL)

함수: get_image_url(key: str) -> str

환경변수: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME

로컬 개발 환경 (ENV=dev): images/ 폴더에 로컬 저장으로 fallback
운영 환경 (ENV=prod): S3 업로드
```

---

### 📅 35일차
**목표:** 이미지 생성 통합 테스트

```
Copilot 프롬프트:

이미지 생성 기능 전체를 테스트해줘.
파일: tests/test_image_generator.py

테스트:
1. test_logo_generation_mock: API mock으로 로고 3개 반환 확인
2. test_character_generation_mock: 캐릭터 이미지 반환 확인
3. test_image_generation_failure: API 실패 시 None 반환 확인
4. test_prompt_construction: 프롬프트가 올바르게 생성되는지

scripts/test_real_image_api.py:
- 실제 gemini-3.1-flash-image-preview로 테스트 이미지 1개 생성
- 성공 시 test_output.png로 저장
```

---

## WEEK 8 — 로딩 UX + 에러 처리 완성 (36일차 ~ 40일차)

---

### 📅 36일차
**목표:** 로딩 UX 전체 개선

```
Copilot 프롬프트:

Streamlit 앱의 로딩 경험을 개선해줘.

개선안:
1. loading_view.py 업데이트:
   - 애니메이션 텍스트: "." → ".." → "..." 반복 (0.3초 간격)
   - 단계별 진행 메시지를 실제 처리 단계와 동기화
   - 예상 남은 시간 표시: "약 10초 남았어요"

2. 진행 상태 저장:
   - generation_started_at = time.time() 저장
   - 30초 초과 시 타임아웃 안내

3. 취소 버튼:
   - "취소하고 처음으로" 버튼 → session_state 초기화

4. 성공 애니메이션:
   - 완료 시 st.balloons() 또는 st.success("브랜드가 완성됐어요! 🎉")
```

---

### 📅 37일차
**목표:** 전체 에러 시나리오 대응

```
Copilot 프롬프트:

앱에서 발생 가능한 모든 에러 시나리오를 정리하고 대응 로직을 완성해줘.

에러 시나리오 & 대응:
1. Gemini API 키 없음 → "API 키 설정이 필요해요" + 설정 가이드 링크
2. API 할당량 초과 → "오늘 사용량이 가득 찼어요. 내일 다시 시도해주세요."
3. JSON 파싱 3회 모두 실패 → "다른 표현으로 다시 입력해보세요." + 입력 초기화
4. 이미지 생성 실패 → 텍스트 결과는 유지, 이미지 실패 안내
5. 세션 상태 손상 → 자동 초기화 + "앱을 새로 시작합니다." 안내
6. 인터넷 연결 없음 → "네트워크 연결을 확인해주세요."

utils/error_handler.py에 모든 에러 타입과 메시지 매핑 딕셔너리로 관리.
```

---

### 📅 38일차
**목표:** Google Analytics 연동

```
Copilot 프롬프트:

Streamlit 앱에 Google Analytics를 연동해줘.
방법: Streamlit의 components.html()로 GA 스크립트 삽입
파일: nametag/analytics.py

추적할 이벤트:
- page_view: 각 step 진입 시
- generation_complete: 브랜드 생성 성공 시 (duration_seconds 포함)
- generation_error: 에러 발생 시
- image_generated: 이미지 생성 완료 시
- restart: 다시 시작하기 클릭 시

환경변수: GA_MEASUREMENT_ID
개발 환경 (ENV=dev)에서는 GA 비활성화
```

---

### 📅 39일차
**목표:** 베타 피드백 수집 폼 연동

```
Copilot 프롬프트:

결과 화면 하단에 베타 피드백 수집 UI를 추가해줘.

위치: result_view.py 맨 아래

UI:
st.expander("💬 이 결과가 도움이 됐나요?") 안에:
1. 별점 (1~5): st.slider
2. 좋았던 점 (선택): st.multiselect
   옵션: ["네이밍이 마음에 들어요", "스토리가 좋아요", "서체 추천이 유용해요",
          "캐릭터 컨셉이 좋아요", "이미지가 도움됐어요"]
3. 개선 의견 (선택): st.text_area (50자 이내)
4. 제출 버튼

제출 시 로컬 CSV 파일에 누적 저장 (Phase 2 전까지).
파일: services/feedback.py
```

---

### 📅 40일차
**목표:** 코드 최종 정리 + Streamlit Cloud 배포 준비

```
Copilot 프롬프트:

Streamlit Cloud 배포를 위한 준비를 도와줘.

1. .streamlit/config.toml 작성:
   - 테마 설정 (primaryColor, backgroundColor, font)
   - 서버 설정 (maxUploadSize, maxMessageSize)

2. .streamlit/secrets.toml.example 작성:
   GOOGLE_API_KEY = ""
   GA_MEASUREMENT_ID = ""
   S3_BUCKET_NAME = ""

3. requirements.txt 최종 점검:
   - 버전 충돌 없는지 확인
   - Streamlit Cloud에서 지원하는 패키지인지 확인

4. app.py 상단에 환경 체크:
   필수 환경변수 없으면 st.error + st.stop() 처리
```

---

## WEEK 9 — 배포 & QA (41일차 ~ 45일차)

---

### 📅 41일차
**목표:** Streamlit Cloud 실제 배포

```
Copilot 프롬프트:

Streamlit Cloud 배포 후 발생할 수 있는 문제들을 미리 점검해줘.

체크리스트:
1. 패키지 import 에러 가능성 (버전 호환성)
2. 환경변수 누락 시 앱 동작 방식
3. 파일 시스템 접근 문제 (로컬 저장 → S3 필수)
4. 세션 상태 리셋 (멀티 사용자 환경에서 충돌 가능성)
5. 메모리 한계 (이미지 생성 시 메모리 사용량)
6. Streamlit Cloud 무료 플랜 제한 확인

배포 후 smoke test 시나리오:
- 처음 접속 → 정상 화면
- 전체 플로우 1회 완주
- 에러 화면 → 재시도 동작
```

---

### 📅 42일차
**목표:** 성능 최적화

```
Copilot 프롬프트:

Streamlit 앱의 성능을 최적화해줘.

1. 불필요한 리렌더링 방지:
   - st.session_state 변경 없을 때 st.rerun() 호출 방지
   - 큰 데이터(이미지)는 session_state 아닌 캐시에 저장

2. 이미지 최적화:
   - PIL로 리사이즈 (max 800px)
   - PNG → WebP 변환

3. API 호출 최적화:
   - @st.cache_data가 실제로 작동하는지 확인
   - 캐시 히트율 로깅

4. 로딩 속도:
   - 앱 초기 로딩 시간 측정 (목표: 3초 이내)
   - 무거운 import를 지연 로딩으로 변경
```

---

### 📅 43일차
**목표:** 베타 유저 모집 준비 + 온보딩

```
Copilot 프롬프트:

베타 테스터 30~50명을 모집하고 관리하기 위한 도구를 만들어줘.

1. 베타 접근 코드 시스템:
   - .streamlit/secrets.toml에 BETA_CODES 리스트 저장
   - 앱 첫 화면에 코드 입력란 추가
   - 올바른 코드 입력 시 세션에 beta_access=True 저장
   - 잘못된 코드 → 대기자 등록 폼으로 이동

2. 대기자 등록 폼:
   - 이름, 이메일, 어떤 업종인지
   - Google Sheets에 저장 (gspread 라이브러리)

3. 베타 유저 안내 배너:
   - "베타 버전 — 피드백을 주시면 커피 기프티콘을 드려요! ☕"
```

---

### 📅 44일차
**목표:** 사용 데이터 분석 대시보드 (관리자용)

```
Copilot 프롬프트:

관리자용 간단한 대시보드 페이지를 만들어줘.
파일: pages/admin.py (Streamlit 멀티페이지)

접근 제한: ADMIN_PASSWORD 환경변수와 일치할 때만 표시

표시 내용:
1. 오늘 생성 건수
2. 누적 생성 건수
3. 평균 완료율 (Step 1 진입 vs Step 5 완료)
4. 가장 많이 선택된 감성 태그 Top 5
5. 에러 발생률
6. 베타 피드백 평균 별점

데이터 소스: 로컬 CSV 파일 (feedback.csv, analytics.csv)
시각화: st.bar_chart, st.metric 활용
```

---

### 📅 45일차
**목표:** QA 완료 + 베타 오픈 준비

```
Copilot 프롬프트:

베타 오픈 전 최종 QA 체크리스트를 만들고 실행해줘.

기능 테스트:
- [ ] Step 1 → 5 전체 플로우 완주 (5회 반복)
- [ ] 이미지 생성 성공 / 실패 양쪽 확인
- [ ] 에러 발생 → 재시도 정상 동작
- [ ] 다시 시작하기 완전 초기화 확인
- [ ] 베타 코드 시스템 동작 확인
- [ ] 피드백 폼 제출 → CSV 저장 확인

성능 테스트:
- [ ] 생성 평균 소요 시간 측정 (10회)
- [ ] 동시 접속 3명 시뮬레이션

보안:
- [ ] .env 파일 gitignore 확인
- [ ] API 키 클라이언트 노출 없음 확인
```

---

## WEEK 10 — 베타 운영 & 피드백 수집 (46일차 ~ 50일차)

---

### 📅 46일차
**목표:** 베타 오픈 🎉 + 초기 버그 모니터링

```
Copilot 프롬프트:

베타 오픈 첫날 모니터링을 위한 로깅 시스템을 강화해줘.

1. 구조화된 로그 설정 (Python logging):
   - 레벨: DEBUG(개발), INFO(운영)
   - 포맷: [시간] [레벨] [파일:라인] 메시지
   - 파일 저장: logs/app.log (일별 롤링)

2. 핵심 이벤트 로깅:
   - 생성 요청 시작: 입력 파라미터 (API 키 제외)
   - 생성 완료: 소요 시간, 성공/실패
   - 에러 발생: 에러 타입, 스택 트레이스

3. 긴급 버그 대응 프로세스:
   - P0(앱 다운): 즉시 롤백 방법
   - P1(기능 오류): 핫픽스 브랜치 전략
```

---

### 📅 47일차
**목표:** 베타 피드백 첫 분석 + 긴급 버그 수정

```
Copilot 프롬프트:

베타 유저 피드백 데이터를 분석해줘.
분석 대상: feedback.csv (수집된 피드백)

분석 항목:
1. 별점 분포 (1~5점 각 비율)
2. 좋았던 점 선택 빈도
3. 개선 의견 텍스트 공통 키워드 추출
4. 어느 단계에서 이탈이 많은지

결과를 바탕으로:
- 즉시 수정할 버그 우선순위 Top 3
- 다음 Phase에서 반영할 개선사항 목록
```

---

### 📅 48일차
**목표:** 피드백 기반 긴급 개선

```
Copilot 프롬프트:

베타 피드백 기반으로 가장 많은 불만이 나온 부분을 수정해줘.

예상 수정 항목:
1. 생성 결과가 너무 일반적이다 → 프롬프트 구체화
   - 업종별 특화 프롬프트 분기 (음식점/패션/IT/뷰티 등)

2. 이미지 품질이 아쉽다 → 이미지 프롬프트 개선
   - 더 구체적인 스타일 지시어 추가

3. 속도가 느리다 → 체감 속도 개선
   - 텍스트 먼저 보여주고 이미지 나중에
```

---

### 📅 49일차
**목표:** Phase 1 결과 정리 + Phase 2 설계 시작

```
Copilot 프롬프트:

Phase 1 완료 보고서를 작성하고 Phase 2 설계를 시작해줘.

Phase 1 완료 보고서 (docs/phase1_report.md):
- 달성한 것: 기능 목록
- 베타 지표: 유저 수, 생성 건수, 평균 별점, 완료율
- 발견된 기술 부채 목록

Phase 2 준비 (FastAPI 전환):
1. FastAPI 프로젝트 구조 설계
   - api/ 폴더 생성 계획
   - 라우터 구조: /api/v1/brand, /api/v1/auth, /api/v1/user
2. 데이터베이스 스키마 초안
   - users, sessions, brand_results 테이블 ERD
3. Supabase Auth 연동 방법 조사
```

---

### 📅 50일차

**🏁 마일스톤 M1 달성 — 패키지 A Streamlit MVP 베타 배포**

```
Copilot 프롬프트:

Phase 1 최종 마일스톤 체크리스트 확인해줘.

- [ ] Streamlit Cloud 배포 URL 생성
- [ ] 베타 유저 30명 이상 확보
- [ ] 전체 플로우 완료율 60% 이상
- [ ] 이미지 생성 성공률 80% 이상
- [ ] 평균 별점 3.5 이상
- [ ] 치명적 버그 0개
- [ ] GA 이벤트 추적 정상 동작

Phase 2 킥오프 체크리스트:
- FastAPI 개발 환경 세팅 필요 항목
- React 학습 필요 부분 (Streamlit → React 전환)
- Supabase 프로젝트 생성 절차
```

---

# PHASE 2 — 서비스화 (회원 & 저장)
### 📆 51일차 ~ 100일차 (10주)

---

## WEEK 11~12 — FastAPI 백엔드 구축 (51일차 ~ 60일차)

---

### 📅 51일차
**목표:** FastAPI 프로젝트 초기화

```
Copilot 프롬프트:

FastAPI 백엔드 프로젝트를 구성해줘.

폴더 구조:
api/
├── main.py              # FastAPI 앱 진입점
├── config.py            # 설정 관리
├── database.py          # DB 연결 (SQLAlchemy)
├── models/
│   ├── user.py          # User ORM 모델
│   ├── brand_result.py  # BrandResult ORM 모델
│   └── session.py       # GenerationSession ORM 모델
├── routers/
│   ├── brand.py         # POST /api/v1/brand/generate
│   ├── auth.py          # POST /api/v1/auth/...
│   └── user.py          # GET/PUT /api/v1/user/...
├── schemas/
│   ├── brand.py         # Pydantic 요청/응답 스키마
│   └── user.py
└── services/
    └── gemini_service.py  # Gemini API 호출

main.py에 CORS 설정 포함 (localhost:3000 허용).
uvicorn으로 실행: uvicorn api.main:app --reload
```

---

### 📅 53일차
**목표:** 데이터베이스 모델 + Alembic 마이그레이션

```
Copilot 프롬프트:

PostgreSQL 데이터베이스 모델을 SQLAlchemy로 작성하고 Alembic을 설정해줘.

테이블:
1. users:
   id(UUID PK), email, created_at, updated_at, plan(free|basic|pro), is_active

2. brand_results:
   id(UUID PK), user_id(FK), created_at,
   business_type, keywords, vibes(JSONB), target,
   result(JSONB), selected_brand_index(int),
   logo_urls(JSONB), character_image_url

3. generation_sessions:
   id(UUID PK), user_id(FK, nullable), created_at,
   completed(bool), error_message, duration_seconds

Alembic 초기화: alembic init alembic
첫 마이그레이션: alembic revision --autogenerate -m "initial"
마이그레이션 실행: alembic upgrade head
```

---

### 📅 55일차
**목표:** brand/generate 엔드포인트 완성

```
Copilot 프롬프트:

FastAPI의 POST /api/v1/brand/generate 엔드포인트를 완성해줘.

요청 스키마 (BrandGenerateRequest):
- business_type: str (필수, 2글자 이상)
- keywords: str (선택)
- vibes: list[str] (1~4개)
- target: str (필수, 2글자 이상)

처리 흐름:
1. 요청 유효성 검사 (Pydantic)
2. Gemini API 호출 (gemini-3-flash-preview)
3. 이미지 생성 시작 (비동기, gemini-3.1-flash-image-preview)
4. 결과를 brand_results 테이블에 저장
5. 응답 반환

응답 스키마 (BrandGenerateResponse):
- result_id: UUID
- brands: list (3개)
- typography: dict
- character: dict
- logo_urls: list (null 가능)

에러 응답: 422, 503, 500
```

---

## WEEK 13~14 — Supabase Auth 연동 (61일차 ~ 70일차)

---

### 📅 61일차
**목표:** Supabase Auth + FastAPI JWT 검증

```
Copilot 프롬프트:

Supabase Auth를 FastAPI에 연동해줘.

방법: Supabase JWT를 FastAPI에서 검증

1. 의존성 설치: supabase-py, python-jose

2. api/auth/jwt.py:
   - verify_supabase_jwt(token: str) -> dict
   - Authorization: Bearer {token} 헤더에서 추출
   - Supabase JWT_SECRET으로 검증
   - 유저 ID, 이메일 반환

3. FastAPI 의존성 (Depends):
   - get_current_user(token: str = Depends(oauth2_scheme)) -> User
   - DB에서 유저 조회 (없으면 자동 생성)

4. 보호된 엔드포인트:
   - GET /api/v1/user/me (인증 필요)
   - POST /api/v1/brand/generate (인증 선택, 미인증 시 결과 미저장)

환경변수: SUPABASE_JWT_SECRET, SUPABASE_URL, SUPABASE_ANON_KEY
```

---

### 📅 63일차
**목표:** React 회원가입/로그인 UI

```
Copilot 프롬프트:

React + Supabase Auth로 회원가입/로그인 UI를 만들어줘.

환경: React 18, Tailwind CSS, @supabase/supabase-js

파일: src/pages/Auth.tsx

기능:
1. 이메일 + 비밀번호 로그인
2. 이메일 회원가입 (+ 이름 입력)
3. Google 소셜 로그인
4. 비밀번호 찾기 (이메일 발송)
5. 로그인 상태 유지 (supabase.auth.getSession())

UI:
- 탭으로 로그인/회원가입 전환
- 로딩 스피너
- 에러 메시지 표시

Supabase 초기화: src/lib/supabase.ts
```

---

## WEEK 15~16 — React 전환 (71일차 ~ 80일차)

---

### 📅 71일차
**목표:** React 앱 기반 구성

```
Copilot 프롬프트:

Streamlit Wizard UI를 React로 마이그레이션해줘.

프로젝트 초기화: Vite + React 18 + TypeScript

기본 구조:
frontend/
├── src/
│   ├── App.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Generate.tsx    # 패키지 A 생성 마법사
│   │   ├── Result.tsx      # 결과 화면
│   │   ├── History.tsx     # 생성 히스토리
│   │   └── Auth.tsx        # 로그인/회원가입
│   ├── components/
│   │   ├── Wizard/
│   │   │   ├── Step1Input.tsx
│   │   │   ├── Step2Vibe.tsx
│   │   │   ├── Step3Target.tsx
│   │   │   └── ProgressBar.tsx
│   │   └── Result/
│   │       ├── BrandCards.tsx
│   │       ├── StorySection.tsx
│   │       ├── TypographySection.tsx
│   │       └── ImageSection.tsx
│   ├── hooks/
│   │   ├── useGenerate.ts
│   │   └── useAuth.ts
│   └── lib/
│       ├── supabase.ts
│       └── api.ts          # FastAPI 호출

Tailwind CSS 설정, react-router-dom v6 포함.
```

---

### 📅 76일차
**목표:** 생성 API 연동 (React)

```
Copilot 프롬프트:

React에서 FastAPI의 /api/v1/brand/generate를 호출하는 훅을 만들어줘.

파일: src/hooks/useGenerate.ts

기능:
- 상태: idle | loading | success | error
- 로딩 중 4단계 메시지 순차 표시 (1.5초 간격)
- 성공 시 result 저장 + Result 페이지 이동
- 에러 시 에러 메시지 표시 + 재시도 버튼

src/lib/api.ts:
- axios 기반
- Authorization 헤더 자동 삽입 (Supabase JWT)
- 응답 에러 처리 (422, 503, 500별 메시지)
- 타임아웃: 45초

설치: @tanstack/react-query, axios
```

---

## WEEK 17~18 — 히스토리 & PDF (81일차 ~ 90일차)

---

### 📅 81일차
**목표:** 생성 히스토리 페이지

```
Copilot 프롬프트:

로그인한 유저의 생성 히스토리를 보여주는 페이지를 만들어줘.

파일: src/pages/History.tsx

UI:
- 그리드 카드 레이아웃 (PC: 3열, 모바일: 1열)
- 각 카드: 브랜드명, 업종, 생성 날짜, 선택한 감성 태그 2~3개
- 카드 클릭 → 결과 상세 화면
- 북마크 버튼 (즐겨찾기)
- 삭제 버튼 (확인 다이얼로그)
- 검색 기능 (브랜드명, 업종으로 필터)

FastAPI 엔드포인트 (GET /api/v1/user/history):
- 로그인 유저의 brand_results 목록
- 페이지네이션 (20개씩)
- 정렬: 최신순 기본
```

---

### 📅 86일차
**목표:** PDF 다운로드 (WeasyPrint)

```
Copilot 프롬프트:

패키지 A 결과를 PDF로 다운로드하는 기능을 구현해줘.

백엔드: api/services/pdf_generator.py
도구: WeasyPrint + Jinja2

PDF 구성 (6페이지):
1. 표지: 브랜드명 + 슬로건 + 생성 날짜
2. 브랜드 스토리: story + meaning
3. 서체 가이드: 한글/영문 폰트명 + 사용 이유
4. 캐릭터 컨셉: 이름 + 성격 + 외형
5. 로고 시안: 이미지 3개 (있는 경우)
6. 브랜드 활용 다음 단계 안내

FastAPI 엔드포인트:
GET /api/v1/brand/{result_id}/pdf
- PDF 바이트 반환 (Content-Type: application/pdf)
- 파일명: {브랜드명}_브랜드정체성.pdf

한글 폰트: 나눔고딕 (WeasyPrint 폰트 설정)
```

---

### 📅 100일차

**🏁 마일스톤 M2 달성 — 회원/저장 기능 완성**

```
Copilot 프롬프트:

Phase 2 완료 체크리스트 확인:
- [ ] FastAPI + PostgreSQL 정상 동작
- [ ] Supabase Auth 이메일/Google 로그인
- [ ] 생성 결과 자동 저장
- [ ] 히스토리 목록 + 재열람
- [ ] PDF 다운로드 (한글 폰트 정상)
- [ ] Vercel(프론트) + Railway(백엔드) 배포
- [ ] 신규 회원 100명 목표

Phase 3 킥오프 준비:
- Stripe 계정 생성 + 사업자 정보 등록
- 구독 플랜 구성 계획 (무료/Basic/Pro 가격 확정)
```

---

# PHASE 3 — 수익화 (구독 & 결제)
### 📆 101일차 ~ 150일차 (10주)

---

### 📅 101일차
**목표:** Stripe 결제 시스템 초기 설정

```
Copilot 프롬프트:

Stripe 결제 시스템을 설정해줘.

구독 플랜 정의:
- Free: 월 2회 생성, 히스토리 5개
- Basic: 월 9,900원, 월 10회 생성, 히스토리 무제한, PDF 다운로드
- Pro: 월 29,900원, 무제한 생성, 패키지 B·C·D 포함, 이미지 생성 포함

백엔드 설정:
pip install stripe
환경변수: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
STRIPE_PRICE_BASIC_ID, STRIPE_PRICE_PRO_ID

api/routers/payment.py:
- POST /api/v1/payment/create-checkout-session
- POST /api/v1/payment/webhook
- GET /api/v1/payment/subscription-status
- POST /api/v1/payment/cancel-subscription

Stripe Checkout 사용 (커스텀 결제 UI 최소화).
```

---

### 📅 108일차
**목표:** Webhook 처리

```
Copilot 프롬프트:

Stripe Webhook 처리 로직을 완성해줘.

처리할 이벤트:
1. checkout.session.completed → 구독 활성화, users.plan 업데이트
2. invoice.payment_succeeded → 갱신 성공, 영수증 이메일 발송
3. invoice.payment_failed → 결제 실패, 유저에게 알림 이메일
4. customer.subscription.deleted → 구독 취소, plan=free 다운그레이드

Webhook 보안:
- stripe.Webhook.construct_event()로 서명 검증

이메일 발송: Resend API
- 구독 성공 이메일 템플릿
- 결제 실패 이메일 (카드 업데이트 링크 포함)
- 구독 취소 확인 이메일

환경변수: RESEND_API_KEY
```

---

### 📅 115일차
**목표:** 사용량 제한 (Redis 카운터)

```
Copilot 프롬프트:

구독 플랜별 기능 제한을 Redis 카운터로 구현해줘.
파일: api/services/usage_limiter.py

플랜별 한도:
- free: 월 2회 / basic: 월 10회 / pro: 무제한

함수: check_usage_limit(user_id: str, plan: str) -> bool
- Redis 키: usage:{user_id}:{YYYY-MM}
- 월초에 자동 리셋 (TTL: 월말까지)
- 한도 초과 시 False 반환

함수: increment_usage(user_id: str) -> int
- 생성 성공 시 카운터 증가

FastAPI 미들웨어에서 generate 엔드포인트 호출 전 체크.
한도 초과 시 HTTP 429 + 업그레이드 안내.
```

---

### 📅 122일차
**목표:** 구독 관리 UI (React)

```
Copilot 프롬프트:

구독 관리 페이지를 React로 만들어줘.
파일: src/pages/Subscription.tsx

UI 구성:
1. 현재 플랜 표시 (배지 + 기능 목록)
2. 플랜 비교 표 (Free / Basic / Pro)
3. 업그레이드 버튼 → Stripe Checkout으로 이동
4. 이번 달 사용량 표시 (n회 / 한도)
5. 구독 취소 버튼 (취소 이유 선택 모달)
6. 영수증 내역 (최근 6개월)

결제 성공 후 돌아올 때: ?success=true 파라미터로 성공 메시지 표시.
```

---

### 📅 130일차
**목표:** 신규 가입 온보딩 플로우

```
Copilot 프롬프트:

신규 회원 온보딩 플로우를 만들어줘.

1. 가입 직후 온보딩 마법사 (3단계):
   Step 1: "어떤 사업을 준비하고 계신가요?" (업종 카테고리 선택)
   Step 2: "브랜딩 고민이 어떤 건가요?" (다중 선택)
   Step 3: "Name Tag로 시작해봐요!" (무료 체험 안내)

2. Welcome 이메일 시퀀스 (Resend):
   - D0 (가입 즉시): 환영 + 첫 생성 가이드
   - D3 (3일 후): "첫 브랜드를 만들어보셨나요?" + 팁
   - D7 (7일 후): "무료 체험 기간 안내" + 업그레이드 혜택

3. 이탈 방지 넛지:
   - Step 2에서 5분 이상 머물면 "어려우세요? 예시로 시작해보세요!" 팝업
```

---

### 📅 137일차
**목표:** PostHog 분석 연동

```
Copilot 프롬프트:

PostHog로 사용자 행동 분석을 연동해줘.

1. React 클라이언트 설정: npm install posthog-js

2. 추적할 이벤트:
   - generation_started: 생성 버튼 클릭
   - generation_completed: 생성 성공 (duration_ms, plan 포함)
   - generation_failed: 생성 실패 (error_type)
   - image_generated: 이미지 생성 완료
   - plan_upgraded: 구독 업그레이드 (from_plan, to_plan)
   - pdf_downloaded: PDF 다운로드

3. 사용자 식별:
   로그인 시 posthog.identify(user_id, {email, plan, created_at})
```

---

### 📅 144일차
**목표:** 결제 전체 테스트

```
Copilot 프롬프트:

Stripe 결제 전체 플로우를 테스트해줘.
Stripe 테스트 카드 번호: 4242 4242 4242 4242

테스트 시나리오:
1. 무료 → Basic 업그레이드 → 결제 성공 → plan 업데이트 확인
2. 결제 실패 (4000 0000 0000 0002) → 에러 처리
3. Basic → Pro 업그레이드
4. 구독 취소 → 다음 결제일까지 Pro 유지 확인
5. Webhook 서명 위조 시도 → 거부 확인
6. 월 사용량 한도 도달 → 업그레이드 안내 표시
```

---

### 📅 150일차

**🏁 마일스톤 M3 달성 — 수익 발생 시작**

```
Copilot 프롬프트:

Phase 3 완료 보고서 (docs/phase3_report.md):
- MRR (Monthly Recurring Revenue) 현황
- 플랜별 유저 분포 (Free/Basic/Pro)
- 유료 전환율
- Churn Rate (구독 취소율)
- 월 생성 건수 vs 한도 도달 비율

Phase 4 킥오프 준비:
- 패키지 B 프롬프트 설계 초안
- WeasyPrint PDF 템플릿 와이어프레임
- S3 PDF 저장 구조 설계
```

---

# PHASE 4 — 패키지 B·C·D 가이드 제안서
### 📆 151일차 ~ 225일차 (15주)

---

### 📅 151일차
**목표:** 패키지 B — 브랜드 키트 가이드 프롬프트 설계

```
Copilot 프롬프트:

패키지 B (브랜드 키트 가이드) 프롬프트를 설계해줘.
파일: api/services/package_b_generator.py

패키지 A 결과를 컨텍스트로 받아 JSON 생성:
{
  "color_palette": [
    {"name": "메인 컬러", "hex": "#XXXXXX", "usage": "사용 맥락"},
    {"name": "서브 컬러 1", "hex": "#XXXXXX", "usage": "..."},
    {"name": "서브 컬러 2", "hex": "#XXXXXX", "usage": "..."},
    {"name": "포인트 컬러", "hex": "#XXXXXX", "usage": "..."},
    {"name": "배경 컬러", "hex": "#XXXXXX", "usage": "..."}
  ],
  "typography_guide": {
    "primary_font": {"name": "", "weight": "", "usage": ""},
    "secondary_font": {"name": "", "weight": "", "usage": ""},
    "size_scale": ["제목: 32px", "소제목: 24px", "본문: 16px", "캡션: 12px"]
  },
  "logo_usage_rules": ["규칙1", "규칙2"],
  "application_examples": [
    {"item": "명함", "description": "..."},
    {"item": "봉투", "description": "..."},
    {"item": "패키지", "description": "..."}
  ]
}

모델: gemini-3-flash-preview
```

---

### 📅 158일차
**목표:** 패키지 B PDF 템플릿 작성

```
Copilot 프롬프트:

패키지 B 브랜드 키트 가이드 PDF 템플릿을 만들어줘.
도구: Jinja2 HTML 템플릿 + WeasyPrint
파일: api/templates/package_b.html

페이지 구성 (6~8페이지):
1. 표지: 브랜드명 + "브랜드 키트 가이드" + 날짜
2. 컬러 팔레트: 5가지 색상 칩 + HEX 코드 + 사용 맥락
3. 서체 가이드: 폰트명 + 웨이트 + 사용 예시 텍스트
4. 로고 사용 규칙: 텍스트 목록
5. 적용 예시 — 명함 레이아웃 설명
6. 적용 예시 — 디지털 SNS 프로필 가이드
7. 다음 단계 안내

스타일:
- 브랜드 컬러를 동적으로 적용 (Jinja2 변수)
- 나눔고딕 한글 폰트 임베딩
- A4 세로, 여백 25mm

WeasyPrint 한글 폰트 설정 방법도 포함해줘.
```

---

### 📅 165일차
**목표:** 패키지 B API 엔드포인트 + S3 저장

```
Copilot 프롬프트:

패키지 B 엔드포인트와 PDF S3 저장을 구현해줘.

FastAPI 엔드포인트:
POST /api/v1/package/b/generate
- 요청: brand_result_id (기존 패키지 A 결과 ID)
- 처리: package_b_generator.py로 콘텐츠 생성 → PDF 생성 → S3 업로드
- 응답: pdf_url, result_id

GET /api/v1/package/b/{result_id}/pdf
- PDF presigned URL 반환 (24시간 유효)

S3 저장 구조:
pdfs/package_a/{user_id}/{result_id}.pdf
pdfs/package_b/{user_id}/{result_id}.pdf

DB 테이블 추가: package_results
- id, user_id, brand_result_id, package_type(A|B|C|D)
- content(JSONB), pdf_url, created_at

플랜 제한: Basic 이상만 패키지 B 이용 가능.
```

---

### 📅 172일차
**목표:** 패키지 B React UI

```
Copilot 프롬프트:

패키지 B를 React에서 사용하는 UI를 만들어줘.

진입점: 패키지 A 결과 화면 하단 "🎨 브랜드 키트 만들기" 섹션

UI 흐름:
1. 패키지 B 소개 카드 (무엇을 만들어주는지 설명)
2. "브랜드 키트 생성하기" 버튼
   - Basic 미만: "Basic 플랜 이상에서 사용 가능" + 업그레이드 버튼
   - Basic 이상: 바로 생성 시작
3. 생성 중 로딩 (10~20초 예상)
4. 완료 후 미리보기:
   - 컬러 팔레트 (색상 칩 5개)
   - 서체 이름 표시
   - "PDF 전체 다운로드" 버튼
5. 이미 생성된 경우: 이전 결과 재다운로드 버튼

파일: src/components/PackageB/PackageBSection.tsx
```

---

### 📅 179일차
**목표:** 패키지 C — 웹/앱 가이드 프롬프트 설계

```
Copilot 프롬프트:

패키지 C (웹/앱 페이지 가이드) 프롬프트를 설계해줘.
파일: api/services/package_c_generator.py

패키지 A + B 결과를 컨텍스트로 받아 JSON 생성:
{
  "landing_page_structure": [
    {"section": "히어로", "content": "...", "copy_guide": "..."},
    {"section": "문제 제기", "content": "...", "copy_guide": "..."},
    {"section": "해결책", "content": "...", "copy_guide": "..."},
    {"section": "사회적 증거", "content": "...", "copy_guide": "..."},
    {"section": "CTA", "content": "...", "copy_guide": "..."}
  ],
  "ui_style_guide": {
    "button_style": "...", "card_style": "...", "spacing": "..."
  },
  "mobile_strategy": "...",
  "seo_keywords": ["키워드1", "키워드2"],
  "cta_copies": ["CTA 문구1", "CTA 문구2", "CTA 문구3"]
}
```

---

### 📅 193일차
**목표:** 패키지 D — 인테리어 가이드 프롬프트 설계

```
Copilot 프롬프트:

패키지 D (실내 인테리어 가이드) 프롬프트를 설계해줘.
파일: api/services/package_d_generator.py

업종별 인테리어 패턴 매핑 (프롬프트에 포함):
- 카페: 좌석 밀도, 조명 온도, 소재(우드/패브릭), 동선
- 오피스: 집중존/협업존 구분, 브랜드 컬러 포인트월
- 쇼룸/팝업: 상품 진열 동선, 포토존 설계
- 뷰티샵: 조명 균일도, 위생 소재, 거울 배치
- 피트니스: 에너지 컬러, 거울/조명, 운동존 분리

생성할 JSON:
{
  "space_concept": "공간 컨셉 한 줄",
  "mood_keywords": ["키워드1", "키워드2", "키워드3"],
  "color_application": {"wall": "...", "floor": "...", "accent": "..."},
  "material_guide": [{"material": "", "usage": "", "reason": ""}],
  "lighting_plan": "조명 계획",
  "furniture_direction": "가구·소품 방향성",
  "reference_keywords": ["무드보드 검색 키워드"]
}
```

---

### 📅 210일차
**목표:** 패키지 B·C·D 통합 QA

```
Copilot 프롬프트:

패키지 B·C·D 통합 QA를 해줘.

테스트:
1. 다양한 업종별 각 패키지 생성 (10종):
   카페, 패션, IT, 뷰티, 음식점, 스튜디오, 학원, 반려동물, 인테리어, 피트니스
2. PDF 품질 확인:
   - 한글 폰트 깨짐 없음
   - 컬러 팔레트 HEX 코드 정확도
   - 서체 이름 실제 존재 여부
3. A→B→C→D 데이터 흐름 전체 테스트
4. 플랜 제한 (Free 계정으로 접근 시도 → 차단)
5. S3 업로드 + 다운로드 URL 동작
```

---

### 📅 225일차

**🏁 마일스톤 M4 달성 — 패키지 B·C·D 가이드 제안서 완성**

```
Copilot 프롬프트:

Phase 4 완료 후 분석:
- 패키지 B/C/D 추가 후 MRR 변화
- 패키지별 이용률 비교
- 가장 인기 있는 패키지

Phase 5 킥오프 준비:
- 디자인 파트너 모집 전략
- Stripe Connect 사전 신청 가이드
- 파트너 온보딩 폼 와이어프레임
```

---

# PHASE 5 — B2B 중개 플랫폼
### 📆 226일차 ~ 260일차 (7주)

---

### 📅 226일차
**목표:** 파트너 DB 모델 + 등록 API

```
Copilot 프롬프트:

B2B 디자인 파트너 시스템을 구축해줘.

DB 테이블: design_partners
- id, name, business_name, email, phone
- specialties(JSONB): ["브랜딩", "웹디자인", "패키지디자인"]
- price_range: {min: int, max: int}
- portfolio_urls(JSONB)
- rating: float, review_count: int
- is_verified: bool (관리자 승인)

DB 테이블: quote_requests
- id, user_id, partner_id, brand_result_id
- budget_min, budget_max, requirements: text
- status: pending|responded|contracted|completed|cancelled

FastAPI:
POST /api/v1/partners/register
GET /api/v1/partners/search (감성/예산 기반 검색)
POST /api/v1/partners/{id}/quote-request
```

---

### 📅 233일차
**목표:** 매칭 로직 + 파트너 대시보드

```
Copilot 프롬프트:

파트너 매칭 알고리즘과 파트너용 대시보드를 만들어줘.

매칭 알고리즘:
함수: match_partners(brand_result, budget) -> list[Partner]
- 감성 태그와 파트너 specialties 겹치는 수로 점수
- 예산 범위 필터
- 평점 가중치 (rating * 0.3)
- 최대 5개 추천

파트너 대시보드 (별도 React 페이지):
- 신규 견적 요청 목록
- 견적 응답 폼 (예상 금액, 포트폴리오 첨부, 메시지)
- 진행 중 프로젝트
- 완료 프로젝트 + 리뷰
- 정산 내역

파트너 알림: 새 견적 요청 시 이메일 (Resend)
```

---

### 📅 240일차
**목표:** Stripe Connect 정산 설정

```
Copilot 프롬프트:

Stripe Connect로 파트너 수수료 정산 시스템을 만들어줘.

설정:
- Stripe Connect Express 계정 (파트너용)
- 플랫폼 수수료: 거래액의 15%

API 엔드포인트:
POST /api/v1/partners/connect/onboard
- Stripe Connect 온보딩 링크 생성
- 파트너가 계좌 정보 입력

POST /api/v1/payments/contract
- 유저가 파트너에게 결제
- Stripe Payment Intent (destination charge)
- 자동 수수료 분리

GET /api/v1/partners/{id}/payouts
- 파트너 정산 내역

Webhook: account.updated (파트너 계좌 인증 완료)
```

---

### 📅 247일차
**목표:** 리뷰 & 신뢰 시스템

```
Copilot 프롬프트:

파트너 리뷰 및 신뢰도 시스템을 만들어줘.

DB 테이블: partner_reviews
- id, user_id, partner_id, quote_request_id
- rating(1~5), title, content
- is_verified (계약 완료 후만 작성 가능)

API:
POST /api/v1/reviews (리뷰 작성)
GET /api/v1/partners/{id}/reviews (리뷰 목록)
POST /api/v1/reviews/{id}/report (신고)

파트너 평점 자동 계산: 리뷰 작성 시 design_partners.rating 업데이트

관리자 기능:
- 신고된 리뷰 검토 대기열
- 파트너 경고/정지/퇴출 처리
- 허위 리뷰 판별 기준 (같은 IP, 가입 직후 리뷰 등)
```

---

### 📅 256일차
**목표:** 전체 시스템 통합 QA

```
Copilot 프롬프트:

전체 Name Tag 서비스 최종 QA 체크리스트를 만들고 실행해줘.

패키지 A:
- [ ] 브랜드 생성 전체 플로우
- [ ] 이미지 생성 (로고 3종 + 캐릭터)
- [ ] PDF 다운로드

패키지 B·C·D:
- [ ] 각 패키지 생성 + PDF 다운로드
- [ ] 플랜 제한 정상 동작
- [ ] A→B→C→D 데이터 연결

결제:
- [ ] 구독 업그레이드 (테스트 카드)
- [ ] Webhook 정상 처리

B2B 중개:
- [ ] 파트너 등록 + 승인
- [ ] 유저 → 파트너 견적 요청
- [ ] 계약 → Stripe Connect 정산
- [ ] 리뷰 작성

보안:
- [ ] 인증 없이 보호 API 접근 시도 → 401
- [ ] 타인 데이터 접근 시도 → 403
```

---

### 📅 260일차

**🏁 마일스톤 M5 달성 — 전체 서비스 완성 🎉**

```
Copilot 프롬프트:

Name Tag 서비스 런칭 최종 체크리스트:

서비스:
- [ ] 모든 패키지 A·B·C·D 정상 동작
- [ ] B2B 중개 플랫폼 동작
- [ ] 결제 시스템 (구독 + 단건 + Connect)

인프라:
- [ ] Vercel 프론트 배포 (커스텀 도메인)
- [ ] Railway 백엔드 배포
- [ ] PostgreSQL + Redis + S3 연결
- [ ] CloudFront CDN 연결

모니터링:
- [ ] Sentry 에러 추적 연동
- [ ] PostHog 대시보드 설정
- [ ] Stripe 대시보드 정산 확인
- [ ] UptimeRobot 서버 모니터링

런칭 후 첫 주 모니터링 계획도 만들어줘.
```

---

## 📊 주간 루틴

| 요일 | 루틴 |
|------|------|
| **월요일** | 주간 계획 점검, 이전 주 미완성 항목 이월 |
| **화~목** | 본격 개발 (하루 4~6시간) |
| **금요일** | 코드 리뷰, 커밋 정리, 주간 회고 |

---

## 🆘 막혔을 때 Copilot 프롬프트

```
# 에러 해결
이 에러가 발생했어: [에러 메시지 전체 붙여넣기]
파일: [파일명]
관련 코드: [코드 붙여넣기]
원인과 해결 방법을 알려줘.

# 코드 리뷰
이 코드에서 개선할 점을 찾아줘. 성능, 가독성, 보안 관점에서:
[코드 붙여넣기]

# 다음 단계 막막할 때
현재 [파일명]까지 완성했어. 오늘 계획은 [목표]인데
어디서부터 시작해야 할지 단계별로 알려줘.

# 테스트 작성
[함수명] 함수에 대한 pytest 테스트를 작성해줘.
엣지 케이스까지 포함해서.
[함수 코드 붙여넣기]
```

---

*버전: v3.0 | 기술 스택: Streamlit → React 18 + Tailwind CSS + FastAPI*