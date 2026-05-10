# 🏷️ Name Tag — 개발 플랜 & VS Code Copilot 프롬프트 가이드

> **시작일:** 2026년 5월 4일 (월) | **완료 목표:** 2027년 4월 24일 (금)  
> **총 기간:** 52주 (약 13개월) | **개발자:** 1인 기준 (하루 4~6시간)  
> **프레임워크:** `Django 4.2` | **LLM:** `gemini-3-flash-preview` | **이미지 생성:** `gemini-3.1-flash-image-preview`

---

## 📌 Copilot 사용법

VS Code에서 `Ctrl+Shift+I` (또는 `Cmd+Shift+I`) → Copilot Chat 열기  
각 날짜의 **Copilot 프롬프트** 블록을 그대로 복붙해서 사용하세요.  
`.github/copilot-instructions.md` 파일에 아래 기술 스택을 저장해두면 매번 입력 불필요합니다.

---

## 🛠️ 기술 스택 레퍼런스 (전체 공통)

```
언어:         Python 3.11
웹 프레임워크: Django 4.2 (풀스택 — 프론트·백엔드 통합)
프론트:        Django Templates + Tailwind CSS (CDN)
LLM:          Google Gemini API — gemini-3-flash-preview
이미지 생성:   Google Gemini API — gemini-3.1-flash-image-preview
DB:            PostgreSQL + Django ORM (내장 migration)
인증:          Django 내장 Auth (django.contrib.auth)
결제:          Stripe + Stripe Connect
캐싱:          Redis (django-redis)
저장소:        AWS S3 (django-storages)
PDF 생성:      WeasyPrint + Django Template
배포:          Railway (단일 서버 — Django + gunicorn)
분석:          PostHog + Google Analytics
이메일:        Resend (django-anymail)
테스트:        pytest-django
```

---

## 🗓️ 전체 마일스톤

| 마일스톤 | 날짜 | 내용 |
|---------|------|------|
| ✅ M0 | 2026.05.22 | 개발 환경 완성 + CI/CD 동작 |
| ✅ M1 | 2026.07.10 | 패키지 A Django MVP 베타 배포 |
| ✅ M2 | 2026.09.18 | Django 서비스화 — 회원/저장 기능 |
| ✅ M3 | 2026.11.27 | Stripe 구독 결제 → 수익 발생 시작 |
| ✅ M4 | 2027.03.05 | 패키지 B·C·D 가이드 제안서 출시 |
| ✅ M5 | 2027.04.24 | B2B 중개 플랫폼 완성 |

---

---

# PHASE 0 — 환경 세팅 & 구조 확립
### 📆 2026.05.04 ~ 2026.05.22 (3주)

---

## WEEK 1 — 개발 환경 세팅 (5/4 ~ 5/8)

---

### 📅 2026년 5월 4일 (월)
**목표:** GitHub 레포 생성 + 브랜치 전략 확립  
**태스크:** 레포 초기화, 브랜치 규칙 설정, README 초안 작성

```
Copilot 프롬프트:

GitHub 레포지토리를 새로 만들고 있어. 아래 조건에 맞는 초기 세팅 파일들을 만들어줘.

프로젝트: Name Tag (AI 브랜딩 플랫폼)
언어: Python 3.11

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

### 📅 2026년 5월 5일 (화)
**목표:** Python 환경 + 의존성 관리 설정  
**태스크:** pyproject.toml 작성, 가상환경 구성, 핵심 패키지 설치

```
Copilot 프롬프트:

Python 3.11 Django 프로젝트의 requirements.txt를 작성해줘.
패키지 관리는 pip + requirements.txt 방식으로 할 거야.
아래 패키지들을 버전 고정해서 정리해줘:

필수 (requirements.txt):
- django==4.2.13
- psycopg2-binary          # PostgreSQL 드라이버
- django-environ           # 환경변수 관리
- django-redis             # Redis 캐시
- django-storages[s3]      # S3 파일 저장
- django-anymail[sendgrid] # 이메일 (Resend 호환)
- google-generativeai      # Gemini API
- stripe                   # 결제
- weasyprint               # PDF 생성
- tenacity                 # API 재시도
- boto3                    # AWS S3
- Pillow                   # 이미지 처리
- gunicorn                 # 운영 서버
- whitenoise               # 정적 파일 서빙
- ruff                     # 린터

개발 전용 (requirements-dev.txt):
- pytest-django
- pytest-mock
- factory-boy              # 테스트 데이터 생성

requirements.txt와 requirements-dev.txt로 분리해줘.
```

---

### 📅 2026년 5월 6일 (수)
**목표:** 폴더 구조 확립  
**태스크:** 전체 프로젝트 디렉터리 구조 생성 + 각 파일 역할 정의

```
Copilot 프롬프트:

Name Tag Django 프로젝트의 폴더 구조를 만들어줘.
아래 구조로 빈 파일들을 생성하고, 각 파일 상단에 역할 주석을 달아줘.

django-admin startproject config .  명령 실행 후 아래 앱 구조로 구성해줘.

nametag/                           # 프로젝트 루트
├── manage.py
├── .env.example                   # 환경변수 템플릿
├── requirements.txt
├── requirements-dev.txt
├── config/                        # 프로젝트 설정
│   ├── settings/
│   │   ├── base.py                # 공통 설정
│   │   ├── dev.py                 # 개발 환경 설정
│   │   └── prod.py                # 운영 환경 설정
│   ├── urls.py                    # 루트 URL 라우터
│   └── wsgi.py
├── brand/                         # 브랜드 생성 앱
│   ├── migrations/
│   ├── templates/brand/
│   │   ├── step1_input.html       # Step 1: 업종 입력
│   │   ├── step2_vibe.html        # Step 2: 감성 선택
│   │   ├── step3_target.html      # Step 3: 타겟 고객
│   │   ├── generating.html        # 생성 중 로딩
│   │   └── result.html            # 결과 화면
│   ├── forms.py                   # 입력 폼 정의
│   ├── models.py                  # BrandResult 모델
│   ├── views.py                   # 단계별 View
│   ├── urls.py                    # brand/ URL 패턴
│   └── services/
│       ├── brand_generator.py     # Gemini 텍스트 생성
│       └── image_generator.py     # Gemini 이미지 생성
├── users/                         # 회원 앱 (Phase 2)
│   ├── migrations/
│   ├── templates/users/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── payments/                      # 결제 앱 (Phase 3)
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── utils/
│   ├── __init__.py
│   └── parser.py                  # JSON 파싱 유틸
├── static/                        # CSS, JS, 이미지
└── tests/
    ├── conftest.py
    ├── test_brand_generator.py
    └── test_parser.py

각 파일 상단에 역할 주석(한글 docstring)을 달아줘.
```

---

### 📅 2026년 5월 7일 (목)
**목표:** .env 관리 체계 + Gemini API 키 연결 테스트  
**태스크:** 환경변수 로딩 구조 작성, API 연결 확인 스크립트

```
Copilot 프롬프트:

아래 환경변수를 관리하는 config.py 파일을 만들어줘.
파일 위치: config/settings/base.py 및 .env

필요한 환경변수:
- GOOGLE_API_KEY (Gemini API)
- DATABASE_URL (PostgreSQL — Django DB 설정)
- REDIS_URL
- STRIPE_SECRET_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- S3_BUCKET_NAME

조건:
- django-environ으로 .env 파일 로딩 (env = environ.Env())
- 환경변수 없으면 명확한 에러 메시지 출력
- 개발/운영 환경 분리 (ENV=dev|prod)
- 타입 힌트 포함

그리고 scripts/test_api_connection.py 파일도 만들어줘.
Gemini API (gemini-3-flash-preview) 연결이 정상인지 확인하는 간단한 테스트 스크립트.
```

---

### 📅 2026년 5월 8일 (금)
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
4. python manage.py check (Django 설정 검증)
5. pytest tests/ -v --ds=config.settings.dev (테스트 실행)

추가 조건:
- 환경변수는 GitHub Secrets에서 주입 (GOOGLE_API_KEY 등)
- 테스트 실패 시 Slack 알림 (선택, webhook URL은 SLACK_WEBHOOK secret으로)
- 캐싱: pip 캐시 적용해서 속도 개선
```

**🔖 주간 회고:** 환경 세팅 완료 여부 체크  
- [ ] GitHub 레포 생성  
- [ ] requirements.txt 버전 고정  
- [ ] 폴더 구조 완성  
- [ ] .env 환경변수 로딩 확인  
- [ ] CI 파이프라인 동작 확인  

---

## WEEK 2 — 프로젝트 구조 확립 (5/11 ~ 5/15)

---

### 📅 2026년 5월 11일 (월)
**목표:** Django 프로젝트 초기화 + 브랜드 앱 세팅  
**태스크:** Django 프로젝트 생성 + brand 앱 등록 + URL 구조 확립

```
Copilot 프롬프트:

Django 4.2 프로젝트를 초기 세팅해줘.

1. django-admin startproject config . 실행 후 settings를 분리해줘:
   - config/settings/base.py (공통)
   - config/settings/dev.py  (DEBUG=True, 로컬 DB)
   - config/settings/prod.py (DEBUG=False, 운영 설정)

2. django-environ으로 .env 로딩:
   env = environ.Env()
   environ.Env.read_env(BASE_DIR / ".env")
   SECRET_KEY = env("SECRET_KEY")
   DATABASE_URL = env("DATABASE_URL")

3. INSTALLED_APPS에 추가:
   "brand", "users", "payments"

4. config/urls.py 루트 라우터:
   path("", include("brand.urls"))
   path("users/", include("users.urls"))
   path("payments/", include("payments.urls"))

5. brand/urls.py 초안:
   path("", views.Step1View.as_view(), name="step1")
   path("step2/", views.Step2View.as_view(), name="step2")
   path("step3/", views.Step3View.as_view(), name="step3")
   path("generating/", views.GeneratingView.as_view(), name="generating")
   path("result/", views.ResultView.as_view(), name="result")

6. 로컬 실행 확인: python manage.py runserver
```

---

### 📅 2026년 5월 12일 (화)
**목표:** pytest 테스트 기반 구축  
**태스크:** brand_generator.py 단위 테스트 + mock 설정

```
Copilot 프롬프트:

tests/test_brand_generator.py 파일을 작성해줘.

테스트 대상: nametag/services/brand_generator.py의 generate_brand_identity() 함수

테스트 케이스:
1. test_normal_input: 정상 입력 → dict 반환 확인 (brands, typography, character 키 포함)
2. test_json_extraction_codeblock: ```json ... ``` 형식 응답 파싱
3. test_json_extraction_plain: 순수 JSON 텍스트 파싱
4. test_missing_key_raises: 필수 키 누락 시 ValueError 발생
5. test_empty_response_raises: 빈 응답 시 에러 처리
6. test_extract_json_fallback: 텍스트 앞뒤에 설명이 붙은 경우도 파싱 성공

Gemini API 호출은 pytest-mock으로 mock 처리해줘.
conftest.py에 공통 fixture 분리.
```

---

### 📅 2026년 5월 13일 (수)
**목표:** utils/parser.py 완성  
**태스크:** JSON 추출 함수 3단계 방어 로직

```
Copilot 프롬프트:

nametag/utils/parser.py 파일을 완성해줘.

핵심 함수: extract_json(text: str) -> dict | None

3단계 추출 전략:
1. 코드블록 안 JSON 추출: ```json ... ``` 또는 ``` ... ``` 패턴 정규식
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

### 📅 2026년 5월 14일 (목)
**목표:** 린트 설정 + 코드 스타일 통일  
**태스크:** ruff 설정, pre-commit hooks 구성

```
Copilot 프롬프트:

Python 코드 품질 관리 도구를 설정해줘.

1. pyproject.toml에 ruff 설정 추가:
   - line-length: 100
   - target-version: py311
   - 활성화 규칙: E, W, F, I (isort 포함)
   - 무시 규칙: E501 (너무 긴 줄은 유연하게)
   - 제외 폴더: migrations/, .venv/

2. .pre-commit-config.yaml 작성:
   - ruff check --fix 자동 실행
   - trailing whitespace 제거
   - 파일 끝 newline 추가
   - Python 디버그 구문(breakpoint, pdb) 커밋 방지

3. Makefile 작성 (자주 쓰는 명령어 단축):
   - make lint: ruff check
   - make test: pytest -v
   - make run: python manage.py runserver
   - make migrate: python manage.py migrate
   - make shell: python manage.py shell
   - make clean: __pycache__ 삭제
```

---

### 📅 2026년 5월 15일 (금)
**목표:** Week 2 통합 점검 + 문서화  
**태스크:** 전체 코드 lint 통과 확인, README 업데이트

```
Copilot 프롬프트:

현재까지 작성된 nametag/ 프로젝트 전체를 점검해줘.

점검 항목:
1. 모든 Python 파일에 타입 힌트가 있는지 확인
2. 모든 public 함수에 docstring이 있는지 확인
3. __init__.py에 __all__ 목록이 정의되어 있는지
4. import 순서가 ruff 기준에 맞는지 (stdlib → third-party → local)

README.md 업데이트:
- 로컬 개발 환경 세팅 방법 (단계별)
- 환경변수 설정 방법 (.env.example 기반)
- 테스트 실행 방법
- 브랜치 전략

위 내용을 검토하고 수정이 필요한 부분을 알려줘.
```

---

## WEEK 3 — 마무리 & QA (5/18 ~ 5/22)

---

### 📅 2026년 5월 18일 (월)
**목표:** 전체 구조 최종 점검 + 누락 파일 보완

```
Copilot 프롬프트:

nametag 프로젝트에 아래 파일들이 빠져있는지 확인하고 생성해줘.

1. .env.example — 모든 환경변수 키를 빈 값으로 정리한 템플릿
2. CONTRIBUTING.md — 기여 가이드 (브랜치 네이밍, 커밋 메시지 규칙)
3. scripts/seed_test_data.py — 개발용 테스트 데이터 생성 스크립트
4. docs/architecture.md — 시스템 구조 다이어그램 (텍스트 기반 ASCII)

커밋 메시지 규칙은 Conventional Commits 방식으로:
feat: 기능 추가
fix: 버그 수정
docs: 문서
test: 테스트
refactor: 리팩터링
chore: 빌드/설정
```

---

### 📅 2026년 5월 19일 (화)
**목표:** CI 파이프라인 실제 동작 검증  
**태스크:** 더미 테스트로 전체 파이프라인 통과 확인

```
Copilot 프롬프트:

GitHub Actions CI가 올바르게 동작하는지 확인하기 위한 검증 태스크를 도와줘.

1. tests/ 폴더의 모든 테스트를 pytest -v로 실행했을 때
   예상 통과 테스트 목록을 알려줘

2. 현재 테스트 커버리지가 낮은 부분은 어디인지 분석해줘
   (아직 구현 안 된 부분 제외)

3. ruff check . 실행 결과 예상 경고가 있으면 미리 수정해줘

4. CI 워크플로우에서 secrets 없이 동작하는 부분과
   secrets 필요한 부분을 분리해줘
   (API 키 없어도 기본 lint+test는 통과해야 함)
```

---

### 📅 2026년 5월 20일 (수)
**목표:** 개발 환경 문서화 완료

```
Copilot 프롬프트:

신규 개발자가 이 프로젝트를 처음 클론했을 때 30분 안에 로컬 실행이 가능하도록
onboarding 체크리스트를 만들어줘.

파일: docs/onboarding.md

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

### 📅 2026년 5월 21일 (목)
**목표:** Phase 0 최종 정리 + Phase 1 준비

```
Copilot 프롬프트:

Phase 1 Django UI 개발을 시작하기 전에 준비 작업을 도와줘.

1. brand/forms.py 폼 클래스 설계:
   - Step1Form: business_type(CharField), keywords(CharField, required=False)
   - Step2Form: selected_vibes(MultipleChoiceField, 최대 4개 선택)
   - Step3Form: target(CharField, widget=Textarea)

2. brand/models.py BrandSession 모델 설계:
   - session_key, business_type, keywords, vibes(JSONField)
   - target, result(JSONField), selected_brand(int), error
   - created_at, updated_at
   - (로그인 전에도 세션으로 상태 유지)

3. brand/services/brand_generator.py 스켈레톤 작성:
   - 함수: generate_brand_identity(business_type, vibes, target, keywords) -> dict
   - 내부적으로 gemini-3-flash-preview 모델 사용
   - 실제 구현은 비워두고 타입 힌트 + docstring만

4. 결과 데이터 구조를 TypedDict로 정의:
   - BrandOption: name, meaning, story, slogan
   - Typography: korean, english, reason
   - Character: name, concept, personality, visual
   - BrandResult: brands(list), typography, character

5. python manage.py makemigrations brand → python manage.py migrate 실행
```

---

### 📅 2026년 5월 22일 (금)

**🏁 마일스톤 M0 달성 — 개발 환경 완성**

```
Copilot 프롬프트:

Phase 0 완료 체크리스트를 만들어줘.
현재 프로젝트 상태를 점검하고 Phase 1 시작 준비가 됐는지 확인해줘.

체크 항목:
- [ ] GitHub Actions CI 정상 동작 (lint + test 통과)
- [ ] 폴더 구조 완성 (모든 __init__.py 존재)
- [ ] .env.example 완성
- [ ] README 로컬 실행 가이드 완성
- [ ] pytest 기본 테스트 5개 이상 통과
- [ ] ruff 경고 0개
- [ ] 커밋 히스토리 정리 (의미있는 커밋 메시지)

부족한 항목이 있으면 오늘 안에 처리할 수 있는 우선순위를 잡아줘.
```

---

---

# PHASE 1 — 패키지 A Django MVP
### 📆 2026.05.25 ~ 2026.07.10 (7주)

---

## WEEK 4 — Step 1·2 UI (5/25 ~ 5/29)

---

### 📅 2026년 5월 25일 (월)
**목표:** Step 1 — 업종 입력 화면 완성  
**태스크:** components/step_input.py 완성

```
Copilot 프롬프트:

brand/views.py의 Step1View와 brand/templates/brand/step1_input.html을 작성해줘.

기술: Django 4.2, Class-Based View, Django Forms, Django Sessions

views.py — Step1View:
- GET: Step1Form 렌더링
- POST: 폼 유효성 검사
  - 성공 시 request.session에 business_type, keywords 저장
    → redirect("step2")
  - 실패 시 에러와 함께 폼 재렌더링
- 세션 키: "brand_step1"

step1_input.html 구성:
1. 진행 바: 5단계 (현재: 1단계 강조, Tailwind CSS 적용)
2. 제목: "어떤 업종 · 서비스인가요?"
3. 설명: "구체적일수록 더 정확한 브랜드를 만들 수 있어요"
4. {{ form.business_type }} — placeholder 랜덤 예시 5종
5. {{ form.keywords }} — placeholder: "예: 따뜻함, 일상, 발견"
6. "다음 →" 버튼 (business_type 2글자 미만이면 비활성화)

Tailwind CSS는 CDN으로 적용:
<script src="https://cdn.tailwindcss.com"></script>
```

---

### 📅 2026년 5월 26일 (화)
**목표:** Step 2 — 감성 태그 선택 화면  
**태스크:** components/step_vibe.py 완성

```
Copilot 프롬프트:

brand/views.py의 Step2View와 brand/templates/brand/step2_vibe.html을 작성해줘.

views.py — Step2View:
- GET: Step2Form 렌더링 (이전 선택 세션에서 복원)
- POST: 폼 유효성 검사
  - selected_vibes 1개 이상, 4개 이하 검증 (clean_selected_vibes)
  - 성공 시 request.session["brand_vibes"] = selected_vibes 저장
    → redirect("step3")
  - 실패 시 에러 메시지와 함께 재렌더링

step2_vibe.html 구성:
1. 진행 바 (현재: 2단계)
2. 제목: "브랜드 감성을 선택해주세요"
3. 설명: "최대 4개까지 선택 가능합니다"
4. 감성 태그 체크박스 그리드 (3열, Tailwind grid):
   따뜻한, 차가운, 모던한, 클래식한, 자연친화적, 럭셔리한,
   미니멀한, 활기찬, 유머러스한, 진지한, 감성적인, 신뢰감있는, 트렌디한, 레트로한
5. 선택 수 실시간 표시 (vanilla JS로 카운터 구현)
6. 4개 초과 시 추가 선택 막기 (JS)
7. 이전/다음 버튼

vanilla JS로 체크박스 최대 4개 제한 로직 포함해줘.
```

---

### 📅 2026년 5월 27일 (수)
**목표:** Step 3 — 타겟 고객 입력 화면  
**태스크:** components/step_target.py 완성

```
Copilot 프롬프트:

brand/views.py의 Step3View와 brand/templates/brand/step3_target.html을 작성해줘.

views.py — Step3View:
- GET: Step3Form 렌더링, 세션에 에러 있으면 표시
- POST: 폼 유효성 검사
  - target 2글자 이상 검증
  - 성공 시 request.session["brand_target"] = target 저장
    → redirect("generating")
  - 실패 시 에러와 함께 재렌더링

step3_target.html 구성:
1. 진행 바 (현재: 3단계)
2. 에러 메시지 영역 (세션에 error 있으면 표시 후 세션에서 삭제)
3. 제목: "주요 타겟 고객은 누구인가요?"
4. 설명: "나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요"
5. {{ form.target }} — Textarea, rows=5
   placeholder: "예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들"
6. 이전 버튼 / "✦ 브랜드 생성" 버튼
```

---

### 📅 2026년 5월 28일 (목)
**목표:** 진행 바 + 앱 메인 라우팅 완성  
**태스크:** app.py 완성 (render_progress + 분기 로직)

```
Copilot 프롬프트:

Django 공통 베이스 템플릿과 진행 바 컴포넌트를 작성해줘.

파일 1: brand/templates/base.html
- <head>에 Tailwind CSS CDN 삽입
- 헤더: "🏷️ NAMETAG · 패키지 A"
- 서브타이틀: "나만의 브랜드 정체성 만들기"
- {% block content %}{% endblock %}
- {% block scripts %}{% endblock %}

파일 2: brand/templates/brand/_progress_bar.html (include용 컴포넌트)
- current_step 컨텍스트 변수를 받아 단계별 스타일 적용
- 단계 레이블: ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "완성"]
- Tailwind로 스타일링:
  - 완료 단계: text-gray-400 line-through
  - 현재 단계: font-bold text-black
  - 미완료 단계: text-gray-300

각 step 템플릿 상단에서
{% include "brand/_progress_bar.html" with current_step=1 %}
방식으로 사용.
```

---

### 📅 2026년 5월 29일 (금)
**목표:** 로컬 실행 + UI 흐름 전체 테스트

```
Copilot 프롬프트:

Django 뷰 흐름을 pytest-django로 테스트해줘.

파일: tests/test_brand_views.py

테스트 케이스:
1. test_step1_get: GET /  → 200, step1_input.html 렌더링
2. test_step1_empty_post: POST / 빈 입력 → 폼 에러, 리다이렉트 없음
3. test_step1_valid_post: POST / 정상 입력 → 세션 저장, step2로 리다이렉트
4. test_step2_max_vibes: POST /step2/ 감성 5개 → 유효성 실패
5. test_step2_valid_post: POST /step2/ 감성 1~4개 → step3로 리다이렉트
6. test_step3_valid_post: POST /step3/ → generating으로 리다이렉트
7. test_session_persistence: Step1 → Step2 → Step3 세션 값 유지 확인

conftest.py:
- @pytest.fixture: client (Django test client)
- @pytest.fixture: session_with_step1 (step1 세션 채워진 상태)

python -m pytest tests/test_brand_views.py -v 실행 방법도 알려줘.
```

---

## WEEK 5 — Gemini API 텍스트 생성 연동 (6/1 ~ 6/5)

---

### 📅 2026년 6월 1일 (월)
**목표:** brand_generator.py — Gemini API 텍스트 생성 구현  
**태스크:** 프롬프트 설계 + API 호출 로직

```
Copilot 프롬프트:

nametag/services/brand_generator.py를 완성해줘.

사용 모델: gemini-3-flash-preview (google-generativeai 패키지)

함수: generate_brand_identity(business_type, vibes, target, keywords) -> dict

시스템 프롬프트:
"당신은 전문 브랜드 디렉터입니다. 사용자의 정보를 바탕으로 초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다. 반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."

유저 프롬프트:
업종/서비스, 브랜드 감성, 타겟 고객, 추가 키워드를 받아서
아래 JSON 구조 요청:
{
  "brands": [{"name","meaning","story","slogan"} × 3],
  "typography": {"korean","english","reason"},
  "character": {"name","concept","personality","visual"}
}

응답은 utils/parser.py의 extract_json()으로 파싱.
validate_brand_result()로 검증.
실패 시 ValueError 발생.

google.generativeai 초기화, 모델 호출, 에러 처리 포함.
```

---

### 📅 2026년 6월 2일 (화)
**목표:** API 응답 캐싱 + 재시도 로직  
**태스크:** Django Redis 캐싱 적용 + 타임아웃 처리

```
Copilot 프롬프트:

brand_generator.py에 아래 기능을 추가해줘.

1. Django Redis 캐싱 적용:
   from django.core.cache import cache

   def cached_generate(business_type, vibes_tuple, target, keywords):
       cache_key = f"brand:{hash((business_type, vibes_tuple, target, keywords))}"
       cached = cache.get(cache_key)
       if cached:
           return cached
       result = generate_brand_identity(business_type, list(vibes_tuple), target, keywords)
       cache.set(cache_key, result, timeout=3600)  # 1시간 TTL
       return result

2. 재시도 로직 (tenacity 라이브러리 사용):
   - 최대 3회 재시도
   - 재시도 간격: 2초, 4초, 8초 (exponential backoff)
   - 재시도 대상: APIError, TimeoutError

3. 타임아웃 설정:
   - API 호출 최대 30초
   - 초과 시 TimeoutError 발생

config/settings/base.py에 Redis 캐시 설정:
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
    }
}
```

---

### 📅 2026년 6월 3일 (수)
**목표:** Step 4 — 로딩 화면 구현

```
Copilot 프롬프트:

Django의 GeneratingView와 generating.html을 만들어줘.

전략: 동기 처리 (Gemini API 호출 → 완료 후 result 페이지로 redirect)

views.py — GeneratingView:
- GET: generating.html 렌더링 + 세션에서 입력값 확인
  - 세션 미완성이면 step1으로 redirect
- POST (AJAX 호출용):
  - 세션의 business_type, vibes, target, keywords 읽기
  - cached_generate() 호출
  - 성공: BrandSession DB 저장, session["result_id"] 저장
    → JsonResponse({"status": "done", "redirect": "/result/"})
  - 실패: session["error"] = 에러 메시지
    → JsonResponse({"status": "error", "redirect": "/step3/"})

generating.html:
1. 로딩 스피너 (Tailwind animate-spin)
2. 4단계 메시지 순차 표시 (JS setInterval, 1.5초 간격):
   "업종 · 키워드 분석 중" → "브랜드 네임 도출 중" → "스토리텔링 작성 중" → "서체 · 캐릭터 설계 중"
3. 페이지 로드 즉시 AJAX POST 요청 → 완료 시 redirect
4. "예상 소요 시간: 10~15초" 안내

CSRF 토큰은 fetch 헤더에 포함해줘:
headers: {"X-CSRFToken": getCookie("csrftoken")}
```

---

### 📅 2026년 6월 4일 (목)
**목표:** API 연동 통합 테스트

```
Copilot 프롬프트:

Gemini API 연동 통합 테스트를 작성해줘.

파일: tests/test_integration.py

테스트 시나리오 (실제 API 호출 없이 mock 사용):
1. 정상 플로우: 입력 → generate_brand_identity() → dict 반환
2. API 타임아웃: TimeoutError 발생 → 재시도 3회 후 ValueError
3. JSON 파싱 실패: 잘못된 JSON 응답 → extract_json 3단계 시도
4. 네트워크 에러: ConnectionError → 에러 메시지 반환

그리고 실제 API 연결 테스트용 스크립트도 만들어줘:
scripts/test_real_api.py
- 실제 GOOGLE_API_KEY로 간단한 브랜드 생성 요청
- 응답 시간, 응답 구조, 파싱 성공 여부 출력
```

---

### 📅 2026년 6월 5일 (금)
**목표:** 에러 처리 체계화

```
Copilot 프롬프트:

API 에러 종류별로 사용자에게 보여줄 에러 메시지를 정의하고,
에러 핸들링 미들웨어를 만들어줘.

파일: nametag/utils/error_handler.py

에러 종류별 메시지:
- TimeoutError: "응답이 지연되고 있어요. 잠시 후 다시 시도해주세요."
- ValueError (JSON 파싱): "결과 형식을 인식하지 못했어요. 다시 시도해주세요."
- ConnectionError: "네트워크 연결을 확인해주세요."
- APIError (400): "입력 내용을 조금 더 구체적으로 작성해보세요."
- APIError (429): "요청이 너무 많아요. 잠시 후 다시 시도해주세요."
- 기타: "알 수 없는 오류가 발생했어요. 다시 시도해주세요."

함수: handle_api_error(error: Exception) -> str
Step 3 에러 표시 영역에서 이 메시지를 활용.
```

---

## WEEK 6 — 결과 화면 구현 (6/8 ~ 6/12)

---

### 📅 2026년 6월 8일 (월)
**목표:** 결과 화면 — 브랜드 네임 선택 + 스토리텔링

```
Copilot 프롬프트:

brand/views.py의 ResultView와 brand/templates/brand/result.html을 작성해줘. (1/2)

views.py — ResultView:
- GET: 세션에서 result_id로 BrandSession DB 조회
  - 없으면 step1으로 redirect
  - result JSON을 컨텍스트로 전달
- POST (브랜드 선택 변경):
  - selected_brand index를 세션에 저장
  - JsonResponse로 선택된 브랜드 데이터 반환 (AJAX용)

result.html 섹션 1 — 브랜드 네임 선택:
- 제목: "브랜드 네임 — 3가지 제안"
- 3개 브랜드 카드 (Tailwind border rounded-xl)
- 카드 클릭 시 selected_brand 변경 (JS + AJAX POST)
- 선택된 카드 하이라이트 (ring-2 ring-black)

섹션 2 — 선택한 브랜드 스토리텔링:
- id="story-section" (JS로 내용 교체)
- 브랜드명 (text-2xl font-semibold)
- meaning (text-sm text-gray-500)
- story (leading-relaxed)
- slogan (italic text-gray-400)

브랜드 카드 클릭 → AJAX → 스토리 섹션 innerHTML 교체 (vanilla JS).
```

---

### 📅 2026년 6월 9일 (화)
**목표:** 결과 화면 — 서체 + 캐릭터 컨셉

```
Copilot 프롬프트:

result.html에 이어서 작성해줘. (2/2)

섹션 3 — 추천 서체:
- 제목: "추천 서체"
- 2열 그리드 (Tailwind grid grid-cols-2 gap-4):
  - 한글: {{ result.typography.korean }} (text-lg font-medium)
  - 영문: {{ result.typography.english }} (text-lg font-medium)
- 선택 이유: {{ result.typography.reason }} (text-sm text-gray-500)

섹션 4 — 브랜드 캐릭터 컨셉:
- 제목: "브랜드 캐릭터 컨셉"
- 카드 (border rounded-xl p-5):
  - 캐릭터명 (text-xl font-semibold)
  - 컨셉 (text-sm text-gray-500)
  - 성격: {{ result.character.personality }}
  - 외형 묘사 (leading-relaxed)

섹션 5 — 이미지 (Phase 1):
- 로고 시안 3개 (img 태그, S3 URL)
- 캐릭터 이미지 1개

섹션 6 — 하단 버튼:
- "↺ 다시 시작하기": href="{% url 'step1' %}" + 세션 초기화 View
- "📄 PDF 다운로드": href="{% url 'brand_pdf' result_id %}" (Phase 2 구현 전까지 disabled)

세션 초기화 View (brand/views.py):
def restart(request):
    keys = ["brand_step1", "brand_vibes", "brand_target", "result_id", "error"]
    for k in keys:
        request.session.pop(k, None)
    return redirect("step1")
```

---

### 📅 2026년 6월 10일 (수)
**목표:** 전체 UI 흐름 통합 테스트 + 스타일 개선

```
Copilot 프롬프트:

현재까지 구현된 Django 앱 전체 UI를 개선해줘.

개선 항목:
1. 일관된 여백: Tailwind의 py-8, mb-6 등 spacing 통일
2. 모바일 반응형: Tailwind의 md: 브레이크포인트 적용 (grid-cols-1 md:grid-cols-3)
3. 색상 일관성: 주요 CTA 버튼은 bg-black text-white rounded-lg 통일
4. 로딩 중 버튼 비활성화: HTML disabled 속성 + JS 처리
5. 세션 만료 처리: 미들웨어로 result_id 없는데 /result/ 접근 시 /step1/ redirect

Django 미들웨어 추가 (brand/middleware.py):
class BrandSessionMiddleware:
    - /result/ 접근 시 세션에 result_id 없으면 /으로 redirect

settings/base.py MIDDLEWARE에 등록.
```

---

### 📅 2026년 6월 11일 (목)
**목표:** 사용성 개선 — placeholder 다양화 + 도움말

```
Copilot 프롬프트:

사용자 경험을 개선하는 기능들을 추가해줘.

1. 예시 자동 입력 버튼:
   step1_input.html에 "예시로 시작해보기" 버튼 추가
   클릭 시 JS로 input 필드에 랜덤 예시 값 자동 입력:
   const examples = ["20대를 위한 감성 소품 셀렉샵", "동네 수제 베이커리", ...]
   document.getElementById("id_business_type").value = examples[random]

2. 입력 가이드 툴팁:
   각 입력 필드 아래에 <details><summary>💡 작성 팁</summary> ... </details> HTML 추가
   - 업종 입력 팁: 구체적인 타겟과 가치 포함 예시
   - 감성 태그 팁: 경쟁사와 반대 방향 감성 고려
   - 타겟 팁: 1명의 구체적인 고객을 상상하기

3. 글자 수 카운터:
   business_type, target 필드 아래에 실시간 카운터 추가 (vanilla JS):
   input.addEventListener("input", () => counter.textContent = input.value.length + " / 200자")
```

---

### 📅 2026년 6월 12일 (금)
**목표:** 코드 정리 + 테스트 커버리지 확인

```
Copilot 프롬프트:

현재까지 작성한 코드의 품질을 점검하고 리팩터링해줘.

1. components/ 폴더의 중복 코드 추출:
   공통으로 쓰이는 버튼 스타일, 섹션 헤더를 
   components/common.py 로 분리

2. services/brand_generator.py 테스트 업데이트:
   현재 구현에 맞게 mock 업데이트
   캐싱 함수도 테스트에 포함

3. 전체 테스트 실행: pytest tests/ -v --tb=short
   실패하는 테스트가 있으면 원인과 수정 방법 알려줘

4. 코드 복잡도가 높은 함수 (10줄 이상)를 찾아서
   분리 또는 단순화 제안해줘
```

---

## WEEK 7 — 이미지 생성 연동 (6/15 ~ 6/19)

---

### 📅 2026년 6월 15일 (월)
**목표:** image_generator.py — Gemini 이미지 생성 구현

```
Copilot 프롬프트:

nametag/services/image_generator.py를 작성해줘.

사용 모델: gemini-3.1-flash-image-preview (google-generativeai 패키지)

함수: generate_logo_concepts(brand_name, vibes, colors) -> list[str]
- 로고 시안 이미지 3종 생성
- 반환: 이미지 base64 문자열 리스트 (또는 임시 파일 경로)

함수: generate_character_image(character_name, visual_description, vibes) -> str
- 캐릭터 이미지 1종 생성
- 반환: 이미지 base64 문자열

이미지 생성 프롬프트 전략:
- 브랜드명, 감성, 컬러를 영문으로 변환해서 프롬프트에 삽입
- 로고: "minimalist logo design, [brand_name], [vibe] style, vector art, white background"
- 캐릭터: "[visual_description], [vibe] mascot character, flat illustration"

에러 처리: 이미지 생성 실패 시 None 반환 (텍스트 결과는 유지)
```

---

### 📅 2026년 6월 16일 (화)
**목표:** 결과 화면에 이미지 표시 추가

```
Copilot 프롬프트:

result.html에 이미지 생성 결과를 표시하는 섹션을 추가해줘.

섹션 추가 위치: 스토리텔링 카드 아래

섹션 — 로고 시안 (result.html):
<section class="mt-8">
  <h2>로고 시안 — AI 제안</h2>
  <p class="text-sm text-gray-400">실제 로고 제작은 전문 디자이너에게 맡기세요. 방향성 참고용입니다.</p>
  <div class="grid grid-cols-3 gap-4 mt-4">
    {% for url in result.logo_urls %}
      <img src="{{ url }}" class="rounded-xl border" alt="로고 시안 {{ forloop.counter }}">
    {% empty %}
      <p class="col-span-3 text-gray-400">이미지 생성에 실패했어요. 텍스트 컨셉을 참고해주세요.</p>
    {% endfor %}
  </div>
</section>

섹션 — 캐릭터 이미지:
{% if result.character_image_url %}
  <img src="{{ result.character_image_url }}" class="mx-auto mt-6 rounded-xl" style="max-width:300px">
{% endif %}

이미지 생성 실패 시 {% empty %} 블록으로 대체 메시지 표시.
```

---

### 📅 2026년 6월 17일 (수)
**목표:** 이미지 생성 비동기 처리 + 캐싱

```
Copilot 프롬프트:

이미지 생성이 텍스트 생성보다 느릴 수 있어서 UX를 개선해줘.

전략: 텍스트 결과 먼저 표시 → 이미지는 별도 AJAX로 요청

구현 방법 (Django):
1. GeneratingView POST: 텍스트만 먼저 생성 후 /result/ redirect
2. result.html: 이미지 영역에 "🎨 로고 시안 생성하기" 버튼 표시
3. 버튼 클릭 → AJAX POST /brand/generate-images/<result_id>/
4. brand/views.py — GenerateImagesView:
   - BrandResult 조회
   - image_generator.py로 로고 3종 + 캐릭터 생성
   - S3 업로드 후 URL을 BrandResult.logo_urls, character_image_url에 저장
   - JsonResponse({"logo_urls": [...], "character_image_url": "..."})
5. JS로 응답 받으면 이미지 태그 동적 삽입

캐싱:
cache_key = f"images:{result_id}"
cache.set(cache_key, image_urls, timeout=86400)  # 24시간
```

---

### 📅 2026년 6월 18일 (목)
**목표:** 이미지 S3 업로드 로직 (선택적 구현)

```
Copilot 프롬프트:

생성된 이미지를 S3에 업로드하는 서비스를 만들어줘.
Phase 2에서 본격 사용하지만, 지금 기반 코드 작성.

파일: nametag/services/storage.py

함수: upload_image(image_bytes: bytes, filename: str) -> str
- boto3로 S3 업로드
- 반환: 퍼블릭 URL (또는 presigned URL)

함수: get_image_url(key: str) -> str
- S3 객체 URL 반환

환경변수: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME

로컬 개발 환경에서는 images/ 폴더에 로컬 저장으로 fallback:
- ENV=dev이면 로컬 저장
- ENV=prod이면 S3 업로드

boto3를 requirements.txt에 추가하는 것도 알려줘.
```

---

### 📅 2026년 6월 19일 (금)
**목표:** 이미지 생성 통합 테스트

```
Copilot 프롬프트:

이미지 생성 기능 전체를 테스트해줘.

파일: tests/test_image_generator.py

테스트:
1. test_logo_generation_mock: API mock으로 로고 3개 반환 확인
2. test_character_generation_mock: 캐릭터 이미지 반환 확인
3. test_image_generation_failure: API 실패 시 None 반환 확인
4. test_prompt_construction: 브랜드명/감성 기반 프롬프트가 올바르게 생성되는지

scripts/test_real_image_api.py:
- 실제 gemini-3.1-flash-image-preview로 테스트 이미지 1개 생성
- 성공 시 test_output.png로 저장
- 실패 시 에러 메시지 출력
```

---

## WEEK 8 — 로딩 UX + 에러 처리 완성 (6/22 ~ 6/26)

---

### 📅 2026년 6월 22일 (월)
**목표:** 로딩 UX 전체 개선

```
Copilot 프롬프트:

Django generating.html의 로딩 경험을 개선해줘.

현재 문제: 텍스트 생성(10~15초) + AJAX 응답 대기 중 빈 화면

개선안:
1. generating.html 애니메이션 개선:
   - JS로 메시지 순차 표시 (1.5초 간격):
     ["업종 · 키워드 분석 중...", "브랜드 네임 도출 중...", "스토리텔링 작성 중...", "서체 · 캐릭터 설계 중..."]
   - Tailwind animate-pulse로 점 애니메이션

2. 진행 시간 표시:
   - JS setInterval로 경과 시간 카운트: "15초 경과"
   - 30초 초과 시 "조금 더 걸리고 있어요..." 메시지 변경

3. 취소 버튼:
   - "취소하고 처음으로" 링크: href="/"
   - 클릭 시 세션 초기화 후 step1으로

4. 성공 후 result 페이지:
   - URL에 ?new=1 파라미터 추가
   - result.html에서 ?new=1 감지 시 Tailwind animate-bounce로 성공 배너 표시
   - "브랜드가 완성됐어요! 🎉" 배너 3초 후 fade out
```

---

### 📅 2026년 6월 23일 (화)
**목표:** 전체 에러 시나리오 대응

```
Copilot 프롬프트:

앱에서 발생 가능한 모든 에러 시나리오를 정리하고 대응 로직을 완성해줘.

에러 시나리오 & 대응:
1. Gemini API 키 없음 → "API 키 설정이 필요해요" + 설정 가이드 링크
2. API 할당량 초과 → "오늘 사용량이 가득 찼어요. 내일 다시 시도해주세요."
3. JSON 파싱 3회 모두 실패 → "다른 표현으로 다시 입력해보세요." + 입력 초기화
4. 이미지 생성 실패 → 텍스트 결과는 유지, "로고 시안 생성에 실패했어요." 안내
5. 세션 상태 손상 → 자동 초기화 + "앱을 새로 시작합니다." 안내
6. 인터넷 연결 없음 → "네트워크 연결을 확인해주세요."

utils/error_handler.py에 모든 에러 타입과 메시지 매핑 딕셔너리로 관리.
```

---

### 📅 2026년 6월 24일 (수)
**목표:** Google Analytics 연동

```
Copilot 프롬프트:

Django 앱에 Google Analytics를 연동해줘.

방법: base.html의 <head>에 GA4 스크립트 직접 삽입

파일: brand/templates/base.html 수정

{% if not debug %}
<script async src="https://www.googletagmanager.com/gtag/js?id={{ GA_MEASUREMENT_ID }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag("js", new Date());
  gtag("config", "{{ GA_MEASUREMENT_ID }}");
</script>
{% endif %}

config/settings/base.py:
GA_MEASUREMENT_ID = env("GA_MEASUREMENT_ID", default="")

config/context_processors.py:
def analytics(request):
    return {"GA_MEASUREMENT_ID": settings.GA_MEASUREMENT_ID}

settings에 context_processors에 추가.

추적할 이벤트:
- page_view: 각 step 진입 시
  event_name: "step_view", step_number: 1~5
- generation_complete: 브랜드 생성 성공 시
  event_name: "generation_complete", duration_seconds: float
- generation_error: 에러 발생 시
  event_name: "generation_error", error_type: str
- image_generated: 이미지 생성 완료 시
- restart: 다시 시작하기 클릭 시

환경변수: GA_MEASUREMENT_ID
개발 환경에서는 GA 비활성화 (ENV=dev)
```

---

### 📅 2026년 6월 25일 (목)
**목표:** 베타 피드백 수집 폼 연동

```
Copilot 프롬프트:

result.html 하단에 베타 피드백 수집 UI를 추가해줘.

위치: result.html 맨 아래

HTML:
<details class="mt-8 border rounded-xl p-4">
  <summary class="cursor-pointer font-medium">💬 이 결과가 도움이 됐나요?</summary>
  <form method="POST" action="{% url 'feedback' %}">
    {% csrf_token %}
    <input type="hidden" name="result_id" value="{{ result.id }}">
    <!-- 별점 1~5 (radio 버튼) -->
    <!-- 좋았던 점 (checkbox) -->
    <!-- 개선 의견 (textarea, maxlength=50) -->
    <button type="submit">제출하기</button>
  </form>
</details>

brand/models.py — Feedback 모델:
class Feedback(models.Model):
    result = models.ForeignKey(BrandResult, on_delete=CASCADE)
    rating = models.IntegerField()
    good_points = models.JSONField(default=list)
    comment = models.TextField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

brand/views.py — FeedbackView (POST):
Feedback.objects.create(...)
→ JsonResponse({"status": "ok"})

brand/urls.py:
path("feedback/", FeedbackView.as_view(), name="feedback")
```

---

### 📅 2026년 6월 26일 (금)
**목표:** 코드 최종 정리 + Streamlit Cloud 배포 준비

```
Copilot 프롬프트:

Railway 배포를 위한 준비를 도와줘.

1. Procfile 작성:
   web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

2. railway.toml 또는 nixpacks 설정:
   [build]
   buildCommand = "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
   startCommand = "gunicorn config.wsgi:application"

3. config/settings/prod.py 완성:
   - DEBUG = False
   - ALLOWED_HOSTS = [env("RAILWAY_PUBLIC_DOMAIN")]
   - STATIC_ROOT = BASE_DIR / "staticfiles"
   - STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
   - MIDDLEWARE에 WhiteNoise 추가

4. .env.example 최종 점검:
   SECRET_KEY=
   GOOGLE_API_KEY=
   DATABASE_URL=
   REDIS_URL=
   AWS_ACCESS_KEY_ID=
   GA_MEASUREMENT_ID=
   STRIPE_SECRET_KEY=

5. 환경 체크 management command (management/commands/check_env.py):
   python manage.py check_env 실행 시 필수 환경변수 누락 여부 확인
```

---

## WEEK 9 — 배포 & QA (6/29 ~ 7/3)

---

### 📅 2026년 6월 29일 (월)
**목표:** Streamlit Cloud 실제 배포

```
Copilot 프롬프트:

Railway 배포 후 발생할 수 있는 문제들을 미리 점검해줘.

체크리스트:
1. python manage.py check --deploy 실행 → 보안 경고 확인
2. 환경변수 누락 시 500 에러 → Railway Variables에 모두 입력됐는지 확인
3. 정적 파일: collectstatic 실행 후 whitenoise 서빙 정상 여부
4. 세션 백엔드: DB 세션 or Redis 세션 (settings 확인)
5. 이미지 생성 메모리: Railway 512MB 기본 플랜 충분한지 확인
6. DB 마이그레이션: Railway 배포 시 자동 migrate 실행 여부

배포 후 smoke test 시나리오:
- 처음 접속 → / 정상 렌더링
- Step 1 → Step 2 → Step 3 → 생성 → 결과 전체 플로우
- 에러 발생 시 → step3으로 redirect 및 에러 메시지
- "다시 시작하기" → 세션 초기화 후 step1으로 이동
- 로그인 → 히스토리 저장 확인
```

---

### 📅 2026년 6월 30일 (화)
**목표:** 성능 최적화

```
Copilot 프롬프트:

Streamlit 앱의 성능을 최적화해줘.

1. 불필요한 리렌더링 방지:
   - st.session_state 변경이 없을 때 st.rerun() 호출 방지
   - 큰 데이터(이미지)는 session_state가 아닌 캐시에 저장

2. 이미지 최적화:
   - base64 이미지 크기 줄이기 (PIL로 리사이즈, max 800px)
   - 이미지 포맷: PNG → WebP 변환 (파일 크기 절반)

3. API 호출 최적화:
   - 같은 입력에 대해 @st.cache_data가 실제로 작동하는지 확인
   - 캐시 히트율 로깅

4. 로딩 속도:
   - 앱 초기 로딩 시간 측정 (목표: 3초 이내)
   - 무거운 import를 지연 로딩으로 변경

PIL 설치: requirements.txt에 Pillow 추가.
```

---

### 📅 2026년 7월 1일 (수)
**목표:** 베타 유저 모집 준비 + 온보딩

```
Copilot 프롬프트:

베타 테스터 30~50명을 모집하고 관리하기 위한 도구를 만들어줘.

1. 베타 접근 코드 시스템:
   - .env에 BETA_CODES=CODE1,CODE2,CODE3 형태로 저장
   - brand/views.py — BetaGateView:
     GET: 코드 입력 폼 렌더링
     POST: 코드 확인 후 request.session["beta_access"] = True
           → redirect("/")
   - brand/middleware.py — BetaAccessMiddleware:
     /beta/ 제외 모든 경로에서 session["beta_access"] 없으면 /beta/로 redirect

2. 대기자 등록 폼:
   - 잘못된 코드 입력 시 → 대기자 등록 폼 표시
   - 이름, 이메일, 업종 입력 → BetaWaitlist 모델에 저장
   - (gspread 연동은 선택: settings에 GOOGLE_SHEETS_KEY 추가)

3. 베타 배너:
   - base.html 상단에 조건부 표시:
   {% if request.session.beta_access %}
   <div class="bg-yellow-50 text-center py-2 text-sm">
     베타 버전 — 피드백을 주시면 커피 기프티콘을 드려요! ☕
   </div>
   {% endif %}
```

---

### 📅 2026년 7월 2일 (목)
**목표:** 사용 데이터 분석 대시보드 (관리자용)

```
Copilot 프롬프트:

Django 관리자 대시보드를 만들어줘.

방법: Django Admin 커스터마이징 + 별도 admin 뷰

1. Django Admin 등록 (brand/admin.py):
   @admin.register(BrandResult)
   class BrandResultAdmin(admin.ModelAdmin):
       list_display = ["id", "user", "business_type", "created_at"]
       list_filter = ["created_at"]
       search_fields = ["business_type", "user__email"]

2. 커스텀 대시보드 뷰 (brand/views.py — AdminDashboardView):
   - @staff_member_required 데코레이터
   - 표시 내용:
     - 오늘 생성 건수: BrandResult.objects.filter(created_at__date=today).count()
     - 누적 생성 건수
     - 가장 많이 선택된 감성 태그 Top 5 (vibes JSON 집계)
     - 베타 피드백 평균 별점: Feedback.objects.aggregate(Avg("rating"))
   - 템플릿: brand/templates/brand/admin_dashboard.html
   - Tailwind로 간단한 카드 UI

3. brand/urls.py 추가:
   path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard")
```

---

### 📅 2026년 7월 3일 (금)
**목표:** QA 완료 + 베타 오픈 준비

```
Copilot 프롬프트:

베타 오픈 전 최종 QA 체크리스트를 만들고 실행해줘.

체크리스트:
기능 테스트:
- [ ] Step 1 → 5 전체 플로우 완주 (5회 반복)
- [ ] 이미지 생성 성공 / 실패 양쪽 확인
- [ ] 에러 발생 → 재시도 정상 동작
- [ ] 다시 시작하기 완전 초기화 확인
- [ ] 베타 코드 시스템 동작 확인
- [ ] 피드백 폼 제출 → CSV 저장 확인
- [ ] 관리자 대시보드 접근 제한 확인

성능 테스트:
- [ ] 생성 평균 소요 시간 측정 (10회)
- [ ] 동시 접속 3명 시뮬레이션 (Streamlit Cloud 한계)

보안:
- [ ] .env 파일 gitignore 확인
- [ ] 관리자 페이지 비밀번호 보호 확인
- [ ] API 키 클라이언트 노출 없음 확인
```

---

## WEEK 10 — 베타 운영 & 피드백 수집 (7/6 ~ 7/10)

---

### 📅 2026년 7월 6일 (월)
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

3. Streamlit Cloud 로그 확인 방법 안내

4. 긴급 버그 대응 프로세스:
   - 심각도 분류 (P0/P1/P2)
   - P0(앱 다운): 즉시 롤백 방법
   - P1(기능 오류): 핫픽스 브랜치 전략
```

---

### 📅 2026년 7월 7일 (화)
**목표:** 베타 피드백 첫 분석 + 긴급 버그 수정

```
Copilot 프롬프트:

베타 유저 피드백 데이터를 분석해줘.

분석 대상: feedback.csv (수집된 피드백)

분석 항목:
1. 별점 분포 (1~5점 각 비율)
2. 좋았던 점 선택 빈도
3. 개선 의견 텍스트 공통 키워드 추출
4. 어느 단계에서 이탈이 많은지 (analytics.csv 기반)
5. 이미지 생성 성공률

결과를 바탕으로:
- 즉시 수정할 버그 우선순위 Top 3
- 다음 Phase에서 반영할 개선사항 목록
를 정리해줘.
```

---

### 📅 2026년 7월 8일 (수)
**목표:** 피드백 기반 긴급 개선

```
Copilot 프롬프트:

베타 피드백 기반으로 가장 많은 불만이 나온 부분을 수정해줘.

예상 수정 항목 (피드백 기반):
1. 생성 결과가 너무 일반적이다 → 프롬프트 구체화
   - 업종별 특화 프롬프트 분기 (음식점/패션/IT/뷰티 등)
   - 감성 태그 조합에 따른 프롬프트 변형

2. 이미지 품질이 아쉽다 → 이미지 프롬프트 개선
   - 더 구체적인 스타일 지시어 추가
   - "negative prompt" 개념 활용

3. 속도가 느리다 → 체감 속도 개선
   - 텍스트 먼저 보여주고 이미지 나중에

위 항목들을 실제 코드 수정으로 반영해줘.
```

---

### 📅 2026년 7월 9일 (목)
**목표:** Phase 1 결과 정리 + Phase 2 설계 시작

```
Copilot 프롬프트:

Phase 1 완료 보고서를 작성하고 Phase 2 설계를 시작해줘.

Phase 1 완료 보고서 (docs/phase1_report.md):
- 달성한 것: 기능 목록
- 베타 지표: 유저 수, 생성 건수, 평균 별점, 완료율
- 발견된 기술 부채 목록
- 다음 Phase로 넘기는 미완성 항목

Phase 2 준비 (FastAPI 전환):
1. FastAPI 프로젝트 구조 설계
   - api/ 폴더 생성 계획
   - 라우터 구조: /api/v1/brand, /api/v1/auth, /api/v1/user
2. 데이터베이스 스키마 초안
   - users, sessions, brand_results 테이블 ERD
3. Supabase Auth 연동 방법 조사
```

---

### 📅 2026년 7월 10일 (금)

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
- [ ] 피드백 CSV 수집 정상

미달성 항목이 있으면 Phase 2 시작 전 1주 연장 여부 판단해줘.

Phase 2 킥오프 체크리스트도 만들어줘:
- FastAPI 개발 환경 세팅 필요 항목
- React 학습 필요 부분 (Streamlit → React 전환)
- Supabase 프로젝트 생성 절차
```

---

---

# PHASE 2 — 서비스화 (회원 & 저장)
### 📆 2026.07.13 ~ 2026.09.18 (10주)

> Phase 2는 FastAPI·React 전환 없이 **Django 하나로 계속 진행**합니다. Django Auth로 회원 기능, Django ORM으로 저장, Django Templates로 화면을 구현합니다.

---

## WEEK 11~12 — FastAPI 백엔드 구축 (7/13 ~ 7/24)

**이 구간 핵심 작업:** Streamlit에서 서버 사이드로 API 호출 이전, DB 초기화

### 📅 2026년 7월 13일 (월) — FastAPI 프로젝트 초기화

```
Copilot 프롬프트:

Django 앱 구조를 확장해줘. (FastAPI 없이 Django만으로 진행)

Phase 2에서 할 일:
1. users 앱에 커스텀 User 모델 추가 (AbstractUser 상속)
2. brand 앱 BrandResult 모델 완성 (user FK 연결)
3. Django 내장 Auth로 회원가입·로그인 구현
4. 로그인 후 생성 결과 자동 저장

users/models.py:
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    plan = models.CharField(max_length=10, default="free")  # free|basic|pro
    created_at = models.DateTimeField(auto_now_add=True)

brand/models.py BrandResult 완성:
- user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- business_type, keywords, vibes(JSONField), target
- result(JSONField), selected_brand(int, default=0)
- logo_urls(JSONField, default=list), character_image_url
- created_at

config/settings/base.py:
AUTH_USER_MODEL = "users.User"

python manage.py makemigrations users brand
python manage.py migrate
```

---

### 📅 2026년 7월 15일 (수) — 데이터베이스 모델 + Alembic

```
Copilot 프롬프트:

PostgreSQL 데이터베이스 모델을 SQLAlchemy로 작성하고
Alembic 마이그레이션을 설정해줘.

테이블:
1. users:
   id (UUID PK), email, created_at, updated_at, plan(free|basic|pro), is_active

2. brand_results:
   id (UUID PK), user_id (FK), created_at,
   business_type, keywords, vibes(JSONB), target,
   result(JSONB), selected_brand_index(int),
   logo_urls(JSONB), character_image_url

3. generation_sessions:
   id (UUID PK), user_id (FK, nullable), created_at,
   completed(bool), error_message, duration_seconds

Alembic 초기화: alembic init alembic
첫 마이그레이션 생성: alembic revision --autogenerate -m "initial"
마이그레이션 실행: alembic upgrade head
```

---

### 📅 2026년 7월 20일 (월) — brand/generate 엔드포인트

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
- logo_urls: list (이미지 생성 완료 후 URL, 미완료 시 null)

에러 응답: 422 (유효성 실패), 503 (API 오류), 500 (서버 오류)
```

---

## WEEK 13~14 — Supabase Auth 연동 (7/27 ~ 8/7)

### 📅 2026년 7월 27일 (월) — 인증 설계

```
Copilot 프롬프트:

Django 내장 Auth로 회원가입·로그인·로그아웃을 구현해줘.

users/views.py:
1. SignupView (CreateView 또는 FormView):
   - UserCreationForm 확장 (이메일 필드 추가)
   - 성공 시 자동 로그인 후 "/" redirect
   - 템플릿: users/signup.html

2. LoginView (django.contrib.auth.views.LoginView 재사용):
   - 템플릿: users/login.html
   - 로그인 성공 후 "/" redirect

3. LogoutView (django.contrib.auth.views.LogoutView 재사용):
   - POST 방식으로 처리 (CSRF 보호)

4. @login_required 데코레이터:
   - users/views.py의 ProfileView (마이페이지)
   - brand/views.py의 HistoryView (생성 히스토리)

users/urls.py:
path("signup/", SignupView.as_view(), name="signup")
path("login/", LoginView.as_view(), name="login")
path("logout/", LogoutView.as_view(), name="logout")
path("profile/", ProfileView.as_view(), name="profile")

config/settings/base.py:
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/users/login/"
```

---

### 📅 2026년 7월 29일 (수) — React 회원가입/로그인 UI

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
- 에러 메시지 표시 (이메일 중복, 비밀번호 오류 등)
- 성공 시 메인 페이지 리다이렉트

Supabase 초기화: src/lib/supabase.ts
```

---

## WEEK 15~16 — React 전환 (8/10 ~ 8/21)

### 📅 2026년 8월 10일 (월) — React 앱 기반 구성

```
Copilot 프롬프트:

Streamlit Wizard UI를 React로 마이그레이션해줘.

프로젝트 초기화: create-react-app 또는 Vite + React 18 + TypeScript

기본 구조:
frontend/
├── src/
│   ├── App.tsx
│   ├── pages/
│   │   ├── Home.tsx        # 메인 랜딩
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
│   │   ├── useGenerate.ts  # 생성 API 호출
│   │   └── useAuth.ts      # 인증 상태
│   └── lib/
│       ├── supabase.ts
│       └── api.ts          # FastAPI 호출

Tailwind CSS 설정, 라우터 (react-router-dom v6) 포함.
```

---

### 📅 2026년 8월 17일 (월) — 생성 API 연동 (React)

```
Copilot 프롬프트:

Django의 GeneratingView AJAX 처리를 완성해줘.

brand/views.py — GeneratingView (POST 처리 완성):
1. 세션에서 business_type, vibes, target, keywords 읽기
2. 로그인 유저라면 request.user를 BrandResult에 연결
3. cached_generate() 호출 (Redis 캐싱 포함)
4. 성공:
   - BrandResult.objects.create(user=user_or_none, ..., result=result)
   - request.session["result_id"] = str(brand_result.id)
   - return JsonResponse({"status": "done", "redirect": "/result/"})
5. 실패:
   - request.session["error"] = handle_api_error(e)
   - return JsonResponse({"status": "error", "redirect": "/step3/"})

generating.html JS 완성:
async function startGeneration() {
    const res = await fetch("/generating/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    });
    const data = await res.json();
    window.location.href = data.redirect;
}
document.addEventListener("DOMContentLoaded", startGeneration);

에러 타입별 메시지는 utils/error_handler.py의 handle_api_error() 활용.
```

---

## WEEK 17~18 — 히스토리 & PDF (8/24 ~ 9/4)

### 📅 2026년 8월 24일 (월) — 생성 히스토리 페이지

```
Copilot 프롬프트:

Django로 히스토리 페이지를 완성해줘.

brand/views.py — HistoryView:
- @login_required
- GET: BrandResult.objects.filter(user=request.user).order_by("-created_at")
  - 페이지네이션: Paginator(queryset, 20)
  - 검색: ?q=검색어 → business_type__icontains + brands JSON 필터
- POST (삭제): BrandResult.objects.filter(id=id, user=request.user).delete()
  → JsonResponse({"status": "deleted"})

brand/templates/brand/history.html:
- 그리드 카드 (Tailwind: grid grid-cols-1 md:grid-cols-3 gap-4)
- 각 카드: 브랜드명, 업종, 생성 날짜, 감성 태그 2~3개 (badge 스타일)
- 카드 클릭 → /result/?id={{ result.id }}
- 삭제 버튼 (AJAX DELETE → 카드 fadeOut)
- 검색 폼 (GET 방식, ?q=)
- 페이지네이션 링크

brand/urls.py 추가:
path("history/", HistoryView.as_view(), name="history")
path("history/delete/<uuid:pk>/", HistoryDeleteView.as_view(), name="history_delete")
```

---

### 📅 2026년 8월 31일 (월) — PDF 다운로드 (WeasyPrint)

```
Copilot 프롬프트:

패키지 A 결과를 PDF로 다운로드하는 기능을 구현해줘.

백엔드: brand/services/pdf_generator.py

도구: WeasyPrint + Jinja2

PDF 구성 (6페이지):
1. 표지: 브랜드명 + 슬로건 + 생성 날짜
2. 브랜드 스토리: story + meaning
3. 서체 가이드: 한글/영문 폰트명 + 사용 이유
4. 캐릭터 컨셉: 이름 + 성격 + 외형
5. 로고 시안: 이미지 3개 (있는 경우)
6. 브랜드 활용 다음 단계 안내

FastAPI 엔드포인트:
GET /brand/pdf/<uuid:result_id>/
- PDF 바이트 반환 (Content-Type: application/pdf)
- 파일명: {브랜드명}_브랜드정체성.pdf

React:
- "PDF 다운로드" 버튼 클릭 시 다운로드 트리거
- 한글 폰트: 나눔고딕 (WeasyPrint 폰트 설정)
```

---

## WEEK 19~20 — QA & 마무리 (9/7 ~ 9/18)

### 📅 2026년 9월 7일 (월) — 통합 테스트

```
Copilot 프롬프트:

Phase 2 전체 기능 통합 테스트를 작성해줘.

테스트 시나리오:
1. 비로그인 생성 → 결과 표시 → 저장 불가 안내
2. 회원가입 → 이메일 인증 → 로그인
3. 로그인 생성 → 결과 자동 저장 → 히스토리 확인
4. 히스토리 → 과거 결과 재열람
5. PDF 다운로드 → 파일 정상 생성
6. 북마크 추가/제거
7. 결과 삭제

FastAPI 테스트: pytest + httpx (AsyncClient)
React 테스트: pytest-django 기본 스모크 테스트
```

---

### 📅 2026년 9월 18일 (금)

**🏁 마일스톤 M2 달성 — 회원/저장 기능 완성**

```
Copilot 프롬프트:

Phase 2 완료 체크리스트 확인:
- [ ] FastAPI + PostgreSQL 정상 동작
- [ ] Supabase Auth 이메일/Google 로그인
- [ ] 생성 결과 자동 저장
- [ ] 히스토리 목록 + 재열람
- [ ] PDF 다운로드 (한글 폰트 정상)
- [ ] Railway 단일 배포 (Django + gunicorn, 프론트·백엔드 통합)
- [ ] 신규 회원 100명 목표

Phase 3 (Stripe 결제) 킥오프 준비:
- Stripe 계정 생성 + 사업자 정보 등록
- 구독 플랜 구성 계획 (무료/Basic/Pro 가격 확정)
```

---

---

# PHASE 3 — 수익화 (구독 & 결제)
### 📆 2026.09.21 ~ 2026.11.27 (10주)

---

## WEEK 21~23 — Stripe 결제 연동 (9/21 ~ 10/9)

### 📅 2026년 9월 21일 (월) — Stripe 초기 설정

```
Copilot 프롬프트:

Stripe 결제 시스템을 설정해줘.

1. 구독 플랜 정의 (Stripe 대시보드 설정 가이드):
   - Free: 월 2회 생성, 히스토리 5개
   - Basic: 월 9,900원, 월 10회 생성, 히스토리 무제한, PDF 다운로드
   - Pro: 월 29,900원, 무제한 생성, 패키지 B·C·D 포함, 이미지 생성 포함

2. 백엔드 설정:
   pip install stripe
   환경변수: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
   STRIPE_PRICE_BASIC_ID, STRIPE_PRICE_PRO_ID

3. payments/views.py:
   - POST /payments/create-checkout-session/
   - POST /payments/webhook/
   - GET /payments/subscription-status/
   - POST /payments/cancel-subscription/

Stripe Checkout 사용 (커스텀 결제 UI 최소화).
```

---

### 📅 2026년 9월 28일 (월) — Webhook 처리

```
Copilot 프롬프트:

Stripe Webhook 처리 로직을 완성해줘.

파일: payments/views.py (webhook 엔드포인트)

처리할 이벤트:
1. checkout.session.completed → 구독 활성화, users.plan 업데이트
2. invoice.payment_succeeded → 갱신 성공, 영수증 이메일 발송
3. invoice.payment_failed → 결제 실패, 유저에게 알림 이메일
4. customer.subscription.deleted → 구독 취소, plan=free 다운그레이드

Webhook 보안:
- stripe.Webhook.construct_event()로 서명 검증
- STRIPE_WEBHOOK_SECRET으로 위조 방지

이메일 발송: Resend API
- 구독 성공 이메일 템플릿
- 결제 실패 이메일 (카드 업데이트 링크 포함)
- 구독 취소 확인 이메일

환경변수: RESEND_API_KEY
```

---

## WEEK 24~26 — 플랜별 기능 제한 (10/12 ~ 10/30)

### 📅 2026년 10월 12일 (월) — 사용량 제한 (Redis)

```
Copilot 프롬프트:

구독 플랜별 기능 제한을 Redis 카운터로 구현해줘.

파일: api/services/usage_limiter.py

플랜별 한도:
- free: 월 2회 생성
- basic: 월 10회 생성
- pro: 무제한

함수: check_usage_limit(user_id: str, plan: str) -> bool
- Redis 키: usage:{user_id}:{YYYY-MM}
- 월초에 자동 리셋 (TTL: 월말까지)
- 한도 초과 시 False 반환

함수: increment_usage(user_id: str) -> int
- 생성 성공 시 카운터 증가
- 현재 사용량 반환

FastAPI 미들웨어에서 generate 엔드포인트 호출 전 체크.
한도 초과 시 HTTP 429 + 업그레이드 안내 메시지.

Redis 연결: redis-py, 환경변수 REDIS_URL.
```

---

### 📅 2026년 10월 19일 (월) — 구독 관리 UI (React)

```
Copilot 프롬프트:

구독 관리 페이지를 React로 만들어줘.

파일: src/pages/Subscription.tsx

UI 구성:
1. 현재 플랜 표시 (배지 + 기능 목록)
2. 플랜 비교 표 (Free / Basic / Pro)
   - 각 플랜별 기능 체크리스트
   - 현재 플랜 하이라이트
3. 업그레이드 버튼 → Stripe Checkout으로 이동
4. 이번 달 사용량 표시 (n회 / 한도)
5. 구독 취소 버튼
   - 취소 확인 모달 (취소 이유 선택)
   - 취소 시 "다음 결제일까지 유지" 안내
6. 영수증 내역 (최근 6개월)

결제 성공 후 돌아올 때: ?success=true 파라미터로 성공 메시지 표시.
```

---

## WEEK 27~28 — 온보딩 & 분석 (11/2 ~ 11/13)

### 📅 2026년 11월 2일 (월) — 신규 가입 온보딩 플로우

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
   - Step 2에서 5분 이상 머물면: "어려우세요? 예시로 시작해보세요!" 팝업
   - 결과 화면에서 닫기 시: "결과를 저장하시겠어요?" 다이얼로그

이메일 템플릿은 HTML 형식으로 작성해줘.
```

---

### 📅 2026년 11월 9일 (월) — PostHog 분석 연동

```
Copilot 프롬프트:

PostHog로 사용자 행동 분석을 연동해줘.

1. React 클라이언트 설정:
   npm install posthog-js
   src/lib/analytics.ts에 초기화

2. 추적할 이벤트:
   - $pageview: 페이지 이동마다 자동
   - generation_started: 생성 버튼 클릭
   - generation_completed: 생성 성공 (duration_ms, plan 포함)
   - generation_failed: 생성 실패 (error_type)
   - image_generated: 이미지 생성 완료
   - plan_upgraded: 구독 업그레이드 (from_plan, to_plan)
   - pdf_downloaded: PDF 다운로드
   - step_abandoned: 특정 단계에서 이탈

3. 사용자 식별:
   로그인 시 posthog.identify(user_id, {email, plan, created_at})

4. 퍼널 분석 설정 (PostHog 대시보드 가이드):
   Step1 진입 → Step3 완료 → 생성 성공 → PDF 다운로드
```

---

## WEEK 29~30 — QA & 수익 검증 (11/16 ~ 11/27)

### 📅 2026년 11월 16일 (월) — 결제 전체 테스트

```
Copilot 프롬프트:

Stripe 결제 전체 플로우를 테스트해줘.

Stripe 테스트 카드 번호: 4242 4242 4242 4242

테스트 시나리오:
1. 무료 → Basic 업그레이드 → 결제 성공 → plan 업데이트 확인
2. 결제 실패 (4000 0000 0000 0002 카드) → 에러 처리
3. Basic → Pro 업그레이드
4. 구독 취소 → 다음 결제일까지 Pro 유지 확인
5. Webhook 서명 위조 시도 → 거부 확인
6. 월 사용량 한도 도달 → 업그레이드 안내 표시

테스트 자동화:
pytest로 webhook 이벤트 시뮬레이션 테스트 작성
stripe.Webhook.construct_event() mock 활용
```

---

### 📅 2026년 11월 27일 (금)

**🏁 마일스톤 M3 달성 — 수익 발생 시작**

```
Copilot 프롬프트:

Phase 3 완료 보고서 (docs/phase3_report.md):
- MRR (Monthly Recurring Revenue) 현황
- 플랜별 유저 분포 (Free/Basic/Pro)
- 유료 전환율
- Churn Rate (구독 취소율)
- 월 생성 건수 vs 한도 도달 비율

Phase 4 (패키지 B·C·D) 킥오프 준비:
- 패키지 B 프롬프트 설계 초안
- WeasyPrint PDF 템플릿 와이어프레임
- S3 PDF 저장 구조 설계
```

---

---

# PHASE 4 — 패키지 B·C·D 가이드 제안서
### 📆 2026.11.30 ~ 2027.03.05 (15주)

---

## WEEK 31~35 — 패키지 B: 브랜드 키트 가이드 (11/30 ~ 1/2)

### 📅 2026년 11월 30일 (월) — 패키지 B 프롬프트 설계

```
Copilot 프롬프트:

패키지 B (브랜드 키트 가이드) 프롬프트를 설계해줘.

패키지 A 결과를 컨텍스트로 받아서 브랜드 키트 가이드를 생성.

입력 데이터:
- 브랜드명, 슬로건, 스토리
- 선택한 감성 태그
- 추천 서체 (한글/영문)
- 캐릭터 컨셉

생성할 내용 (JSON 구조):
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
  "logo_usage_rules": ["규칙1", "규칙2", ...],
  "application_examples": [
    {"item": "명함", "description": "..."},
    {"item": "봉투", "description": "..."},
    {"item": "패키지", "description": "..."}
  ]
}

모델: gemini-3-flash-preview
파일: api/services/package_b_generator.py
```

---

### 📅 2026년 12월 7일 (월) — 패키지 B PDF 템플릿

```
Copilot 프롬프트:

패키지 B 브랜드 키트 가이드 PDF 템플릿을 만들어줘.

도구: Jinja2 HTML 템플릿 + WeasyPrint

파일: api/templates/package_b.html

페이지 구성 (6~8페이지):
1. 표지: 브랜드명 + "브랜드 키트 가이드" + 날짜
2. 컬러 팔레트: 5가지 색상 칩 + HEX 코드 + 사용 맥락
3. 서체 가이드: 폰트명 + 웨이트 + 사용 예시 텍스트
4. 로고 사용 규칙: 텍스트 목록 (이미지 없이)
5. 적용 예시 — 명함: 레이아웃 설명
6. 적용 예시 — 디지털: SNS 프로필 가이드
7. 다음 단계 안내

스타일:
- 브랜드 컬러를 동적으로 적용 (Jinja2 변수)
- 나눔고딕 한글 폰트 임베딩
- A4 세로, 여백 25mm
- 페이지 번호

WeasyPrint 한글 폰트 설정 방법도 포함해줘.
```

---

### 📅 2026년 12월 14일 (월) — 패키지 B API 엔드포인트 + S3 저장

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
pdfs/
├── package_a/{user_id}/{result_id}.pdf
├── package_b/{user_id}/{result_id}.pdf

DB 테이블 추가: package_results
- id, user_id, brand_result_id, package_type(A|B|C|D)
- content(JSONB), pdf_url, created_at

플랜 제한: Basic 이상만 패키지 B 이용 가능.
```

---

### 📅 2026년 12월 21일 (월) — 패키지 B React UI

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
4. 완료 후 미리보기 섹션:
   - 컬러 팔레트 (색상 칩 5개)
   - 서체 이름 표시
   - "PDF 전체 다운로드" 버튼
5. 이미 생성된 경우: 이전 결과 재다운로드 버튼

파일: src/components/PackageB/PackageBSection.tsx
```

---

### 📅 2026년 12월 28일 (월) — 패키지 B QA + 베타 출시

```
Copilot 프롬프트:

패키지 B 전체 테스트 및 베타 출시 준비를 해줘.

테스트:
1. 다양한 업종별 브랜드 키트 생성 (10종)
   - 카페, 패션, IT, 뷰티, 음식점, 스튜디오, 학원, 반려동물, 인테리어, 피트니스
2. 각 결과에서 PDF 품질 확인:
   - 컬러 팔레트 HEX 코드 정확도
   - 서체 이름 현실성 (실제 존재하는 폰트인지)
   - 한글 폰트 깨짐 없음
   - 로고 사용 규칙 내용 유용성
3. S3 업로드 + 다운로드 URL 동작
4. 플랜 제한 (Free 계정으로 접근 시도 → 차단)

베타 출시 공지:
기존 베타 유저 이메일로 패키지 B 출시 안내 + 무료 체험 쿠폰.
```

---

## WEEK 36~40 — 패키지 C: 웹/앱 가이드 (1/5 ~ 2/6)

### 📅 2027년 1월 5일 (월) — 패키지 C 프롬프트 설계

```
Copilot 프롬프트:

패키지 C (웹/앱 페이지 가이드) 프롬프트를 설계해줘.

패키지 A + B 결과를 컨텍스트로 받아서 웹/앱 구성 가이드 생성.

생성할 내용 (JSON):
{
  "landing_page_structure": [
    {"section": "히어로", "content": "...", "copy_guide": "..."},
    {"section": "문제 제기", "content": "...", "copy_guide": "..."},
    {"section": "해결책", "content": "...", "copy_guide": "..."},
    {"section": "사회적 증거", "content": "...", "copy_guide": "..."},
    {"section": "CTA", "content": "...", "copy_guide": "..."}
  ],
  "ui_style_guide": {
    "button_style": "...",
    "card_style": "...",
    "spacing": "...",
    "color_application": "..."
  },
  "mobile_strategy": "...",
  "seo_keywords": ["키워드1", "키워드2", ...],
  "cta_copies": ["CTA 문구1", "CTA 문구2", "CTA 문구3"]
}

파일: api/services/package_c_generator.py
모델: gemini-3-flash-preview
```

---

### 📅 2027년 1월 12일 (월) — 패키지 C PDF 템플릿 + API

```
Copilot 프롬프트:

패키지 C 웹/앱 가이드 PDF 템플릿과 API를 만들어줘.

PDF 구성 (8~10페이지):
1. 표지
2. 랜딩페이지 구조도 (섹션별 텍스트 다이어그램)
3. 히어로 섹션 가이드 (카피 + 구성 설명)
4. 핵심 섹션별 카피 가이드 (3~4개 섹션)
5. UI 스타일 가이드 (버튼, 카드, 간격)
6. 컬러/폰트 웹 적용 기준 (패키지 B 연계)
7. 모바일 전략
8. SEO 키워드 목록
9. 다음 단계 (개발자/디자이너에게 전달할 체크리스트)

API: POST /api/v1/package/c/generate
플랜 제한: Pro 플랜 이상 (또는 단건 구매 옵션)

단건 구매: 19,900원
Stripe payment_intent로 구현 (구독 아닌 일회성 결제)
```

---

### 📅 2027년 1월 26일 (월) — 패키지 C QA + 출시

```
Copilot 프롬프트:

패키지 C 출시 전 최종 점검을 해줘.

품질 기준:
1. 랜딩페이지 구조가 업종에 맞게 다른지 (카페 vs IT SaaS 비교)
2. 카피 가이드가 실제 쓸 수 있는 수준인지
3. SEO 키워드가 실제 검색량 있는 키워드인지
4. 모바일 전략이 구체적인지 (추상적 조언 → 구체적 가이드)

개선이 필요한 부분 프롬프트 수정.

출시 후 마케팅:
- 패키지 C 샘플 PDF 공개 (랜딩페이지에 다운로드)
- SNS 공유: "AI가 내 브랜드 웹사이트 기획서 써줬어요"
```

---

## WEEK 41~45 — 패키지 D: 인테리어 가이드 (2/9 ~ 3/5)

### 📅 2027년 2월 9일 (월) — 패키지 D 프롬프트 설계

```
Copilot 프롬프트:

패키지 D (실내 인테리어 가이드) 프롬프트를 설계해줘.

업종별 인테리어 패턴 매핑 (이 매핑을 프롬프트에 포함):
- 카페: 좌석 밀도, 조명 온도, 소재(우드/패브릭), 동선
- 오피스: 집중존/협업존 구분, 브랜드 컬러 포인트월
- 쇼룸/팝업: 상품 진열 동선, 포토존 설계
- 뷰티샵: 조명 균일도, 위생 소재, 거울 배치
- 피트니스: 에너지 컬러, 거울/조명, 운동존 분리

생성할 내용 (JSON):
{
  "space_concept": "공간 컨셉 한 줄",
  "mood_keywords": ["키워드1", "키워드2", "키워드3"],
  "color_application": {
    "wall": "벽면 컬러 가이드",
    "floor": "바닥재 가이드",
    "accent": "포인트 컬러 활용"
  },
  "material_guide": [{"material": "", "usage": "", "reason": ""}],
  "lighting_plan": "조명 계획",
  "furniture_direction": "가구·소품 방향성",
  "reference_keywords": ["무드보드 검색 키워드"]
}

파일: api/services/package_d_generator.py
```

---

### 📅 2027년 2월 16일 (월) — 패키지 D PDF + 통합 QA

```
Copilot 프롬프트:

패키지 D PDF 템플릿과 전체 B·C·D 통합 QA를 해줘.

패키지 D PDF (8~10페이지):
1. 표지 + 공간 컨셉 소개
2. 무드 키워드 + 레퍼런스 검색 가이드
3. 컬러 적용 가이드 (벽/바닥/포인트)
4. 소재·질감 가이드
5. 조명 계획
6. 가구·소품 방향성
7. 공간별 적용 예시 (입구/메인공간/세부공간)
8. 인테리어 업체 의뢰 전 체크리스트

B·C·D 통합 QA:
- A→B→C→D 데이터 흐름 전체 테스트
- 각 패키지 PDF에 브랜드 일관성 확인
  (같은 브랜드의 B/C/D 컬러, 서체 일치)
- 모든 PDF 한글 폰트 확인
- S3 저장 + URL 만료 정책 확인
```

---

### 📅 2027년 3월 5일 (금)

**🏁 마일스톤 M4 달성 — 패키지 B·C·D 가이드 제안서 완성**

```
Copilot 프롬프트:

Phase 4 완료 후 MRR 업데이트 분석:
- 패키지 B/C/D 추가 후 MRR 변화
- 패키지별 이용률 비교
- 가장 인기 있는 패키지
- 다음 Phase (B2B 중개) 전환 판단 지표

Phase 5 킥오프 준비:
- 디자인 파트너 모집 전략
- Stripe Connect 사전 신청 가이드
- 파트너 온보딩 폼 와이어프레임
```

---

---

# PHASE 5 — B2B 중개 플랫폼
### 📆 2027.03.08 ~ 2027.04.24 (7주)

---

## WEEK 46~48 — 파트너 등록 & 매칭 (3/8 ~ 3/26)

### 📅 2027년 3월 8일 (월) — 파트너 DB 모델 + 등록 API

```
Copilot 프롬프트:

B2B 디자인 파트너 시스템을 구축해줘.

DB 테이블: design_partners
- id, name, business_name, email, phone
- specialties(JSONB): ["브랜딩", "웹디자인", "패키지디자인"]
- price_range: {min: int, max: int} (만원 단위)
- portfolio_urls(JSONB): URL 목록
- rating: float, review_count: int
- is_verified: bool (관리자 승인)
- created_at

DB 테이블: quote_requests
- id, user_id, partner_id, brand_result_id
- budget_min, budget_max
- requirements: text
- status: pending|responded|contracted|completed|cancelled
- created_at

FastAPI:
POST /api/v1/partners/register (파트너 신청)
GET /api/v1/partners/search (감성/예산 기반 검색)
POST /api/v1/partners/{id}/quote-request (견적 요청)
```

---

### 📅 2027년 3월 15일 (월) — 매칭 로직 + 파트너 대시보드

```
Copilot 프롬프트:

파트너 매칭 알고리즘과 파트너용 대시보드를 만들어줘.

매칭 알고리즘:
함수: match_partners(brand_result, budget) -> list[Partner]
- 감성 태그와 파트너 specialties 겹치는 수로 점수
- 예산 범위 필터
- 평점 가중치 (rating * 0.3)
- 최대 5개 추천

파트너 대시보드 (별도 페이지):
- 신규 견적 요청 목록
- 견적 응답 폼 (예상 금액, 포트폴리오 첨부, 메시지)
- 진행 중 프로젝트
- 완료 프로젝트 + 리뷰
- 정산 내역

파트너 알림:
- 새 견적 요청 시 이메일 알림 (Resend)
- 계약 성사 시 알림
```

---

## WEEK 49~51 — Stripe Connect 정산 (3/29 ~ 4/16)

### 📅 2027년 3월 29일 (월) — Stripe Connect 설정

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

사업자 등록 + Stripe Connect 심사 준비 필요 사항도 정리해줘.
```

---

### 📅 2027년 4월 5일 (월) — 리뷰 & 신뢰 시스템

```
Copilot 프롬프트:

파트너 리뷰 및 신뢰도 시스템을 만들어줘.

DB 테이블: partner_reviews
- id, user_id, partner_id, quote_request_id
- rating(1~5), title, content
- is_verified(계약 완료 후만 작성 가능)
- created_at

API:
POST /api/v1/reviews (리뷰 작성, 계약 완료 후만 가능)
GET /api/v1/partners/{id}/reviews (리뷰 목록)
POST /api/v1/reviews/{id}/report (신고)

파트너 평점 자동 계산: 리뷰 작성 시 design_partners.rating 업데이트

관리자 기능:
- 신고된 리뷰 검토 대기열
- 파트너 경고/정지/퇴출 처리
- 허위 리뷰 판별 기준 (같은 IP, 가입 직후 리뷰 등)

UI: 파트너 카드에 별점 + 리뷰 수 표시
```

---

## WEEK 52 — 최종 QA & 런칭 (4/20 ~ 4/24)

### 📅 2027년 4월 20일 (월) — 전체 시스템 통합 QA

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
- [ ] 환불 시나리오

B2B 중개:
- [ ] 파트너 등록 + 승인
- [ ] 유저 → 파트너 견적 요청
- [ ] 계약 → Stripe Connect 정산
- [ ] 리뷰 작성

보안:
- [ ] 인증 없이 보호 API 접근 시도 → 401
- [ ] 타인 데이터 접근 시도 → 403
- [ ] SQL 인젝션 기본 테스트
```

---

### 📅 2027년 4월 24일 (금)

**🏁 마일스톤 M5 달성 — 전체 서비스 완성 🎉**

```
Copilot 프롬프트:

Name Tag 서비스 런칭 체크리스트 최종 확인:

서비스:
- [ ] 모든 패키지 A·B·C·D 정상 동작
- [ ] B2B 중개 플랫폼 동작
- [ ] 결제 시스템 (구독 + 단건 + Connect)

인프라:
- [ ] Railway 단일 서버 배포 (Django + gunicorn)
- [ ] 커스텀 도메인 연결
- [ ] PostgreSQL RDS 또는 Railway DB
- [ ] Redis Cloud 연결
- [ ] S3 PDF 저장
- [ ] CloudFront CDN 연결

모니터링:
- [ ] Sentry 에러 추적 연동
- [ ] PostHog 대시보드 설정
- [ ] Stripe 대시보드 정산 확인
- [ ] 서버 업타임 모니터링 (UptimeRobot)

런칭 후 첫 주 모니터링 계획도 만들어줘.
```

---

---

## 📊 주간 루틴 (매주 반복)

| 요일 | 루틴 |
|------|------|
| **월요일** | 주간 계획 점검, 이전 주 미완성 항목 이월 |
| **화~목** | 본격 개발 (하루 4~6시간) |
| **금요일** | 코드 리뷰, 커밋 정리, 주간 회고 |

---

## 🆘 막혔을 때 Copilot에게 물어보는 프롬프트

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

*최종 업데이트: 2026.04.30 | 버전: v1.0*