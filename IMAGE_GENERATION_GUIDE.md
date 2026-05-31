# 네임텍 이미지 생성 기능 가이드

## 개요

네임텍 서비스에 **고급 이미지 생성 기능**이 추가되었습니다. 이 기능은 `Prompt/네임텍 로고 캐릭터 생성 프롬프트.md`의 상세한 프롬프트 템플릿을 활용하여 전문적인 로고와 캐릭터를 생성합니다.

---

## 새로운 API 엔드포인트

### 1. 고급 로고 생성: `/brand/logo-advanced`

**설명**: Name Tag 프롬프트 시스템을 사용한 전문 로고 생성

**Method**: `POST`

**Request Body**:
```json
{
  "brand_name": "Brewly",
  "brand_topic": "수제 커피 구독 서비스",
  "core_value": "신뢰와 정밀함",
  "vibes": ["모던 & 신뢰"],
  "brand_color": "#2D6A4F",
  "symbol_type": "기하학적",
  "logo_type": "심볼+텍스트 조합",
  "background": "흰색"
}
```

**Request Fields**:
- `brand_name` (string, required): 브랜드명
- `brand_topic` (string, required): 사업 주제 또는 업종
- `core_value` (string, required): 브랜드 핵심 가치
- `vibes` (array, required): 브랜드 감성 (1-4개)
- `brand_color` (string, optional): 선호 색상 (빈값이면 감성에 따라 자동 매핑)
  - 예: `"#2D6A4F"`, `"딥그린 계열"`
- `symbol_type` (string, optional, default: "기하학적"): 심볼 스타일
  - 옵션: `"기하학적"`, `"유기적"`, `"미니멀"`, `"레터마크"`, `"아이콘형"`
- `logo_type` (string, optional, default: "심볼+텍스트 조합"): 로고 구성 방식
  - 옵션: `"심볼+텍스트 조합"`, `"심볼만"`, `"텍스트만"`, `"배지형"`
- `background` (string, optional, default: "흰색"): 배경 색상
  - 옵션: `"흰색"`, `"검정"`, `"브랜드 색상"`, `"투명"`

**Response**:
```json
{
  "image": "base64_encoded_image_string"
}
```

**자동 매핑 규칙** (vibes에 따른 자동 설정):
```
"모던 & 신뢰"      → 차콜(#333333), 기하학 산세리프
"따뜻 & 친근"      → 테라코타(#C8553D), 부드러운 산세리프
"미니멀 & 프리미엄" → 블랙(#1A1A1A) + 골드(#C9A84C)
"자연 & 지속가능"   → 딥그린(#2D6A4F), 유기적 산세리프
"에너지 & 역동"     → 바이브런트 블루(#0077B6), 굵은 산세리프
"부드러움 & 케어"   → 소프트 핑크(#F4A5A5), 라운드 산세리프
"혁신 & 기술"       → 딥퍼플(#6B4EFF), 모던 기하학
"클래식 & 전통"     → 네이비(#003153), 클래식 세리프
```

---

### 2. 고급 캐릭터 생성: `/brand/character-advanced`

**설명**: Name Tag 프롬프트 시스템을 사용한 전문 캐릭터/마스코트 생성

**Method**: `POST`

**Request Body**:
```json
{
  "brand_name": "Brewly",
  "brand_topic": "수제 커피 구독 서비스",
  "core_value": "신뢰와 정밀함",
  "character_name": "브루",
  "character_concept": "커피 원두의 의인화",
  "character_personality": "친근함, 따뜻함, 신뢰할 수 있음",
  "vibes": ["따뜻 & 친근"],
  "character_style": "플랫 일러스트",
  "character_age_feel": "나이 초월"
}
```

**Request Fields**:
- `brand_name` (string, required): 브랜드명
- `brand_topic` (string, required): 사업 주제 또는 업종
- `core_value` (string, required): 브랜드 핵심 가치
- `character_name` (string, required): 캐릭터 이름
- `character_concept` (string, required): 캐릭터 컨셉
  - 예: `"커피 원두의 의인화"`, `"작은 로봇"`, `"바람을 타는 씨앗"`
- `character_personality` (string, required): 성격 특징 (쉼표로 구분, 3개 권장)
  - 예: `"친근함, 똑똑함, 엉뚱함"`
- `vibes` (array, required): 브랜드 감성 (1-4개)
- `character_style` (string, optional, default: "플랫 일러스트"): 일러스트 스타일
  - 옵션: `"플랫 일러스트"`, `"손그림 느낌"`, `"3D 렌더"`, `"2.5D"`, `"픽셀아트"`
- `character_age_feel` (string, optional, default: "나이 초월"): 나이대 느낌
  - 옵션: `"어린이"`, `"청소년"`, `"청년"`, `"중장년"`, `"나이 초월"`

**Response**:
```json
{
  "image": "base64_encoded_image_string"
}
```

---

## 사용 예시

### Python 예시

```python
import requests
import json
import base64
from PIL import Image
from io import BytesIO

BASE_URL = "http://localhost:8000"

# 1. 고급 로고 생성
logo_request = {
    "brand_name": "Brewly",
    "brand_topic": "수제 커피 구독 서비스",
    "core_value": "신뢰와 정밀함",
    "vibes": ["모던 & 신뢰"],
    "symbol_type": "기하학적",
    "logo_type": "심볼+텍스트 조합"
}

response = requests.post(f"{BASE_URL}/brand/logo-advanced", json=logo_request)
data = response.json()

# Base64 이미지 디코딩
image_data = base64.b64decode(data["image"])
image = Image.open(BytesIO(image_data))
image.save("generated_logo.png")

# 2. 고급 캐릭터 생성
character_request = {
    "brand_name": "Brewly",
    "brand_topic": "수제 커피 구독 서비스",
    "core_value": "신뢰와 정밀함",
    "character_name": "브루",
    "character_concept": "커피 원두의 의인화",
    "character_personality": "친근함, 따뜻함, 신뢰할 수 있음",
    "vibes": ["따뜻 & 친근"],
    "character_style": "플랫 일러스트"
}

response = requests.post(f"{BASE_URL}/brand/character-advanced", json=character_request)
data = response.json()

# 이미지 저장
image_data = base64.b64decode(data["image"])
image = Image.open(BytesIO(image_data))
image.save("generated_character.png")
```

### cURL 예시

```bash
# 로고 생성
curl -X POST "http://localhost:8000/brand/logo-advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name": "Brewly",
    "brand_topic": "수제 커피 구독 서비스",
    "core_value": "신뢰와 정밀함",
    "vibes": ["모던 & 신뢰"],
    "symbol_type": "기하학적",
    "logo_type": "심볼+텍스트 조합"
  }' > logo_response.json

# 캐릭터 생성
curl -X POST "http://localhost:8000/brand/character-advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name": "Brewly",
    "brand_topic": "수제 커피 구독 서비스",
    "core_value": "신뢰와 정밀함",
    "character_name": "브루",
    "character_concept": "커피 원두의 의인화",
    "character_personality": "친근함, 따뜻함, 신뢰할 수 있음",
    "vibes": ["따뜻 & 친근"],
    "character_style": "플랫 일러스트"
  }' > character_response.json
```

---

## 프롬프트 템플릿 참조

모든 이미지 생성은 다음 프롬프트 템플릿을 기반으로 합니다:

**파일 위치**: `Prompt/네임텍 로고 캐릭터 생성 프롬프트.md`

### 템플릿의 주요 섹션

1. **로고 생성 프롬프트** (마스터 템플릿)
   - 브랜드 맥락 정보 통합
   - 심볼 디자인 사양
   - 타이포그래피 규칙
   - 색상 팔레트
   - 품질 요구사항

2. **캐릭터 생성 프롬프트** (마스터 템플릿)
   - 캐릭터 정체성 정의
   - 시각 스타일 규칙
   - 감정 표현 가이드
   - 디자인 제약 사항

3. **무드 자동 매핑**
   - 8가지 브랜드 무드별 색상/서체/스타일 매핑
   - 자동 추천 로직

---

## 구현 세부사항

### 새로운 파일들

1. **`utils/prompt_loader.py`**
   - 프롬프트 파일 로드 함수
   - 템플릿 추출 함수
   - 변수 매핑 함수
   - 무드 매핑 테이블 파싱

2. **업데이트된 파일**
   - `backend/services/brand_generator.py`
     - `generate_logo_image_with_context()` 추가
     - `generate_character_image_with_context()` 추가
   - `backend/routers/brand.py`
     - `/brand/logo-advanced` 엔드포인트 추가
     - `/brand/character-advanced` 엔드포인트 추가
     - 새로운 Request/Response 모델 추가

### 기술 스택

- **Gemini API**: 2.0 Flash 모델 사용 (이미지 생성)
- **Framework**: FastAPI
- **Language**: Python 3.8+

---

## 주의사항

1. **API Key**: `GEMINI_API_KEY` 환경변수가 반드시 설정되어야 합니다.
2. **모델**: 이미지 생성은 `gemini-2.0-flash-001` 모델을 사용합니다.
3. **응답 시간**: 이미지 생성에 30-60초가 소요될 수 있습니다.
4. **인코딩**: 응답은 Base64 인코딩된 바이너리 이미지입니다.

---

## 로그/에러 처리

### 일반적인 에러

| 상태 코드 | 메시지 | 원인 |
|---|---|---|
| 422 | JSON 파싱 실패 | 변수 대체 실패 또는 프롬프트 템플릿 오류 |
| 500 | GEMINI_API_KEY가 설정되지 않았습니다 | 환경변수 미설정 |
| 500 | 이미지 생성에 실패했습니다 | Gemini API 오류 |

---

## 향후 개선 사항

- [ ] 이미지 품질 평가 시스템
- [ ] 여러 이미지 생성 옵션 반환
- [ ] 캐시 시스템 구현
- [ ] 사용자 맞춤 프롬프트 수정 기능
- [ ] 벡터 포맷(SVG) 생성 옵션
