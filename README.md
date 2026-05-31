# NameTag

NameTag는 업종, 감성, 타겟 고객을 입력하면 브랜드 후보, 스토리, 서체, 로고, 캐릭터, 가이드 문서까지 이어서 만들어주는 서비스입니다.

현재 구조는 다음 순서로 동작합니다.

1. 프론트엔드에서 업종, 감성, 타겟을 입력합니다.
2. 백엔드가 후보 브랜드 3개를 생성합니다.
3. 선택한 후보를 기준으로 철학, 스토리, 포지셔닝, 시각 언어를 확장합니다.
4. 로고와 캐릭터 이미지를 생성합니다.
5. HTML과 PDF 가이드를 저장합니다.

## 실제로 되는지 한 줄로 답하면

네. 지금 저장소 기준으로는 도커로 백엔드와 프론트를 함께 실행하면 처음 입력부터 결과 화면, 로고/캐릭터, 가이드 문서 생성까지 이어지는 흐름이 동작합니다.

## 권장 실행 환경

- Docker Desktop 또는 Docker Engine + Docker Compose
- Gemini API 키 필요

로컬 venv 없이도 실행할 수 있도록 도커 기준으로 정리했습니다.

## 프로젝트 구조

- [backend/](backend) - FastAPI 백엔드
- [frontend/](frontend) - Vite + React 프론트엔드
- [notebook_backend/](notebook_backend) - 문서와 PDF 조립 기준이 되는 참고 로직
- [docker-compose.yml](docker-compose.yml) - 백엔드와 프론트를 함께 띄우는 구성

## 환경 변수

백엔드는 [backend/.env.example](backend/.env.example)를 참고해서 [backend/.env](backend/.env) 파일을 만듭니다.

예시:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
PORT=8000
ENV=development
```

프론트엔드는 기본값으로 `http://localhost:8000`을 사용합니다. 별도 설정이 필요하면 `VITE_API_URL`을 지정하세요.

## Docker로 실행

아래 한 줄로 전체 스택을 띄울 수 있습니다.

```bash
docker compose up --build
```

기본 포트:

- 백엔드: `8000`
- 프론트엔드: `3000`

실행 후 확인 주소:

- `http://localhost:8000/health`
- `http://localhost:3000`

참고:

- 프론트는 빌드 시점에 `VITE_API_URL=http://localhost:8000/api` 를 사용합니다.
- 백엔드는 `http://localhost:3000` 과 `http://localhost:5173` 둘 다 CORS 허용합니다.

## 실행 순서 상세

### 1. 홈 화면

프론트에서 시작하면 섹션형 진행 화면이 보입니다.

### 2. 입력 단계

Section O에서 다음 값을 입력합니다.

- 업종 또는 서비스명
- 브랜드 감성 1개 이상, 최대 4개
- 타겟 고객 설명
- 필요하면 추가 키워드

### 3. 후보 생성

프론트가 백엔드의 [POST /api/section-o/interview](backend/routers/section_o.py) 와 [POST /api/section-o/candidates](backend/routers/section_o.py) 를 호출합니다.

### 4. 확장 단계

Section A, B, C, DE를 순서대로 진행하면 철학, 스토리, 타겟, 시각 언어, 로고, 캐릭터가 확장됩니다.

### 5. 가이드 생성

[POST /api/pdf/generate](backend/routers/pdf.py) 를 호출하면 PDF 파일이 내려갑니다.

## 백엔드가 만드는 결과물

- 브랜드 후보 4개
- 철학, 스토리, 포지셔닝 확장 정보
- 컬러, 타이포, 무드 시스템
- 로고 이미지
- 캐릭터 이미지
- HTML 가이드
- PDF 가이드

생성 결과는 주로 다음 위치에 저장됩니다.

- `output/` - HTML/PDF 가이드
- `assets/logos/` - 로고 이미지
- `assets/characters/` - 캐릭터 이미지

## 주요 API

- `GET /health`
- `POST /api/section-o/interview`
- `POST /api/section-o/candidates`
- `POST /api/section-a/interview`
- `POST /api/section-a/generate`
- `POST /api/section-b/interview`
- `POST /api/section-b/generate`
- `POST /api/section-c/interview`
- `POST /api/section-c/generate`
- `POST /api/section-de/interview`
- `POST /api/section-de/generate`
- `POST /api/pdf/generate`

## 확인 포인트

실행이 제대로 됐는지는 아래 순서로 보면 됩니다.

1. `http://localhost:8000/health`가 `ok`를 반환하는지 확인합니다.
2. 프론트에서 Section O에 업종, 감성, 타겟을 입력하고 인터뷰를 실행합니다.
3. 후보 4개를 믹스앤매치로 조합해 브랜드 정보를 확정합니다.
4. Section A, B, C, DE를 순서대로 생성합니다.
5. Preview에서 PDF 다운로드를 눌러 파일이 내려가는지 확인합니다.

## 문제 해결

- Gemini 키가 없으면 이미지나 텍스트 생성이 제한됩니다.
- 프론트가 백엔드를 못 찾으면 도커 컨테이너 재빌드 후 `http://localhost:8000/api` 주소가 빌드에 반영됐는지 확인하세요.

## 참고 문서

- [backend/NAMETAG_BACKEND_FLOW.md](backend/NAMETAG_BACKEND_FLOW.md)