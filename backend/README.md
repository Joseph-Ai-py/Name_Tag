# NameTag Backend

REST API 서버입니다.

## 개발 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```
GEMINI_API_KEY=your_key_here
```

### 3. 서버 실행
```bash
python -m uvicorn main:app --reload --port 8000
```

## API 엔드포인트

### Health Check
```
GET /health
```

### 브랜드 생성
```
POST /api/v1/brand/generate
Content-Type: application/json

{
  "business_type": "string",
  "vibes": ["string"],
  "target": "string",
  "keywords": "string"
}
```

응답:
```json
{
  "brands": [...],
  "typography": {...},
  "character": {...}
}
```

## 구조

- `main.py` - FastAPI 진입점
- `routers/` - API 라우터
- `services/` - 비즈니스 로직
- `utils/` - 유틸리티
