# 네임텍 커스텀 이미지 생성 가이드

## 개요

사용자가 이전 단계에서 입력한 **브랜드 정보**를 기반으로, **선택적으로** 로고와 캐릭터 생성 변수를 직접 커스터마이징할 수 있습니다.

- **입력하지 않은 변수**: AI가 자동으로 추론
- **입력한 변수**: 사용자 선택 사항 우선

---

## 워크플로우

### 1단계: 기본 정보 입력 (Step 1-3)
- 업종/서비스 입력 → `[BRAND_TOPIC]`
- 브랜드 감성 선택 → `[TARGET_MOOD]`
- 타겟 고객 설명 → 맥락 정보

### 2단계: 이미지 생성 변수 입력 (Step 5 - 새 기능)
```
로고 생성 변수:
├─ 브랜드명 (선택) ← 입력 안하면 자동 추론
├─ 업종/주제 (선택) ← Step 1 정보 활용
├─ 핵심 가치 (선택) ← 자동 추론
└─ 심볼 스타일 (선택) ← 기본값: 기하학적

캐릭터 생성 변수:
├─ 캐릭터 컨셉 (선택) ← 자동 생성
├─ 성격 특징 (선택) ← 자동 추론
├─ 스타일 (선택) ← 기본값: 플랫 일러스트
└─ 나이대 느낌 (선택) ← 기본값: 나이 초월
```

### 3단계: 이미지 생성
- 입력된 정보로 로고/캐릭터 생성
- 자동 추론 후 생성
- Base64 인코딩된 이미지 반환

---

## API 엔드포인트

### 1. 변수 추론: `POST /api/v1/brand/infer-variables`

**목적**: 기존 브랜드 정보로부터 누락된 변수들을 AI가 추론

**Request Body** (모두 선택사항):
```json
{
  "brand_name": "",
  "brand_topic": "수제 커피 구독 서비스",
  "core_value": "",
  "business_type": "",
  "vibes": ["모던 & 신뢰"],
  "target": "직장인, 20-40대",
  "keywords": ""
}
```

**Response**:
```json
{
  "inferred_variables": {
    "brand_name": "Brewly",
    "brand_topic": "수제 커피 구독 서비스",
    "core_value": "신뢰와 정밀함",
    "symbol_type": "기하학적",
    "character_concept": "커피 원두의 의인화",
    "character_personality": "친근함, 따뜻함, 신뢰할 수 있음",
    "character_style": "플랫 일러스트",
    "character_age_feel": "나이 초월",
    "recommended_mood": "MOOD-01"
  },
  "reasoning": "커피 서비스라는 주제에 맞게..."
}
```

---

### 2. 커스텀 로고 생성: `POST /api/v1/brand/logo-custom`

**목적**: 사용자 입력 + 자동 추론 변수로 로고 생성

**Request Body** (모두 선택사항):
```json
{
  "brand_name": "",
  "brand_topic": "수제 커피 구독 서비스",
  "core_value": "",
  "vibes": ["모던 & 신뢰"],
  "brand_color": "",
  "symbol_type": "기하학적",
  "logo_type": "",
  "background": "",
  "business_type": "",
  "target": "직장인, 20-40대",
  "keywords": ""
}
```

**Response**:
```json
{
  "image": "base64_encoded_image_string"
}
```

**프로세스**:
1. 빈 필드 → AI가 추론 API 호출
2. 추론된 값 + 사용자 입력 값 합병 (사용자 값 우선)
3. 로고 생성 API 호출
4. Base64 이미지 반환

---

### 3. 커스텀 캐릭터 생성: `POST /api/v1/brand/character-custom`

**목적**: 사용자 입력 + 자동 추론 변수로 캐릭터 생성

**Request Body** (모두 선택사항):
```json
{
  "brand_name": "",
  "brand_topic": "수제 커피 구독 서비스",
  "core_value": "",
  "character_name": "",
  "character_concept": "커피 원두의 의인화",
  "character_personality": "",
  "vibes": ["따뜻 & 친근"],
  "character_style": "플랫 일러스트",
  "character_age_feel": "",
  "business_type": "",
  "target": "",
  "keywords": ""
}
```

**Response**:
```json
{
  "image": "base64_encoded_character_image"
}
```

---

## 프론트엔드 통합

### Step 5: 이미지 생성 커스터마이제이션

현재 Generate.tsx에 새로운 스텝 추가:

```tsx
{currentStep === 5 && <ImageGenerationCustomizer brandData={generationStore} />}
```

### ImageGenerationCustomizer 컴포넌트

사용자가:
1. 기존 정보 확인
2. 선택적으로 변수 커스터마이징
3. "로고 생성", "캐릭터 생성" 버튼 클릭

---

## 사용 시나리오

### 시나리오 1: 최소 입력 (AI에 맡기기)

**사용자 입력**:
```
Step 1-3: 브랜드 기본 정보 입력
Step 5: 모든 필드 비워두기 → AI가 자동 추론 & 생성
```

**플로우**:
```
사용자 데이터 → infer-variables API
→ 추론된 변수들 → logo-custom API
→ 로고 생성 → 캐릭터도 동일 프로세스
```

### 시나리오 2: 부분 커스터마이징

**사용자 입력**:
```
Step 5:
- 로고: "심볼 스타일 = 유기적" (직접 입력)
- 캐릭터: 컨셉만 입력, 나머지는 비워두기
```

**플로우**:
```
사용자 입력 + 비운 필드 → infer-variables API
→ 추론 + 사용자 입력 병합
→ 로고 생성, 캐릭터 생성
```

### 시나리오 3: 완전 커스터마이징

**사용자 입력**:
```
Step 5: 모든 필드 작성
- 심볼 타입: 미니멀
- 색상: #333333
- 캐릭터 성격: 친근함, 신뢰, 지혜로움
- 스타일: 2.5D
```

**플로우**:
```
사용자 입력 (추론 스킵) → 
logo-advanced API / character-advanced API
→ 이미지 생성
```

---

## 백엔드 변수 추론 로직

### `infer_missing_variables()` 함수

**입력**:
- Step 1-3에서 수집한 정보
- 사용자가 입력한 부분 변수

**처리**:
```python
1. 제공된 정보 정리
2. Gemini API 호출 (프롬프트 엔지니어링)
3. 브랜드 컨텍스트 기반 추론
   - 업종 → 적절한 심볼 스타일
   - 감성 → 캐릭터 스타일
   - 타겟 → 캐릭터 나이대
4. JSON 파싱 & 반환
```

**추론 기준**:
```
업종별 심볼 스타일 추천:
- IT/SaaS → 기하학적
- 푸드 → 유기적
- 럭셔리 → 미니멀
- 동물/대사관 → 동물 마스코트

감성별 캐릭터 스타일:
- 현대/신뢰 → 플랫, 깔끔
- 따뜻/친근 → 플랫, 유기적
- 혁신/기술 → 2.5D, 미래 느낌
- 클래식 → 손그림, 전통적
```

---

## 선택적 입력의 장점

1. **간편성**: 빈칸으로 두면 자동 처리
2. **유연성**: 원하는 부분만 커스터마이징
3. **일관성**: 이전 단계 정보 자동 활용
4. **시간 절감**: 반복 작업 최소화
5. **AI 활용**: 전문가 수준의 추천

---

## 에러 처리

### 빈 정보로 추론 불가

**상황**: 모든 필드가 비어있음

**처리**:
```python
→ 기본값 사용 (fallback)
  - brand_name: "Brand"
  - symbol_type: "기하학적"
  - character_style: "플랫 일러스트"
  - character_age_feel: "나이 초월"
```

### API 오류 (422/500)

**처리**:
```
사용자에게 알림:
"변수 추론에 실패했습니다. 일부 정보를 수동으로 입력해주세요."
→ 기본값으로 폴백하거나
→ 사용자가 모든 필드 입력하도록 유도
```

---

## 테스트 케이스

### Test 1: 최소 입력
```bash
curl -X POST http://localhost:8000/api/v1/brand/logo-custom \
  -H "Content-Type: application/json" \
  -d '{"vibes": ["모던 & 신뢰"]}'
```

### Test 2: 부분 입력
```bash
curl -X POST http://localhost:8000/api/v1/brand/character-custom \
  -H "Content-Type: application/json" \
  -d '{
    "brand_topic": "커피",
    "character_concept": "커피 원두",
    "vibes": ["따뜻 & 친근"]
  }'
```

### Test 3: 변수 추론
```bash
curl -X POST http://localhost:8000/api/v1/brand/infer-variables \
  -H "Content-Type: application/json" \
  -d '{
    "business_type": "수제 커피 구독",
    "target": "직장인, 20-40대",
    "vibes": ["모던 & 신뢰"]
  }'
```

---

## 향후 확장

- [ ] 사용자 커스터마이징 역사 저장
- [ ] 여러 변형 이미지 동시 생성
- [ ] 사용자 커스텀 템플릿 저장
- [ ] 생성 결과 평가 피드백
- [ ] 배치 생성 (여러 변형 한 번에)
