# NAME TAG 작업 프롬프트 (Claude Code용)

> 상태 안내: 이 문서는 V1 오류 수정용 과거 작업 지시서입니다. V2 보고서 화면과 API가 현재 기본 흐름이므로, 새 작업은 `README.md`, `docs/REPORT_V2_INTEGRATION.md`, `backend/prompts/nametag_prompts_v2.py`를 기준으로 진행하세요.

아래 전체를 복사해서 저장소 루트(`Name_Tag/`)에서 실행한 Claude Code 세션에 붙여넣으세요.
Phase 단위로 나뉘어 있으니 **한 번에 한 Phase만** 진행시키는 것을 권장합니다.

---

## 역할과 목표

너는 NAME TAG 저장소(FastAPI + React, `backend/`, `frontend/`)를 수정하는 시니어 백엔드 엔지니어다.
설계 문서 "NAME TAG V1 필수 수정 + V2 브랜드·사업 전략 보고서 설계"를 기준으로 코드를 단계적으로 수정한다.
이번 요청의 범위는 **Phase 1 (V1 버그 수정 + 인터뷰 스키마 검증)** 이다. Phase 2 이후는 내가 따로 지시할 때까지 구현하지 않는다.

## 작업 규칙

1. 새 브랜치 `fix/p0-interview-schema`를 만들어 작업한다. `main`에 직접 커밋하지 않는다.

2. **`V2/` 폴더와 `streamlit/` 폴더는 수정하지 않는다.** 대상은 루트의 `backend/`, `frontend/`뿐이다.

3. 코드를 바꾸기 전에 관련 파일을 먼저 읽고, 아래 "확인된 현재 상태"가 실제와 다르면 멈추고 보고한다.

4. 요청받지 않은 리팩터링, 포맷 일괄 변경, 의존성 추가를 하지 않는다. 필요한 의존성이 있으면 이유와 함께 먼저 묻는다.

5. 기존 프론트엔드의 "직접 입력(자유 입력)" 기능과 현재 API 경로(`/api/section-*/...`)는 유지한다.

6. 작업 단위(버그 1개 = 커밋 1개)로 커밋한다. 커밋 메시지는 한국어 또는 영어 중 하나로 통일한다.

7. 푸시와 PR 생성은 하지 않는다. 마지막에 변경 요약과 `git diff --stat`만 보여준다.

## 확인된 현재 상태 (이미 조사 완료)

항목
위치
현재 문제

1.1 O 인터뷰가 입력 무시
`backend/routers/section_o.py` `/interview`, `backend/prompts/nametag_prompts.py` `get_O_interview_prompt()`
라우터가 `req: dict`를 받고 프롬프트 함수는 인자가 없음. 업종·감성·타겟·키워드가 프롬프트에 안 들어감

1.2 O 재생성 오참조
`backend/routers/section_o.py` `/re-generate`
`ORegenRequest`에는 `brand_data`만 있는데 `req.brand_info`를 참조 (실행 시 AttributeError)

1.3 질문 수·선택지 불일치
`backend/schemas/schema_interview.py`, `prompts`의 `get_B_interview_prompt`, `get_C_interview_prompt`, `get_DE_interview_prompt` 및 A/O 인터뷰 프롬프트
스키마에 개수 검증이 없음. B/C 예시는 `required_question_count: 1`, DE 예시는 3개

1.4 B1/B2 필드 충돌
`backend/prompts/nametag_prompts.py` `get_B1_persona_prompt`, `get_B2_journey_prompt`, `backend/routers/section_b.py` `/generate`
두 응답 모두 최상위 `strategic_reasoning`을 반환하고 `merged.update()`로 병합되어 B1 값이 B2로 덮임

추가 관찰: `re-generate` 프롬프트 문자열이 O/A/B/C/DE 라우터에 거의 동일하게 복붙되어 있고, `{req.brand_info}` 객체를 f-string에 그대로 넣는다.

## 구현 지시

### Task 1. 인터뷰 스키마 강화 (`backend/schemas/schema_interview.py`)

Pydantic v2 기준으로 다음을 만족하게 수정한다.

- `InterviewQuestion.options`: 정확히 4개 (`min_length=4, max_length=4`)

- `InterviewResponseSchema.required_question_count`: 5~10

- `InterviewResponseSchema.questions`: 5~10개

- `model_validator(mode="after")`로 검증: `required_question_count == len(questions)`, `question_id` 중복 금지

- 기존 필드명(`question_id`, `question_text`, `options`, `required_question_count`, `reasoning`, `questions`)은 바꾸지 않는다. 프론트가 이미 사용 중이다.

- 먼저 `pydantic` 버전을 확인하고, v1이면 멈추고 보고한다.

### Task 2. O 인터뷰에 `brand_data` 전달 (버그 1.1)

- `/interview` 요청 모델을 `OInterviewRequest`(이미 정의되어 있음)로 바꾼다. `req: dict` 제거.

- `get_O_interview_prompt(brand_data: dict)`로 시그니처를 바꾸고, 프롬프트에 업종(`business_type`), 분위기(`vibes`), 타겟(`target`), 키워드(`keywords`)를 명시적으로 주입한다. 파일에 이미 있는 `_brand_context()` 헬퍼를 재사용할 수 있으면 재사용한다.

- 입력이 비어 있는 항목은 임의로 추정하지 말고 "인터뷰에서 확인할 것"으로 취급하라는 지시를 프롬프트에 넣는다.

- **프론트엔드 호출부를 먼저 확인한다.** 프론트가 현재 `/section-o/interview`에 어떤 body를 보내는지 읽고, `{ brand_data: {...} }` 형태와 맞는지 검증한다. 맞지 않으면 프론트 쪽 요청 body를 최소 수정한다.

### Task 3. O 재생성 수정 (버그 1.2)

- `req.brand_info`를 `req.brand_data`로 바꾼다.

- 재생성 프롬프트에 `brand_data`, `context`, `target`이 모두 들어가게 한다.

- 프론트 함수 매개변수명이 `brandInfo`로 되어 있으면 `brandData`로 통일한다. 단, 서버로 보내는 JSON 키 이름이 실제 `brand_data`와 일치하는지 먼저 확인한다.

- 같은 AttributeError 위험이 A/B/C/DE `re-generate`에 있는지 확인하고, **있으면 보고만 한다** (해당 라우터의 요청 모델에는 `brand_info`가 정의되어 있어 현재는 문제가 없을 것으로 보인다).

### Task 4. 모든 단계 프롬프트의 질문 규칙 통일 (버그 1.3)

- O/A/B/C/DE 인터뷰 프롬프트 5개 모두에 다음 규칙을 동일한 문구로 넣는다: 질문 5~10개, 질문당 선택지 정확히 4개, 질문 ID 중복 금지, `required_question_count`는 `questions` 길이와 같아야 한다.

- 프롬프트 안 JSON 예시를 **질문 5개 이상, 각 4개 선택지**를 보여주는 유효한 예시로 바꾼다. B/C의 `required_question_count: 1`, DE의 `3`을 반드시 제거한다. 예시 질문은 해당 단계의 목적에 맞게 작성한다.

- 가능하면 규칙 문구를 상수(예: `INTERVIEW_RULES`)로 한 번만 정의해서 5개 프롬프트가 공유하게 한다.

- A/B/C/DE 인터뷰 라우터가 모두 `InterviewResponseSchema`를 통해 검증되는지 확인한다. 아닌 곳이 있으면 적용한다.

- 스키마 검증 실패 시 동작을 확인한다. `request_gemini_with_schema`(`backend/services/gemini_service.py`)가 검증 실패 시 재시도하는지 읽어보고, 재시도가 없으면 **최대 2회 재시도**를 추가하는 방안을 제안만 한다 (구현은 내가 승인하면 한다).

### Task 5. B1/B2 필드 충돌 해결 (버그 1.4)

- B1의 `strategic_reasoning` → `target_strategy_reasoning`

- B2의 `strategic_reasoning` → `journey_strategy_reasoning`

- 프롬프트 JSON 예시와 설명을 같이 바꾼다.

- B 응답용 Pydantic 스키마(`backend/schemas/schema_b.py`)를 새로 만들어 B1/B2 결과를 검증한다. 스키마 필드는 현재 프롬프트의 JSON 키(`core_target_group`, `primary_persona`, `secondary_personas`, `emotional_triggers`, `customer_journey_map`)를 그대로 따른다. **구조를 바꾸거나 4인 페르소나 설계를 앞당겨 적용하지 않는다.**

- `section_b.py`의 병합 로직이 키 충돌 시 예외를 내도록 하거나, 최소한 충돌 키를 감지해서 로그를 남기게 한다.

- **프론트엔드와 PDF 빌더가 `strategic_reasoning`을 읽는지** `frontend/src`, `backend/pdf/nametag_pdf_builder.py`, `backend/routers/pdf.py`에서 grep으로 확인하고, 읽고 있다면 새 필드명에 맞게 수정한다.

### Task 6. 테스트 추가

- `backend/tests/`가 없으면 만들고 pytest로 다음을 검증한다. (Gemini 호출은 mock하거나 스키마 단위 테스트로 한정한다. 실제 API 키가 없어도 통과해야 한다.)

1. 유효한 인터뷰 응답(5개, 선택지 4개) → 통과

2. 질문 4개 / 11개 → 실패

3. 선택지 3개 / 5개 → 실패

4. `required_question_count`와 `questions` 길이 불일치 → 실패

5. `question_id` 중복 → 실패

6. `get_O_interview_prompt(brand_data)` 결과에 업종·감성·타겟·키워드 문자열이 포함됨

7. B1/B2 병합 후 `target_strategy_reasoning`과 `journey_strategy_reasoning`이 둘 다 보존됨

8. O 재생성 프롬프트에 `brand_data`와 `context`가 포함되고 `brand_info` 참조가 없음

- `pytest`가 `requirements.txt`에 없으면 추가하지 말고 알려준다.

## 완료 기준 (Definition of Done)

- [ ] `python -m pytest backend/tests`가 통과

- [ ] `grep -rn "req.brand_info" backend/routers/section_o.py` 결과가 없음

- [ ] `grep -rn "required_question_count\": 1" backend/prompts` 결과가 없음

- [ ] 5개 인터뷰 프롬프트가 동일한 규칙 상수를 사용

- [ ] 프론트 빌드(`cd frontend && npm run build`)가 에러 없이 끝남 (프론트를 수정한 경우)

- [ ] 변경하지 않은 영역(`V2/`, `streamlit/`)에 diff가 없음

## 보고 형식

작업이 끝나면 다음만 짧게 보고한다.

1. 버그 1.1~1.4별로 무엇을 어떻게 고쳤는지 1~2줄

2. 수정한 파일 목록 (`git diff --stat`)

3. 테스트 실행 결과

4. 내가 결정해야 할 항목 (예: 재시도 추가 여부, 프론트 영향 범위)

5. 발견했지만 이번 범위에서 손대지 않은 문제

---

## 이후 Phase (지금은 구현하지 말 것)

- **Phase 2:** `backend/schemas/report_v2/`에 설계 문서 4장의 JSON 스키마를 Pydantic으로 정의하고, `backend/services/scoring.py`에 VPC X/Y 가중합 계산(X=0.35S+0.25F+0.25I+0.15A, Y=0.35P+0.30G+0.20D+0.15C), 포지셔닝 좌표 계산, 사분면 판정을 순수 함수와 단위 테스트로 구현. 기존 A/B/C/DE 출력을 새 구조로 변환하는 어댑터 추가.

- **Phase 3:** 4명 페르소나, 페르소나별 VPC 점수, 포지셔닝 축·경쟁사 평가, SWOT/TOWS, BMC 생성 프롬프트와 라우터.

- **Phase 4:** 시장 조사(검색 grounding), TAM/SAM/SOM, 경쟁사 출처 관리.

- **Phase 5:** 24페이지 PDF 렌더러(A4/A3, 가로/세로 혼합).
