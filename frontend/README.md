# NameTag Frontend

## 개발 시작

### 1. 의존성 설치
```bash
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```

브라우저에서 `http://localhost:5173`을 열면 됩니다.

### 3. 프로덕션 빌드
```bash
npm run build
npm run preview
```

## 환경 변수

`.env.local` 파일을 생성하고 다음을 설정하세요:

```
VITE_API_URL=http://localhost:8000
```

## 구조

- `src/components/` - React 컴포넌트
  - `Wizard/` - Step별 입력 컴포넌트
  - `Result/` - 결과 표시 컴포넌트
  - `Layout/` - Header, Footer
- `src/hooks/` - Custom hooks
  - `useGenerate` - API 호출 훅
  - `useWizard` - 상태 관리 훅
- `src/stores/` - Zustand 상태 저장소
- `src/lib/` - API 클라이언트
- `src/pages/` - 페이지 컴포넌트
