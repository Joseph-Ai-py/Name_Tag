from __future__ import annotations

from urllib.parse import quote

from pdf_builder import assemble_html

from pdf_builder import (
    build_css,
    build_a1_philosophy,
    build_a2_core_identity,
    build_a3_story,
    build_a4_verbal_toolkit,
    build_a5_positioning,
    build_a6_promise
)


def generate_pdf_bytes(
	brand_info: dict,
	data_a: dict,
	data_b: dict,
	data_c: dict,
	data_de: dict,
) -> bytes:
	try:
		from weasyprint import HTML
	except (ImportError, OSError) as exc:
		raise RuntimeError(
			"Unable to import WeasyPrint. Install system dependencies such as libcairo2, "
			"libgobject-2.0-0, and libpango."
		) from exc

	html_content = assemble_html(brand_info, data_a, data_b, data_c, data_de)
	return HTML(string=html_content).write_pdf()


def build_download_filename(brand_name: str) -> str:
	return f"nametag_{brand_name}_guideline.pdf"


def build_content_disposition(brand_name: str) -> str:
	encoded_filename = quote(build_download_filename(brand_name))
	return f"attachment; filename*=utf-8''{encoded_filename}"

def generate_a_only_html(brand_info: dict, data_a: dict) -> str:
    """PDF 변환 없이 HTML 문자열만 렌더링하여 반환합니다 (빠른 미리보기용)"""
    
    if data_a and 'data_a' in data_a:
        data_a = data_a['data_a']

    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color = "#3A3A3A"
    sl_color = "#F8F9FA"

    # 기본 CSS 로드
    base_css = build_css(seed_color, sd_color, sl_color)
    
    preview_css = base_css + """
    body {
        max-width: 210mm;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 40px;
        overflow-x: hidden;
    }
    """

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;800&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">
  <style>{preview_css}</style>
</head>
<body>
"""
    if data_a:
        html += build_a1_philosophy(data_a)
        html += build_a2_core_identity(data_a)
        html += build_a3_story(data_a)
        html += build_a4_verbal_toolkit(data_a)
        html += build_a5_positioning(data_a)
        html += build_a6_promise(data_a)

    html += "</body>\n</html>"

    return html

