# Name_Tag 브랜드 가이드 생성기

Gemini 기반 인터뷰 결과를 바탕으로 브랜드 전략, 비주얼 아이덴티티, 로고·캐릭터 가이드를 만들고 하나의 PDF 브랜드 가이드로 내보내는 Streamlit 앱입니다.

## 주요 흐름

앱은 다음 순서로 진행됩니다.

1. **O**: 브랜드명, 의미, 슬로건, 핵심 컬러 확정
2. **A**: 철학, 미션·비전, 브랜드 스토리, 포지셔닝, 브랜드 약속 생성
3. **B**: 핵심 고객, 페르소나, 고객 여정, SWOT, 사업 모델 가설 생성
4. **C**: 컬러, 서체, 비주얼 무드와 디자인 원칙 생성
5. **DE**: 로고와 캐릭터 가이드 생성
6. **Preview**: 무결성 검수 후 PDF 생성·미리보기·다운로드

## 요구 사항

- Python 3.11 이상
- Gemini API 키
- PDF 렌더링용 Cairo, Pango, GDK Pixbuf 계열 시스템 라이브러리

Dev Container를 사용하면 `.devcontainer/devcontainer.json`의 설정에 따라 `packages.txt`와 `requirements.txt`가 자동 설치됩니다.

## 설치

저장소 루트에서 실행합니다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

Debian/Ubuntu 환경에서 PDF 시스템 패키지를 직접 설치해야 한다면 다음을 실행합니다.

```bash
sudo apt update
sudo xargs apt install -y < packages.txt
```

## 환경 변수

`.env.example`을 복사해 `.env`를 만들고 값을 입력합니다.

```bash
cp .env.example .env
```

필수 값:

- `GEMINI_API_KEY`: 텍스트 생성 API 키
- `GEMINI_IMAGE_API_KEY`: 로고·캐릭터 이미지 생성 API 키

선택 값:

- `GEMINI_MODEL`: 텍스트 생성 모델
- `GEMINI_IMAGE_MODEL`: 이미지 생성 모델

`.env`와 `.streamlit/secrets.toml`에는 비밀값을 넣으므로 Git에 커밋하지 않습니다.

## 실행

```bash
.venv/bin/streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

브라우저에서 `http://localhost:8501`을 엽니다. Dev Container에서는 포트 8501이 자동 포워딩됩니다.

## 테스트

브랜드 DNA와 PDF HTML 출력 계약을 모두 검사합니다.

```bash
python3 -m unittest discover -s . -p 'test_*.py'
```

검사 항목:

- 중첩된 SWOT와 사업 모델이 PDF HTML에 표시되는지
- 타 브랜드 샘플 문구가 최종 HTML에 포함되지 않는지
- Brand DNA가 Python 딕셔너리 원문으로 노출되지 않는지
- Decision Trace가 구조화된 내부 검토 부록으로 표시되는지
- 최종 HTML의 무결성 검사에서 오염 문구를 차단하는지

## PDF 출력 정책

- PDF 본문에는 사람이 읽을 수 있는 브랜드 전략과 Brand DNA 요약을 표시합니다.
- Decision Trace는 `Appendix · Internal Review` 부록에서 필드별로 표시합니다.
- Section B의 SWOT와 사업 모델은 `data_b.customer_swot` 및 `data_b.business_model` 구조를 사용합니다.
- PDF 생성 직전에 최종 HTML을 `Brand Integrity Check`로 검사합니다.
- 확정 브랜드명이 없거나 다른 브랜드 문구가 발견되면 PDF 생성이 중단됩니다.

## 프로젝트 구조

| 파일 | 역할 |
| --- | --- |
| `app.py` | Streamlit 진입점과 멀티 스텝 UI |
| `state.py` | 세션 상태 관리 |
| `models.py` | Pydantic 데이터 모델과 응답 스키마 |
| `prompts.py` | Gemini 프롬프트 |
| `logic_o.py`, `logic_a.py`, `logic_b.py`, `logic_c.py`, `logic_de.py` | 단계별 생성 로직 |
| `brand_dna.py` | canonical Brand DNA와 무결성 검사 |
| `pdf_builder.py` | PDF용 HTML/CSS 조립 |
| `pdf_service.py` | WeasyPrint PDF 생성과 검수 연결 |
| `image_service.py` | 생성 이미지 저장 |
| `assets/` | 로고·캐릭터 이미지 저장 위치 |

## 생성 파일과 보안

- API 키와 Streamlit secrets는 저장소에 커밋하지 않습니다.
- 새로 생성되는 로고·캐릭터 이미지는 Git 추적 대상에서 제외됩니다.
- 기존에 저장소에 포함된 샘플 asset은 유지됩니다.
- 생성된 PDF, 로그, Python 캐시는 Git에서 제외됩니다.
