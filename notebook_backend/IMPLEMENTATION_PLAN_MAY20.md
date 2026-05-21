# 📅 NameTag 5월 20일 완성 계획

**목표**: 모든 주요 기능 구현 및 테스트 (5월 20일 실행)

---

## 📊 현재 상태 분석

### ✅ 완성된 기능
1. **브랜드명** (.txt) - 3개 옵션
2. **슬로건** (.txt) - 3개 옵션
3. **브랜드 스토리텔링** (.txt) - 3개 옵션
4. **서체 추천** (.txt) - 한글/영문 폰트
5. **캐릭터 정보** (.txt) - 이름, 성격, 묘사
6. **로고 이미지** (.png) - Gemini 생성
7. **캐릭터 이미지** (.png) - Gemini 생성

### ⚠️ 부분/미완료 기능

| 기능 | 상태 | 문제점 |
|------|------|--------|
| **로고/심볼** | ⚠️ 이미지만 | SVG 변환 필요 |
| **캐릭터** | ⚠️ 1개만 | 10개 이상 페르소나 생성 필요 |
| **컬러 톤앤 매너** | ⚠️ 자동맵핑만 | 상세 설명 및 팔레트 필요 |
| **마케팅 방식** | ❌ 미구현 | 테마별 효과적인 제안 필요 |
| **시장검증 방식** | ❌ 미구현 | 시장 진출 전략 필요 |

---

## 🎯 구현 계획 (단계별)

### **Phase 1: 프롬프트 개선 (1-2일)**
*백엔드 AI 프롬프트 업그레이드*

#### 1-1. 컬러 톤앤 매너 상세화
- **위치**: `backend/services/brand_generator.py`
- **변경사항**:
  - 컬러 팔레트 생성 추가 (Primary, Secondary, Accent 색상)
  - 각 색상의 심리학적 의미 설명
  - 텍스트 포맷: `color_tone_manner.txt`
  - 출력 예시:
    ```
    [Primary Color]
    색상: #FF6B6B (따뜻한 빨강)
    의미: 열정, 에너지, 신뢰성
    사용처: 주요 버튼, 강조 부분
    
    [Secondary Color]
    색상: #4ECDC4 (시원한 민트)
    의미: 신선함, 혁신
    사용처: 배경, 보조 요소
    ```

#### 1-2. 마케팅 방식 구현
- **위치**: `backend/services/brand_generator.py`
- **기능**: 브랜드 특성별 효과적인 마케팅 전략 제안
- **출력**: `marketing_strategy.txt`
- **포함 사항**:
  - 3가지 마케팅 채널 추천 (SNS, 이메일, 인플루언서 등)
  - 각 채널별 콘텐츠 주제 5가지
  - 타겟 오디언스별 메시지 톤
  - 시즌별/이벤트별 캠페인 아이디어

#### 1-3. 시장검증 방식 구현
- **위치**: `backend/services/brand_generator.py`
- **기능**: 브랜드 성공 여부를 미리 검증하는 방법 제시
- **출력**: `market_validation.txt`
- **포함 사항**:
  - 타겟 고객 인터뷰 질문 5가지
  - A/B 테스트 전략 (로고, 슬로건 변형 테스트)
  - 경쟁사 분석 체크리스트
  - 시장 반응 지표 (KPI) 정의

#### 1-4. 페르소나 10개 생성 구현
- **위치**: `backend/services/brand_generator.py`
- **기능**: 단일 캐릭터 대신 10개 이상의 다양한 페르소나 생성
- **출력**: `persona_profiles.txt`
- **포함 사항** (각 페르소나별):
  - 이름, 나이, 직업
  - 성격 3가지
  - 구매 동기
  - 선호 채널
  - 일일 루틴 스니펫

### **Phase 2: SVG 변환 시스템 (1-2일)**
*이미지를 SVG 벡터 포맷으로 변환*

#### 2-1. 로고 SVG 생성 엔드포인트 추가
- **위치**: `backend/routers/brand.py`
- **새 엔드포인트**: `POST /api/v1/brand/logo-svg`
- **로직**:
  1. Gemini Image API로 로고 이미지 생성
  2. PNG/JPG 바이너리 → Base64
  3. **변환 방식 선택**:
     - **Option A (권장)**: Potrace 또는 ImageMagick으로 자동 추적
     - **Option B**: Gemini에 직접 SVG 코드 요청 (더 간단하고 품질 높음)
  4. SVG 파일 저장 경로: `logo/` 폴더
  5. 파일명 포맷: `logo_{브랜드명}_{생성일시}.svg`

#### 2-2. 심볼 SVG 생성 엔드포인트 추가
- **위치**: `backend/routers/brand.py`
- **새 엔드포인트**: `POST /api/v1/brand/symbol-svg`
- **로직**: 로고의 심볼 부분만 SVG로 생성
- **저장**: `logo/symbols/` 폴더

#### 2-3. 캐릭터 SVG 생성 엔드포인트 추가
- **위치**: `backend/routers/brand.py`
- **새 엔드포인트**: `POST /api/v1/brand/character-svg`
- **로직**: 캐릭터 일러스트를 SVG로 생성
- **저장**: `logo/characters/` 폴더

#### 2-4. SVG 저장 유틸 함수 작성
- **위치**: `backend/utils/svg_handler.py` (신규)
- **기능**:
  - SVG 파일 저장 처리
  - 파일명 관리 (브랜드명, 타입, 생성일시)
  - SVG 메타데이터 추가 (브랜드명, 생성일, 버전)

### **Phase 3: 프론트엔드 결과 화면 업데이트 (1-2일)**
*새로운 출력들을 UI에 표시*

#### 3-1. ResultView 확장
- **위치**: `frontend/src/components/Result/ResultView.tsx`
- **새 탭/섹션 추가**:
  - 탭1: 브랜드 정보 (현재 구현됨)
  - 탭2: 로고/심볼 이미지 & SVG 다운로드
  - 탭3: 캐릭터 페르소나 (10개 카드 형식)
  - 탭4: 컬러 톤앤 매너 (팔레트 시각화)
  - 탭5: 마케팅 전략
  - 탭6: 시장검증 체크리스트

#### 3-2. 페르소나 카드 컴포넌트 생성
- **위치**: `frontend/src/components/Persona/PersonaCard.tsx` (신규)
- **디자인**:
  - 프로필 사진 (캐릭터 이미지 또는 기본 아바타)
  - 이름, 나이, 직업
  - 성격 태그
  - 구매 동기 한 줄 요약

#### 3-3. 컬러 팔레트 시각화 컴포넌트
- **위치**: `frontend/src/components/ColorPalette/PaletteViewer.tsx` (신규)
- **디자인**:
  - 컬러 사각형 표시 (hex + RGB)
  - 색상명 한글 표시
  - 심리학적 의미 설명

#### 3-4. SVG 다운로드 버튼 추가
- **위치**: `frontend/src/components/Result/ResultView.tsx`
- **기능**:
  - 로고 SVG 다운로드
  - 심볼 SVG 다운로드
  - 캐릭터 SVG 다운로드
  - 파일명: `{브랜드명}_{타입}_{생성일시}.svg`

### **Phase 4: 통합 엔드포인트 개선 (1일)**
*기존 엔드포인트에 새 기능 통합*

#### 4-1. `/api/v1/brand/generate` 응답 확장
- **추가 필드**:
  ```json
  {
    "brand_options": [...],
    "color_tone_manner": { ... },
    "marketing_strategies": { ... },
    "market_validation": { ... },
    "personas": [...]  // 10개
  }
  ```

#### 4-2. 타입 정의 업데이트
- **위치**: `frontend/src/types/index.ts`
- **새 타입**:
  - `ColorToneManner`
  - `MarketingStrategy`
  - `MarketValidation`
  - `Persona`

### **Phase 5: 테스트 및 검증 (1일)**
*모든 기능이 정상 작동하는지 확인*

#### 5-1. 백엔드 테스트
- **테스트 파일**: `Test/test_all_features.py` (신규)
- **테스트 항목**:
  - 컬러 톤앤 매너 생성
  - 마케팅 전략 생성
  - 시장검증 방식 생성
  - 10개 페르소나 생성
  - 로고 SVG 생성 및 저장
  - 심볼 SVG 생성 및 저장
  - 캐릭터 SVG 생성 및 저장

#### 5-2. 프론트엔드 테스트
- **수동 테스트**:
  - 모든 탭 렌더링 확인
  - SVG 파일 다운로드 정상 작동
  - 페르소나 카드 표시 확인
  - 컬러 팔레트 시각화 정상 작동

#### 5-3. 통합 테스트
- **시나리오**: 전체 흐름 한 번에 테스트
  1. 사용자 입력
  2. AI 응답 생성
  3. 모든 출력 파일 저장 확인
  4. 프론트엔드 표시 확인
  5. SVG 다운로드 테스트

### **Phase 6: 결과 파일 정리 (1일)**
*모든 출력을 .txt 파일로 저장*

#### 6-1. 저장 시스템 설정
- **저장 위치**: `results/{브랜드명}_{생성일시}/`
- **저장 파일**:
  ```
  results/
  ├── brand_name.txt (브랜드명)
  ├── slogan.txt (슬로건)
  ├── brand_story.txt (브랜드 스토리텔링)
  ├── typography.txt (서체)
  ├── color_tone_manner.txt (컬러 톤앤 매너)
  ├── marketing_strategy.txt (마케팅 방식)
  ├── market_validation.txt (시장검증)
  ├── persona_profiles.txt (10개 페르소나)
  ├── logo/
  │  ├── logo.svg
  │  └── logo.png
  ├── symbols/
  │  └── symbol.svg
  └── characters/
     ├── character.svg
     └── character_personas.svg (10개 묶음)
  ```

#### 6-2. 다운로드 패키지 생성
- **기능**: 모든 파일을 ZIP으로 압축 후 다운로드
- **엔드포인트**: `GET /api/v1/brand/download-all/{session_id}`

---

## 📁 핵심 수정 파일 목록

| 파일 | 역할 | 상태 |
|------|------|------|
| `backend/services/brand_generator.py` | 프롬프트 개선 & 새 기능 추가 | 📝 수정 |
| `backend/routers/brand.py` | SVG 엔드포인트 추가 | 📝 수정 |
| `backend/utils/svg_handler.py` | SVG 저장 유틸 | 📝 신규 |
| `frontend/src/components/Result/ResultView.tsx` | 새 탭/섹션 추가 | 📝 수정 |
| `frontend/src/components/Persona/PersonaCard.tsx` | 페르소나 카드 | 📝 신규 |
| `frontend/src/components/ColorPalette/PaletteViewer.tsx` | 컬러 팔레트 | 📝 신규 |
| `frontend/src/types/index.ts` | 타입 정의 확장 | 📝 수정 |
| `Test/test_all_features.py` | 통합 테스트 | 📝 신규 |

---

## ⏱️ 일정 (5월 20일 완성 기준)

| Phase | 예상 기간 | 마감일 |
|-------|---------|--------|
| Phase 1: 프롬프트 개선 | 1-2일 | 5월 16-17일 |
| Phase 2: SVG 변환 | 1-2일 | 5월 17-18일 |
| Phase 3: 프론트엔드 | 1-2일 | 5월 18-19일 |
| Phase 4: 통합 개선 | 1일 | 5월 19일 |
| Phase 5: 테스트 | 1일 | 5월 19-20일 |
| Phase 6: 파일 정리 | 1일 | 5월 20일 |

---

## ✅ 5월 20일 최종 결과물 체크리스트

- [ ] 브랜드명 (.txt) - 3개
- [ ] 슬로건 (.txt) - 3개
- [ ] 브랜드 스토리텔링 (.txt) - 3개
- [ ] 서체 추천 (.txt)
- [ ] **컬러 톤앤 매너 (.txt)** - 상세 팔레트 포함
- [ ] **마케팅 방식 (.txt)** - 테마별 전략
- [ ] **시장검증 방식 (.txt)** - 검증 체크리스트
- [ ] **페르소나 10개 이상 (.txt)**
- [ ] **로고 SVG** - 다운로드 가능
- [ ] **심볼 SVG** - 다운로드 가능
- [ ] **캐릭터 SVG** - 다운로드 가능
- [ ] 모든 파일 ZIP으로 패키징

---

## 🚀 추천 구현 순서

1. **프롬프트 개선 먼저** (Phase 1)
   - AI 출력을 충실하게 만들기
   - 텍스트 기반 기능들은 상대적으로 구현이 빠름

2. **SVG 변환** (Phase 2)
   - 이미지 형식 변환은 독립적으로 진행 가능
   - 병렬로 프론트엔드 작업과 진행 가능

3. **프론트엔드** (Phase 3)
   - 백엔드 API 안정화 후 진행
   - UI 컴포넌트는 재사용 가능하도록 설계

---

## ⚠️ 주의사항

1. **Gemini API 할당량**: 대량 생성 시 API 호출 제한 주의
2. **SVG 품질**: 이미지 → SVG 변환 품질 테스트 필수
3. **성능**: 10개 페르소나 생성 시 응답 시간 증가 → 캐싱 고려
4. **메모리**: SVG 파일 저장 시 디스크 용량 관리

---

**작성일**: 2026년 5월 20일  
**목표**: 5월 20일 완성
