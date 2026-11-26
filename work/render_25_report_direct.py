import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

import fitz
from weasyprint import HTML

from backend.pdf.report_v2_pdf import build_report_v2_html
from backend.prompts.nametag_prompts_v2 import REPORT_PAGE_ORDER, apply_backend_calculations, validate_page_result


state = json.loads((ROOT / "work" / "nametag_25_report.json").read_text(encoding="utf-8"))
pages = state["pages"]
assert set(pages) == set(REPORT_PAGE_ORDER) and len(pages) == 25
for page_id in REPORT_PAGE_ORDER:
    pages[page_id] = apply_backend_calculations(page_id, pages[page_id])
    errors = validate_page_result(page_id, pages[page_id], pages)
    assert not errors, f"{page_id}: {errors}"

qa_dir = ROOT / "work" / "pdf_qa" / "25pages"
qa_dir.mkdir(parents=True, exist_ok=True)
combined = fitz.open()
for number, page_id in enumerate(REPORT_PAGE_ORDER, 1):
    html = build_report_v2_html({page_id: pages[page_id]})
    # Avoid WeasyPrint grid fragmentation loops on long content and keep one section per page.
    html = html.replace(
        "</style>",
        ".prism-panel { display:block; break-inside:auto; }.prism-grid { display:block; }"
        ".prism-card { display:inline-block; width:30%; vertical-align:top; break-inside:avoid; }"
        ".identity-lower { display:block; }.identity-lower > div { display:inline-block; width:48%; vertical-align:top; }"
        ".two-column { display:block; }.metric-grid .item-grid { display:block; }"
        ".data-group { break-inside:auto; }"
        "</style>",
    )
    chunk = qa_dir / f"page-{page_id}.pdf"
    started = time.time()
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(chunk))
    rendered = fitz.open(chunk)
    print(f"RENDERED {number}/25 id={page_id} physical={len(rendered)} seconds={time.time()-started:.1f} bytes={chunk.stat().st_size}", flush=True)
    combined.insert_pdf(rendered)
    rendered.close()
    chunk.unlink()

pdf_path = ROOT / "work" / "nametag_25_report.pdf"
combined.save(pdf_path, garbage=4, deflate=True)
combined.close()
result = fitz.open(pdf_path)
print(f"PDF_BYTES {pdf_path.stat().st_size} PHYSICAL_PAGES {len(result)}", flush=True)
for index, page in enumerate(result, 1):
    text = page.get_text()
    print(f"PAGE {index:02d} {page.rect.width:.0f}x{page.rect.height:.0f} chars={len(text)}", flush=True)
    page.get_pixmap(matrix=fitz.Matrix(0.7, 0.7), alpha=False).save(str(ROOT / "work" / "pdf_qa" / f"25page-{index:02d}.png"))
result.close()
