from __future__ import annotations

from urllib.parse import quote

from pdf_builder import assemble_html


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

