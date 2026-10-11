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

## 초보자용 빠른 시작

처음 실행하는 경우에는 아래 순서대로 따라 하면 됩니다.

1. Docker Desktop 또는 Docker Engine + Docker Compose를 설치합니다.
2. 저장소 루트에서 백엔드 환경 파일을 만듭니다.

```bash
cp backend/.env.example backend/.env
```

3. [backend/.env](backend/.env) 파일을 열고 `GEMINI_API_KEY` 값을 넣습니다.
4. 저장소 루트에서 아래 명령어를 실행합니다.

```bash
docker compose up --build
```

5. 브라우저에서 [http://localhost:3000](http://localhost:3000) 을 엽니다.

백엔드가 정상인지 먼저 보고 싶으면 [http://localhost:8000/health](http://localhost:8000/health) 를 확인합니다.

만약 Docker 대신 로컬에서 실행하고 싶다면, 아래의 `가상환경 + 라이브러리 설치` 섹션을 따라가면 됩니다.

## 권장 실행 환경

- Docker Desktop 또는 Docker Engine + Docker Compose
- Gemini API 키 필요
- Python 3.10 이상
- Node.js 18 이상

로컬 venv 없이도 실행할 수 있도록 도커 기준으로 정리했습니다.

## 가상환경과 라이브러리 설치

Docker를 쓰지 않고 로컬에서 실행하려면 먼저 백엔드용 Python 가상환경을 만들고, 필요한 라이브러리를 설치해야 합니다.

### 1. Python 가상환경 만들기

저장소 루트에서 아래 명령어를 실행합니다.

```bash
cd backend
python -m venv venv
```

`python` 명령이 없으면 `python3` 로 바꿔서 실행합니다.

### 2. 가상환경 활성화하기

운영체제에 따라 활성화 명령이 다릅니다.

```bash
# macOS / Linux
source venv/bin/activate
```

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

가상환경이 켜지면 터미널 앞쪽에 `venv` 같은 표시가 붙습니다.

### 3. Python 라이브러리 설치하기

가상환경이 활성화된 상태에서 백엔드 의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

백엔드 라이브러리는 [backend/requirements.txt](backend/requirements.txt)에 정리되어 있습니다.

### 4. 백엔드 실행하기

가상환경이 활성화된 상태에서 아래처럼 실행합니다.

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

중요한 점은 `main.py`가 [backend/](backend) 안에 있어서, 반드시 `backend` 폴더로 이동한 뒤 실행해야 한다는 것입니다.

만약 저장소 루트에서 바로 실행하고 싶다면 아래처럼 `--app-dir backend` 를 추가할 수 있습니다.

```bash
python -m uvicorn main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

### 5. 프론트엔드 라이브러리 설치하기

프론트엔드는 별도로 Node 패키지를 설치해야 합니다.

```bash
cd ../frontend
npm install
```

프론트엔드 라이브러리는 [frontend/package.json](frontend/package.json)을 기준으로 설치됩니다.

## 프로젝트 구조

- [backend/](backend) - FastAPI 백엔드
- [frontend/](frontend) - Vite + React 프론트엔드
- [notebook_backend/](notebook_backend) - 문서와 PDF 조립 기준이 되는 참고 로직
- [docker-compose.yml](docker-compose.yml) - 백엔드와 프론트를 함께 띄우는 구성

## 환경 변수

백엔드는 [backend/.env.example](backend/.env.example)를 참고해서 [backend/.env](backend/.env) 파일을 만듭니다. 초보자는 아래 한 줄로 복사한 뒤 값을 수정하면 됩니다.

```bash
cp backend/.env.example backend/.env
```

예시:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
PORT=8000
ENV=development
```

프론트엔드는 기본값으로 `http://localhost:8000`을 사용합니다. 별도 설정이 필요하면 `VITE_API_URL`을 지정하세요.

## Docker로 실행

가장 쉬운 실행 방법입니다. 백엔드와 프론트엔드를 한 번에 띄웁니다.

```bash
docker compose up --build
```

실행하면 두 개의 주소를 주로 사용합니다.

- 백엔드: [http://localhost:8000](http://localhost:8000)
- 프론트엔드: [http://localhost:3000](http://localhost:3000)

실행 후 확인 주소:

- [http://localhost:8000/health](http://localhost:8000/health)
- [http://localhost:3000](http://localhost:3000)

참고:

- 프론트는 빌드 시점에 `VITE_API_URL=http://localhost:8000/api` 를 사용합니다.
- 백엔드는 `http://localhost:3000` 과 `http://localhost:5173` 둘 다 CORS 허용합니다.

도커를 쓰면 로컬에 Python 가상환경이나 Node 패키지를 따로 설치하지 않아도 됩니다.

## 프론트엔드만 실행

프론트엔드 화면만 먼저 확인하려면 아래 명령어를 사용합니다. 이 방법은 UI만 빠르게 볼 때 유용합니다.

```bash
cd frontend
npm install
npm run dev
```

기본 접속 주소는 `http://localhost:5173` 입니다.

## 백엔드와 함께 개발 실행

백엔드 API까지 함께 붙여서 개발할 때는 터미널을 두 개 열어 각각 실행합니다. 첫 번째 터미널은 백엔드, 두 번째 터미널은 프론트엔드입니다.

먼저 백엔드 환경을 준비합니다.

```bash
cd backend
cp .env.example .env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`backend/.env` 파일을 열어서 `GEMINI_API_KEY` 를 넣습니다.

그다음 백엔드를 실행합니다. 이 명령은 반드시 `backend` 폴더 안에서 실행해야 합니다.

```bash
# 터미널 1
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

프론트엔드는 새 터미널에서 실행합니다.

```bash
# 터미널 2
cd frontend
npm install
npm run dev
```

이 경우 프론트엔드는 `http://localhost:5173`, 백엔드는 `http://localhost:8000` 에서 확인할 수 있습니다.

### 초보자가 자주 막히는 경우

- `python` 명령이 없으면 `python3` 를 사용합니다.
- `npm` 명령이 없으면 Node.js 설치가 필요합니다.
- `GEMINI_API_KEY` 가 비어 있으면 일부 생성 기능이 동작하지 않을 수 있습니다.
- 포트 충돌이 나면 `3000` 또는 `8000` 을 이미 쓰고 있는 프로그램이 있는지 확인합니다.

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