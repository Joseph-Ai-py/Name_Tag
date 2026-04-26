# NameTag Package A

Version: v0.0.1

네임텍(NameTag) 패키지 A는 초기 스타트업 및 1인 기업을 위한 AI 브랜드 정체성 설계 Streamlit MVP입니다.

## 주요 기능

- 브랜드 네이밍 3안 제안
- 브랜드 의미, 스토리텔링, 슬로건 생성
- 한글/영문 서체 추천
- 브랜드 캐릭터 컨셉 제안
- 단계형 입력 UI (업종 -> 감성 -> 타겟 -> 생성 -> 결과)

## 기술 스택

- Python 3.11+
- Streamlit
- Google Gemini API (google-genai)
- python-dotenv

## 프로젝트 구조

```text
Name_Tag/
├── app.py
├── requirements.txt
├── .env
├── components/
│   ├── step_input.py
│   ├── step_vibe.py
│   ├── step_target.py
│   └── result_view.py
├── services/
│   └── brand_generator.py
├── utils/
│   └── parser.py
└── pages/
    └── result.py
```

## 시작하기

### 1) 가상환경 생성

```bash
python -m venv .venv
```

### 2) 가상환경 활성화 (Windows PowerShell)

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
GEMINI_MODEL=gemini-1.5-pro
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
