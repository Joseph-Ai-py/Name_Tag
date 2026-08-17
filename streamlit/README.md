# Name_Tag 스트림릿 앱

## 개요
이 폴더는 Name_Tag 워크플로우를 스트림릿으로 독립 구현한 코드입니다.
기존 backend, frontend 모듈을 직접 import하지 않고 실행되도록 구성했습니다.

## 폴더 구성
- app.py: 스트림릿 실행 진입점, 멀티 스텝 화면
- state.py: 세션 상태 관리 유틸
- models.py: 공통 데이터 모델 및 스키마
- prompts.py: 프롬프트 생성 함수 모음
- gemini_client.py: Gemini 텍스트/이미지 호출 클라이언트
- logic_o.py: Section O 처리 로직
- logic_a.py: Section A 처리 로직
- logic_b.py: Section B 처리 로직
- logic_c.py: Section C 처리 로직
- logic_de.py: Section DE 처리 로직
- image_service.py: 로고/캐릭터 이미지 생성 및 저장 유틸
- pdf_builder.py: PDF용 HTML 조립기
- pdf_service.py: PDF 바이트 생성 서비스
- utils.py: 공통 유틸 함수
- requirements.txt: 이 폴더 실행에 필요한 파이썬 라이브러리 목록
- .env: 실행 환경 변수 파일

## 설치
아래 명령으로 의존성을 한 번에 설치합니다.

```bash
/workspaces/Name_Tag/.venv/bin/python -m pip install -r requirements.txt
```

## 환경 변수 설정
.env 파일에 아래 값을 설정하세요.

- GEMINI_API_KEY
- GEMINI_IMAGE_API_KEY
- GEMINI_MODEL (선택)
- GEMINI_IMAGE_MODEL (선택)

## 실행 방법
streamlit 폴더에서 아래 명령을 실행합니다.

```bash
/workspaces/Name_Tag/.venv/bin/python -m streamlit run app.py
```

## 참고 사항
- PDF 내보내기는 WeasyPrint 및 시스템 라이브러리(cairo, pango 계열)가 필요합니다.
- 생성된 이미지는 이 폴더 내부 assets 디렉터리에 저장됩니다.
- 현재 UI는 기능 중심으로 구성되어 있어 이후 스타일 개선이 가능합니다.
