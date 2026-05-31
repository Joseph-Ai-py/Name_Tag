# NameTag - 통합 배포 가이드

## 🐳 Docker Compose로 로컬에서 실행

### 전제 조건
- Docker
- Docker Compose

### 1. 환경 변수 설정
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 2. 컨테이너 실행
```bash
docker-compose up --build
```

### 3. 접속
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health

---

## ☁️ Vercel (Frontend) + Railway (Backend) 배포

### Backend 배포 (Railway)

1. **Railway 계정 생성**
   - https://railway.app 에서 가입

2. **GitHub 연동**
   - Repository 연결

3. **환경 변수 설정**
   - `GEMINI_API_KEY` 추가

4. **자동 배포**
   - main 브랜치 push 시 자동 배포

### Frontend 배포 (Vercel)

1. **Vercel 계정 생성**
   - https://vercel.com 에서 가입

2. **GitHub 연동**
   - Repository 연결

3. **빌드 설정**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **환경 변수 설정**
   - `VITE_API_URL`: Railway에서 생성된 API URL

5. **자동 배포**
   - main 브랜치 push 시 자동 배포

---

## 📦 수동 배포

### 1. Backend (FastAPI) - 모든 클라우드 제공자

```bash
cd backend
pip install -r requirements.txt

# 환경 변수 설정
export GEMINI_API_KEY=your_key_here
export PORT=8000

# 실행
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend (React) - Vercel / Netlify

```bash
cd frontend
npm install
npm run build

# Vercel
vercel deploy --prod

# 또는 Netlify
netlify deploy --prod --dir=dist
```

---

## 🔍 배포 후 테스트

### Backend 확인
```bash
curl http://your-backend-url/health
```

응답:
```json
{"status": "ok"}
```

### 전체 플로우 테스트
1. Frontend URL 접속
2. "패키지 A 시작하기" 클릭
3. 입력 양식 작성
4. "브랜드 생성" 클릭
5. 결과 확인

---

## 환경 변수

### Backend (.env)
```
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-1.5-pro
PORT=8000
ENV=production
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend-url
```

---

## 문제 해결

### CORS 오류
- Backend에서 Frontend URL을 ALLOWED_ORIGINS에 추가

### API 연결 안 됨
- VITE_API_URL이 올바른지 확인
- Backend가 실행 중인지 확인
- 방화벽/네트워크 설정 확인

### Gemini API 오류
- GEMINI_API_KEY가 올바른지 확인
- API 할당량 확인
