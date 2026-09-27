# Name Tag v2

Conversation-first 실험 공간입니다. 기존 `streamlit/app.py` MVP와 분리되어 있습니다.

## 실행

```bash
cd streamlit/v2
../../.venv/bin/python -m streamlit run app.py --server.port 8504
```

v2는 기존 Streamlit의 Gemini client와 Brand Integrity checker를 재사용하지만, 세션 state와 대화 UI는 v2 전용입니다.

현재 vertical slice:

```text
ConversationMessage
-> Adaptive conversation turn
-> raw_results[conversation]
-> structured_context
-> BrandDocument
-> PDF view model / Integrity snapshot
```
