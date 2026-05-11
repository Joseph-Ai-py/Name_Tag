# NameTag - 마이그레이션 완료

모든 코드가 React + FastAPI로 전환되었습니다.

## 프로젝트 구조

```
Name_Tag/
├── backend/              # FastAPI 백엔드
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── utils/
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # React 프론트엔드
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── app.py               # 기존 Streamlit (레거시)
└── README.md
```

## 빠른 시작

### 1. 환경 변수 설정
```bash
cp backend/.env.example backend/.env
# backend/.env에서 GEMINI_API_KEY 설정
```

### 2. 백엔드 실행
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### 3. 프론트엔드 실행 (다른 터미널)
```bash
cd frontend
npm install
npm run dev
```

브라우저: http://localhost:5173

## 기술 스택

| 계층 | 기술 |
|------|------|
| 프론트엔드 | React 18 + TypeScript + Tailwind CSS + Vite |
| 상태 관리 | Zustand + TanStack Query |
| 라우팅 | React Router v6 |
| 백엔드 | FastAPI + Uvicorn |
| Python 버전 | 3.11+ |
| API | REST (JSON) |

## 데이터 흐름

```
React Component
  ↓
useGenerate hook (TanStack Query)
  ↓
axios POST /api/v1/brand/generate
  ↓
FastAPI router
  ↓
brand_generator.py
  ↓
Gemini API
  ↓
JSON 응답
  ↓
Zustand store → UI 렌더링
```

## 주요 파일

### Backend
- `backend/main.py` - FastAPI 앱 진입점
- `backend/routers/brand.py` - 브랜드 생성 엔드포인트
- `backend/services/brand_generator.py` - Gemini API 호출 (기존 로직 재사용)

### Frontend
- `frontend/src/App.tsx` - React 진입점
- `frontend/src/pages/Generate.tsx` - 메인 마법사 페이지
- `frontend/src/stores/generationStore.ts` - Zustand 상태 관리
- `frontend/src/hooks/useGenerate.ts` - API 호출 훅

## API 엔드포인트

### Health Check
```
GET /health
```

### 브랜드 생성
```
POST /api/v1/brand/generate

Request:
{
  "business_type": "string",
  "vibes": ["string"],
  "target": "string",
  "keywords": "string"
}

Response:
{
  "brands": [...],
  "typography": {...},
  "character": {...}
}
```

## Streamlit (레거시)

기존 Streamlit 앱은 `app.py`에 그대로 보관되어 있습니다.
필요시 실행:
```bash
streamlit run app.py
```

## 다음 단계

- [ ] Supabase Auth 통합
- [ ] PostgreSQL 데이터베이스 (결과 저장)
- [ ] Stripe 결제 시스템
- [ ] PDF 다운로드
- [ ] 이미지 생성
- [ ] 배포 (Vercel + Railway)
