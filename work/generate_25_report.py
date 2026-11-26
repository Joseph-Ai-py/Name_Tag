import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.prompts.nametag_prompts_v2 import REPORT_PAGE_ORDER, validate_page_result

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/api"
STATE_PATH = ROOT / "work" / "nametag_25_report.json"
DECISIONS = {"17": True, "21": True}
ANSWERS = {key: [] for key in ("brand", "business", "customer", "market", "visual", "logo_character")}
CONTEXT = {
    "brand": {
        "brand_name": "살뜰마을",
        "business_type": "지역 생활용품 구독 서비스",
        "target": "20~40대 1인 가구",
        "vibes": [],
        "keywords": [],
    },
    "input_limitations": "확인된 사용자 입력은 브랜드명, 서비스 유형, 타겟뿐이다. 가격·운영 지역·팀·성과·고객 조사·시장 데이터·실제 인터뷰 답변은 확인되지 않았다. 근거가 필요한 항목은 사실처럼 채우지 말고 insufficient_data 또는 to_validate로 표시한다.",
    "interview_answers": ANSWERS,
    "pages": {},
}


def post(path: str, body: dict, timeout: int = 180):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = Request(f"{BASE}{path}", data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=timeout) as response:
        return response.status, response.read()


def save_state():
    STATE_PATH.write_text(json.dumps({"brand": CONTEXT["brand"], "pages": CONTEXT["pages"], "interview_answers": ANSWERS}, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if STATE_PATH.exists():
        saved = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if saved.get("brand") == CONTEXT["brand"]:
            CONTEXT["pages"] = saved.get("pages", {})

    # Ensure the page contracts still enumerate the full 00–24 set.
    with urlopen(f"{BASE}/report-v2/meta", timeout=30) as response:
        meta_bytes = response.read()
    meta = json.loads(meta_bytes)
    if meta["page_order"] != list(REPORT_PAGE_ORDER) or len(meta["page_order"]) != 25:
        raise RuntimeError("Server page order does not contain the expected 25 IDs")

    completed = set(CONTEXT["pages"])
    for page_id in REPORT_PAGE_ORDER:
        if page_id in completed:
            errors = validate_page_result(page_id, CONTEXT["pages"][page_id], CONTEXT["pages"])
            if errors:
                del CONTEXT["pages"][page_id]
                completed.remove(page_id)
                print(f"REGENERATE {page_id}: saved result failed validation: {errors}", flush=True)

    while len(CONTEXT["pages"]) < 25:
        plan_body = {
            "context": CONTEXT,
            "conditional_decisions": DECISIONS,
            "skipped_page_ids": [],
        }
        _, raw = post("/report-v2/plan", plan_body, timeout=30)
        plan = json.loads(raw)
        ready = [page_id for page_id in plan["ready_page_ids"] if page_id not in CONTEXT["pages"]]
        if not ready:
            remaining = [page_id for page_id in REPORT_PAGE_ORDER if page_id not in CONTEXT["pages"]]
            raise RuntimeError(f"No ready page; remaining IDs: {remaining}; plan={plan}")

        # Generate one page per request so each prompt receives the latest validated canonical state.
        page_id = ready[0]
        request_body = {"context": CONTEXT, "conditional_decisions": DECISIONS, "regenerate": False}
        last_error = None
        for attempt in range(1, 4):
            try:
                status, raw = post(f"/report-v2/pages/{page_id}", request_body, timeout=660)
                payload = json.loads(raw)
                page = payload["page"]
                errors = validate_page_result(page_id, page, CONTEXT["pages"])
                if errors:
                    raise RuntimeError(f"local contract validation failed: {errors}")
                CONTEXT["pages"][page_id] = page
                save_state()
                print(f"OK {len(CONTEXT['pages'])}/25 {page_id} {page['title']} status={page['status']} confidence={page['confidence']} bytes={len(raw)}", flush=True)
                last_error = None
                break
            except HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = f"HTTP {exc.code}: {detail}"
            except (URLError, TimeoutError, RuntimeError, KeyError, ValueError, json.JSONDecodeError) as exc:
                last_error = repr(exc)
            if attempt < 3:
                print(f"RETRY {page_id} attempt={attempt + 1} after {last_error}", flush=True)
                time.sleep(attempt * 2)
        if last_error:
            raise RuntimeError(f"Page {page_id} failed after three attempts: {last_error}")

    validation_errors = {
        page_id: validate_page_result(page_id, CONTEXT["pages"][page_id], CONTEXT["pages"])
        for page_id in REPORT_PAGE_ORDER
    }
    validation_errors = {page_id: errors for page_id, errors in validation_errors.items() if errors}
    if validation_errors:
        raise RuntimeError(f"Final validation errors: {validation_errors}")
    print(f"COMPLETE ids={len(CONTEXT['pages'])} status_counts={ {status: sum(p['status'] == status for p in CONTEXT['pages'].values()) for status in ('complete', 'insufficient_data', 'to_validate')} }", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FATAL {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
