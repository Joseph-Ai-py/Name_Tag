# 🏷️ NameTag - AI 브랜드 정체성 생성기

**Version:** v0.1.0 (React + FastAPI)

네임텍(NameTag)은 초기 스타트업 및 1인 기업을 위한 **AI 기반 브랜드 정체성 설계 플랫폼**입니다.

## 🎨 브랜드 정체성

NameTag는 **Fluid Kinetic UI** 디자인 철학으로 구성되어 있습니다:
- **로고**: 역동적이고 현대적인 디자인 (`logo/logo_black.png`, `logo/logo_white.png`)
- **색상**: Cyan (#00D9FF) → Purple (#A855F7) → Magenta (#EC4899) 네온 그라데이션
- **폰트**: Pretendard (한글) + Inter (영문)
- **다크모드**: 시스템 설정 기반 + 수동 토글 가능

## ✨ 주요 기능

✅ **브랜드 네이밍** - AI가 생성한 3가지 이름 제안  
✅ **스토리텔링** - 감정 있는 브랜드 의미와 슬로건  
✅ **서체 추천** - 한글/영문 폰트 매칭  
✅ **캐릭터 설계** - 브랜드 persona 제안  
✅ **단계형 마법사** - 직관적인 5단계 입력 프로세스  

## 🛠️ 기술 스택

| 계층 | 기술 |
|------|------|
| **Frontend** | React 18 + TypeScript + Tailwind CSS + Vite |
| **Backend** | FastAPI + Python 3.11 |
| **상태 관리** | Zustand + TanStack Query |
| **AI/LLM** | Google Gemini API (gemini-1.5-pro) |
| **배포** | Docker + Docker Compose |

## 📁 프로젝트 구조

```
Name_Tag/
├── frontend/                    # React 프론트엔드 (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Wizard/         # Step 1~3 입력 컴포넌트
│   │   │   ├── Result/         # 결과 표시
│   │   │   └── Layout/         # Header/Footer
│   │   ├── hooks/              # useGenerate, useWizard
│   │   ├── stores/             # Zustand 상태 관리
│   │   ├── lib/                # API 클라이언트
│   │   ├── pages/              # 페이지 컴포넌트
│   │   ├── types/              # TypeScript 타입 정의
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/                 # 로고 및 정적 파일 (로고는 Docker에서 자동 복사)
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   └── Dockerfile
│
├── backend/                     # FastAPI 백엔드
│   ├── main.py                 # 진입점
│   ├── routers/
│   │   └── brand.py            # 브랜드 생성 엔드포인트
│   ├── services/
│   │   └── brand_generator.py  # Gemini API 호출
│   ├── utils/
│   │   └── parser.py           # JSON 파싱
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── logo/                        # 브랜드 로고
│   ├── logo_black.png          # 검은색 로고
│   └── logo_white.png          # 흰색 로고
│
├── app.py                       # 기존 Streamlit (레거시)
├── docker-compose.yml           # 로컬 개발 + 배포
├── MIGRATION.md                 # 마이그레이션 가이드
├── DEPLOYMENT.md                # 배포 가이드
└── .env.example

```

## 🚀 빠른 시작 (초보자 추천)

### 🐳 **방법 1: Docker Compose 사용 (가장 간단함!)**

**Docker란?** 컴퓨터에 설치하지 않고도 프로그램을 마치 "보따리 상자"처럼 실행할 수 있게 해주는 도구입니다. Backend와 Frontend를 따로 설정할 필요 없이 한 번에 실행됩니다!

#### ⚙️ 사전 준비: Docker Desktop 설치

**1단계: Docker Desktop 다운로드**

👉 **[Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop)** 클릭

- **Windows**: "Docker Desktop for Windows" 다운로드
- **Mac**: "Docker Desktop for Mac" 다운로드

**2단계: Docker Desktop 설치**

다운로드된 파일을 실행하고 설치 마법사를 따라 진행합니다.

**3단계: 설치 확인**

새로운 터미널(명령 프롬프트)을 열고 다음 명령을 입력합니다:

```bash
docker --version
```

✅ 다음과 같이 버전이 보이면 설치 완료:
```
Docker version 25.x.x, build xxxxxxx
```

#### 🚀 실행 방법

**1단계: 터미널 열기**

Windows:
- 시작 메뉴 → "명령 프롬프트" 검색 → 열기

또는

- 프로젝트 폴더에서 마우스 우클릭 → "여기서 터미널 열기" (Windows 11)

**2단계: Docker Desktop 실행 중인지 확인**

Docker Desktop 애플리케이션이 실행 중이어야 합니다. (시스템 트레이에 고래 아이콘 확인)

**3단계: 프로젝트 폴더로 이동**

터미널에 다음을 입력합니다:

```bash
cd Name_Tag
```

**4단계: Docker로 애플리케이션 시작**

```bash
docker-compose up --build
```

이 명령을 입력하면 자동으로:
- ✅ Python 환경 설정
- ✅ Node.js 환경 설정
- ✅ 필요한 패키지 설치
- ✅ Backend 실행 (포트 8000)
- ✅ Frontend 실행 (포트 3000)

**⏳ 첫 실행은 3-5분 소요됩니다.** (Docker 이미지 다운로드 때문)

**5단계: 완료 확인**

다음과 같은 메시지가 보이면 성공입니다:

```
backend-1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend-1  |  INFO  Accepting connections at http://localhost:3000
```

**6단계: 브라우저에서 접속**

브라우저를 열고 다음 주소로 접속합니다:

```
http://localhost:3000
```

✅ NameTag 화면이 보이면 성공!

**중지 방법**: 터미널에서 `Ctrl+C` 누르기

**다시 시작하기**: 같은 터미널에서 `docker-compose up` 명령 실행 (--build 제거)

#### 🔧 Docker 문제 해결

**Q: Docker Desktop을 켰는데도 "Docker daemon not running" 오류가 나요**
- Docker Desktop 애플리케이션을 다시 시작해보세요.
- 시스템 트레이(화면 우측 하단)에서 Docker 아이콘을 확인하세요.

**Q: 포트 3000이 이미 사용 중이라는 오류가 나요**
- 다른 프로그램이 포트를 사용 중입니다.
- 다음 명령으로 강제 중지합니다:
```bash
docker-compose down -v
```
- 그 후 다시 `docker-compose up` 시도

**Q: 이미지 다운로드가 너무 오래 걸려요**
- 네트워크 상태를 확인하세요.
- 중단했다면 `docker-compose up` 다시 실행하면 이어서 진행됩니다.

**Q: Docker 완전히 제거하고 싶어요**
```bash
docker-compose down -v
```

---

### 💻 **방법 2: 로컬에서 실행 (고급 사용자)**

직접 Backend와 Frontend를 실행하고 싶은 경우 이 방법을 사용합니다.

#### 요구사항
- Python 3.11 이상 ([다운로드](https://www.python.org/downloads/))
- Node.js 20 이상 ([다운로드](https://nodejs.org/))

#### ⚙️ 사전 준비: 환경 변수 설정

프로젝트 루트 폴더에 `.env` 파일을 생성하고 아래 내용을 입력합니다:

```env
GEMINI_API_KEY=your api key
GEMINI_MODEL=gemini-3-flash-preview
```

> **📝 참고**: `backend/.env` 파일을 확인하여 이 내용이 맞는지 확인하세요.

#### 🔴 Step 1: Backend 실행 (터미널 1 열기)

**Windows 사용자:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**macOS/Linux 사용자:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

✅ 다음과 같은 메시지가 보이면 성공:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 🟢 Step 2: Frontend 실행 (새로운 터미널 2 열기)

**새로운 터미널 창을 열고** 아래를 실행합니다:

```bash
cd frontend
npm install
npm run dev
```

✅ 다음과 같은 메시지가 보이면 성공:
```
  VITE v5.x.x  ready in xx ms

  ➜  Local:   http://localhost:5173/
```

#### 🟡 Step 3: 브라우저에서 접속

**http://localhost:5173** 을 열어서 애플리케이션을 사용합니다.

> **🎯 팁**: Backend와 Frontend를 동시에 실행해야 합니다. 각각 다른 터미널에서 실행하세요!

## 📡 API 엔드포인트

### ❓ 자주 묻는 질문 (FAQ)

**Q1: 어떤 방법을 선택해야 하나요?**
- Docker 설치했으면 👉 **방법 1 (Docker)** 추천 (가장 간단함)
- Docker 모르고 Python/Node.js 설치했으면 👉 **방법 2 (로컬 실행)**

**Q2: Docker와 로컬 중 뭐가 다른가요?**
- Docker: "검은 상자"처럼 모든 설정이 되어 있음. 버튼만 누르면 끝!
- 로컬: 직접 Python, Node.js를 설치하고 수동으로 설정해야 함

**Q3: 터미널에서 "command not found" 오류가 나요 (로컬 실행 시)**
- Python 또는 Node.js를 설치했는지 확인하세요.
- Python: 설치 후 `python --version` 입력해서 버전 확인
- Node.js: 설치 후 `node --version` 입력해서 버전 확인

**Q4: "cd backend" 후 다시 원래 폴더로 돌아가야 하나요? (로컬 실행 시)**
- 아니요! Backend 터미널은 그대로 두고, **새로운 터미널 창을 열어서** Frontend를 실행하세요.
- VS Code를 사용한다면: 하단 "터미널" 탭 옆 `+` 버튼으로 새 터미널 생성

**Q5: 포트가 이미 사용 중이라는 오류가 나요?**

Docker 사용 시:
```bash
docker-compose down -v
docker-compose up
```

로컬 실행 시:
- Backend 포트 8000을 다르게 지정: `python -m uvicorn main:app --reload --port 9000`
- Frontend 포트 5173은 자동으로 변경됨

**Q6: 앱을 실행했는데 아무것도 안 나타나요**
- Backend가 실행되고 있는지 확인하세요 (Docker인 경우 터미널 확인, 로컬인 경우 다른 터미널 확인)
- 브라우저 개발자 도구 열기: F12 키 → Console 탭 → 빨간 에러 메시지 확인
- 포트를 잘못 입력했는지 확인 (Docker: 3000, 로컬: 5173)

**Q7: "No such file or directory" 오류가 나요**
- 현재 폴더가 Name_Tag 폴더가 맞는지 확인하세요.
- `ls` (Mac/Linux) 또는 `dir` (Windows)를 입력해서 파일 목록 확인
- 현재 폴더에 frontend, backend 폴더가 보여야 합니다.

## 📡 API 엔드포인트

### 헬스 체크
```
GET /health
응답: { "status": "ok" }
```

### 브랜드 생성
```
POST /api/v1/brand/generate
Content-Type: application/json

요청:
{
  "business_type": "string",    # 필수 (3글자 이상)
  "vibes": ["string"],          # 필수 (1~4개)
  "target": "string",           # 필수 (3글자 이상)
  "keywords": "string"          # 선택
}

응답:
{
  "brands": [
    {
      "name": "string",
      "meaning": "string",
      "story": "string",
      "slogan": "string"
    },
    ...
  ],
  "typography": {
    "korean": "string",
    "english": "string",
    "reason": "string"
  },
  "character": {
    "name": "string",
    "concept": "string",
    "personality": "string",
    "visual": "string"
  }
}
```

## 📚 문서

- [마이그레이션 가이드](./MIGRATION.md) - Streamlit → React 마이그레이션 내역
- [배포 가이드](./DEPLOYMENT.md) - Vercel + Railway 배포 방법
- [Backend README](./backend/README.md) - FastAPI 사용법
- [Frontend README](./frontend/README.md) - React 개발 가이드

## 🔄 데이터 흐름

```
사용자 입력 (React Component)
  ↓
useGenerate hook (TanStack Query)
  ↓
axios POST /api/v1/brand/generate
  ↓
FastAPI Router
  ↓
brand_generator.py
  ↓
Google Gemini API (gemini-1.5-pro)
  ↓
JSON 응답
  ↓
utils/parser.py (JSON 파싱)
  ↓
Zustand store (상태 업데이트)
  ↓
UI 렌더링 (React Component)
```

## 🔧 개발 중 주의사항

### CORS 설정
- Backend: `main.py`의 ALLOWED_ORIGINS 수정
- Frontend: `vite.config.ts`의 proxy 설정 확인

### Gemini API
- 최신 모델: `gemini-1.5-pro` (권장)
- API 키: [Google AI Studio](https://aistudio.google.com/apikey)에서 발급

### 상태 관리
- Zustand store: `frontend/src/stores/generationStore.ts`
- 모든 상태 변경은 여기서 관리

## 📋 마이그레이션 완료 항목

✅ Streamlit → React 전환  
✅ 상태 관리 (st.session_state → Zustand)  
✅ API 분리 (FastAPI 백엔드)  
✅ TypeScript 타입 안전성  
✅ Tailwind CSS 스타일링  
✅ Docker 컨테이너화  
✅ 환경 변수 관리  

## 📝 다음 단계 (Phase 3+)

- [ ] Supabase Auth 통합 (회원가입/로그인)
- [ ] PostgreSQL 데이터베이스 (결과 저장)
- [ ] Stripe 결제 시스템
- [ ] PDF 다운로드 기능
- [ ] 이미지 생성 (Gemini 이미지)
- [ ] 프로덕션 배포 (Vercel + Railway)
- [ ] 분석 연동 (PostHog/GA)

## 👨‍💻 개발자 정보

**프로젝트:** NameTag - AI 브랜드 정체성 생성기  
**저장소:** Joseph-Ai-py/Name_Tag  
**라이선스:** MIT  

## 📞 지원

문제 발생 시:
1. [MIGRATION.md](./MIGRATION.md) 확인
2. [DEPLOYMENT.md](./DEPLOYMENT.md) 확인  
3. Backend/Frontend의 개별 README 확인

---

**🎉 마이그레이션 완료! React + FastAPI로 업그레이드되었습니다.**

```bash
.venv\Scripts\Activate.ps1
```

### 3) 패키지 설치

```bash
pip install -r requirements.txt
```

### 4) 환경 변수 설정

프로젝트 루트의 .env 파일에 아래 값을 설정합니다.

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

## 실행

```bash
streamlit run app.py
```

포트 지정 실행:

```bash
streamlit run app.py --server.port 8501
```

## 동작 흐름

1. 업종/서비스 입력
2. 브랜드 감성 태그 선택 (최대 4개)
3. 타겟 고객 입력
4. Gemini API로 브랜드 정체성 생성
5. 결과 확인 및 브랜드 선택

## 참고

- API 호출 로직은 services/brand_generator.py에만 위치합니다.
- 입력 상태와 단계는 Streamlit session_state로 관리됩니다.
- 같은 입력 재호출을 줄이기 위해 app.py에서 캐시를 사용합니다.
