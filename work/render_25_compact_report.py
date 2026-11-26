import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

import fitz
from weasyprint import HTML

from backend.pdf.report_v2_pdf import DEFAULT_PAGE_LAYOUTS, PAGE_TITLES, _render_inline_markdown
from backend.prompts.nametag_prompts_v2 import REPORT_PAGE_ORDER, validate_page_result

STATE_PATH = ROOT / "work" / "nametag_25_report.json"
QA_DIR = ROOT / "work" / "pdf_qa" / "compact_25"
QA_DIR.mkdir(parents=True, exist_ok=True)


def compact(value):
    if value is None or value == "":
        return "추가 정보 필요"
    if isinstance(value, dict):
        return " · ".join(f'<span class="label">{html.escape(str(key), quote=True)}:</span> {compact(child)}' for key, child in value.items())
    if isinstance(value, list):
        return " · ".join(compact(child) for child in value) if value else "추가 정보 필요"
    if isinstance(value, bool):
        return "예" if value else "아니요"
    return _render_inline_markdown(value)


def render_value(key, value, depth=0):
    label = html.escape(str(key), quote=True)
    if isinstance(value, dict) and depth == 0:
        rows = "".join(f'<div class="item"><span class="label">{html.escape(str(child_key), quote=True)}</span><span>{compact(child)}</span></div>' for child_key, child in value.items())
        return f'<section class="group"><h3>{label}</h3>{rows}</section>'
    if isinstance(value, list) and depth == 0:
        entries = []
        for index, child in enumerate(value, 1):
            if isinstance(child, dict):
                title_key = next((k for k in ("persona_id", "strategy_id", "competitor_id", "id", "name", "period", "stage", "metric", "factor_id") if child.get(k)), None)
                title = html.escape(str(child.get(title_key) if title_key else f"항목 {index}"), quote=True)
                entries.append(f'<article class="record"><h5>{title}</h5><div>{compact(child)}</div></article>')
            else:
                entries.append(f'<article class="record">{compact(child)}</article>')
        body = "".join(entries) if entries else "추가 정보 필요"
        return f'<section class="group"><h3>{label}</h3>{body}</section>'
    return f'<div class="item"><span class="label">{label}</span><span>{compact(value)}</span></div>'


def make_html(page_id, page, scale):
    paper, orientation, margin = DEFAULT_PAGE_LAYOUTS.get(page_id, ("A4", "portrait", 12))
    data = page.get("data", {})
    chars = len(json.dumps(data, ensure_ascii=False))
    if paper == "A3":
        base_size = 9.2 if chars < 3200 else 8.2 if chars < 5200 else 7.5
    elif orientation == "landscape":
        base_size = 8.8 if chars < 2400 else 7.7 if chars < 4200 else 7.1
    else:
        base_size = 9.4 if chars < 1700 else 8.4 if chars < 3000 else 7.6
    body_size = base_size * scale
    title_size = max(18, body_size * 2.25)
    css = """@page { size: __SIZE__; margin: __MARGIN__mm; }
* { box-sizing: border-box; }
body { margin:0; font-family:"Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif; color:#383630; background:#fffdf9; font-size:__BODY__pt; line-height:1.23; }
.page { width:100%; }
header { border-bottom:1px solid #e9e1d7; padding-bottom:3mm; margin-bottom:4mm; }
.eyebrow { color:#b78367; font-size:__SMALL__pt; letter-spacing:.6px; }
h1 { color:#403b35; font-size:__TITLE__pt; line-height:1.14; font-weight:500; margin:1.5mm 0 1mm; }
.subtitle { color:#817970; font-size:__SUB__pt; }
.meta { float:right; color:#817970; font-size:__TINY__pt; text-align:right; }
.group { margin:0 0 2mm; padding:0 0 1mm; border-bottom:.4pt solid #e9e1d7; }
h3,h4,h5 { color:#655d53; font-weight:600; line-height:1.16; margin:0 0 .7mm; }
h3 { font-size:__H3__pt; } h4 { font-size:__H4__pt; } h5 { font-size:__H5__pt; }
.item { margin:.3mm 0; } .label { color:#817970; font-size:__SMALL__pt; font-weight:600; margin-right:1mm; } .compact { display:inline; }
.record { border-left:1.2pt solid #d8c5b4; padding-left:1.5mm; margin:.8mm 0 1.1mm; }
strong.emphasis { color:#3c342e; font-weight:700; }
.validation { color:#817970; border-top:.4pt solid #e9e1d7; margin-top:2mm; padding-top:1mm; font-size:__TINY__pt; }
.footer { position:fixed; bottom:0; left:0; right:0; border-top:.4pt solid #e9e1d7; padding-top:1mm; color:#9b9389; font-size:__TINY__pt; }
.cover { min-height:245mm; display:flex; flex-direction:column; justify-content:center; }
.cover h1 { font-size:42pt; margin:10mm 0 4mm; }.cover-headline { font-size:18pt; color:#6c6258; }
.cover-promise { border-left:2pt solid #b78367; background:#f6f1e9; padding:4mm; margin:4mm 0; }
.cover-details { margin-top:20mm; }
"""
    replacements = {
        "__SIZE__": f"{paper} {orientation}", "__MARGIN__": str(0 if page_id == "00" else margin),
        "__BODY__": f"{body_size:.2f}", "__TITLE__": f"{title_size:.2f}",
        "__SMALL__": f"{max(6, body_size*.76):.2f}", "__SUB__": f"{max(8, body_size*.92):.2f}",
        "__TINY__": f"{max(5.8, body_size*.68):.2f}", "__H3__": f"{max(9, body_size*1.22):.2f}",
        "__H4__": f"{max(8, body_size*1.08):.2f}", "__H5__": f"{max(7.5, body_size*.98):.2f}",
    }
    for key, value in replacements.items():
        css = css.replace(key, value)
    status = html.escape(str(page.get("status", "to_validate")), quote=True)
    confidence = html.escape(str(page.get("confidence", "low")), quote=True)
    note = " · ".join(map(str, page.get("validation_notes", [])))
    if page_id == "00":
        brand = _render_inline_markdown(data.get("brand_name", "살뜰마을"))
        headline = _render_inline_markdown(data.get("key_sentence", "브랜드 전략 보고서"))
        content = f'<section class="cover"><div class="eyebrow">NAME TAG · BRAND & BUSINESS STRATEGY</div><h1>{brand}</h1><p class="cover-headline">{headline}</p><div class="cover-promise">{_render_inline_markdown(data.get("brand_promise", ""))}</div><div class="cover-details">{render_value("업종 / 산업", data.get("industry"))}{render_value("작성일", data.get("report_date"))}</div></section>'
    else:
        content = "".join(render_value(key, value) for key, value in data.items())
    title = html.escape(str(page.get("title") or PAGE_TITLES[page_id][0]), quote=True)
    subtitle = html.escape(PAGE_TITLES[page_id][1], quote=True)
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body><main class="page" style="page:report_{page_id}"><header><span class="eyebrow">NAME TAG · BRAND & BUSINESS REPORT · {page_id}</span><span class="meta">상태 · {status}<br>신뢰도 · {confidence}</span><h1>{title}</h1><div class="subtitle">{subtitle}</div></header>{content}{f"<div class=validation>{html.escape(note)}</div>" if note and page_id != "00" else ""}<footer class="footer">NAME TAG · BRAND & BUSINESS STRATEGY <span style="float:right">{page_id} / 25</span></footer></main></body></html>'


state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
pages = state["pages"]
assert set(pages) == set(REPORT_PAGE_ORDER) and len(pages) == 25
for page_id in REPORT_PAGE_ORDER:
    errors = validate_page_result(page_id, pages[page_id], pages)
    assert not errors, f"{page_id}: {errors}"

combined = fitz.open()
for number, page_id in enumerate(REPORT_PAGE_ORDER, 1):
    path = QA_DIR / f"page-{page_id}.pdf"
    scale = 1.0
    for attempt in range(7):
        HTML(string=make_html(page_id, pages[page_id], scale), base_url=str(ROOT)).write_pdf(str(path))
        candidate = fitz.open(path)
        count = len(candidate)
        candidate.close()
        if count == 1:
            break
        scale *= .82
    if count != 1:
        raise RuntimeError(f"Page {page_id} overflows after compact scaling: {count} pages at scale {scale:.3f}")
    candidate = fitz.open(path)
    print(f"PAGE {number}/25 id={page_id} one physical page scale={scale:.3f}", flush=True)
    combined.insert_pdf(candidate)
    candidate.close()

pdf_path = ROOT / "work" / "nametag_25_report.pdf"
combined.save(pdf_path, garbage=4, deflate=True)
combined.close()
final_doc = fitz.open(pdf_path)
assert len(final_doc) == 25, f"Expected 25 physical pages, got {len(final_doc)}"
for number, page in enumerate(final_doc, 1):
    text = page.get_text()
    assert len(text.strip()) > 40, f"Page {number} appears blank"
    page.get_pixmap(matrix=fitz.Matrix(.9, .9), alpha=False).save(str(ROOT / "work" / "pdf_qa" / f"final25-{number:02d}.png"))
    print(f"QA {number:02d}/25 {page.rect.width:.0f}x{page.rect.height:.0f} chars={len(text)}", flush=True)
final_doc.close()
print(f"PDF {pdf_path} bytes={pdf_path.stat().st_size}", flush=True)
