from __future__ import annotations

import os
import tempfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.pdf.nametag_pdf_builder import assemble_html
from backend.pdf.report_v2_pdf import build_report_v2_compact_html, build_report_v2_html
from backend.prompts.nametag_prompts_v2 import apply_backend_calculations, validate_page_result
from backend.schemas.report_v2 import ReportV2PdfRequest

router = APIRouter()


class PdfRequest(BaseModel):
    brand_info: dict
    data_a: dict
    data_b: dict
    data_c: dict
    data_de: dict


@router.post("/generate")
async def generate_pdf(req: PdfRequest):
    try:
        try:
            from weasyprint import HTML
        except (ImportError, OSError) as exc:
            raise HTTPException(
                status_code=500,
                detail=(
                    "PDF 생성용 라이브러리를 불러올 수 없습니다. "
                    "WeasyPrint가 필요로 하는 시스템 패키지(libcairo2, libgobject-2.0-0, "
                    "libpango 등)가 설치되어 있는지 확인하세요."
                ),
            ) from exc

        print(
            f"[DEBUG] PDF 생성 시작 - brand_name: {req.brand_info.get('brand_name')}, "
            f"data_keys={{'a': list(req.data_a.keys()), 'b': list(req.data_b.keys()), 'c': list(req.data_c.keys()), 'de': list(req.data_de.keys())}}"
        )
        
        html_content = assemble_html(req.brand_info, req.data_a, req.data_b, req.data_c, req.data_de)
        print(f"[DEBUG] PDF HTML assembled - length={len(html_content)}")
        
        # PDF 생성
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        HTML(string=html_content).write_pdf(tmp.name)
        tmp.close()

        print(f"[DEBUG] PDF 생성 완료: {tmp.name}")

        def file_iterator(path: str, chunk_size: int = 4096):
            try:
                with open(path, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
            finally:
                try:
                    os.remove(path)
                except Exception:
                    pass

        brand_name = req.brand_info.get("brand_name", "brand")
        
        # 1. URL 인코딩을 위한 패키지 불러오기 (파일 최상단에 적어도 되지만 여기에 적어도 작동합니다)
        from urllib.parse import quote
        
        # 2. 파일명 전체를 URL 안전한 형태로 변환 (예: %EC%95%88%EB%85%95.pdf)
        encoded_filename = quote(f"nametag_{brand_name}_guideline.pdf")
        
        # 3. filename*=utf-8'' 포맷을 사용하여 한글 파일명 헤더에 삽입
        headers = {"Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}"}

        return StreamingResponse(file_iterator(tmp.name), media_type="application/pdf", headers=headers)
    except Exception as exc:
        print(f"[DEBUG] PDF 생성 오류: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-v2")
async def generate_v2_pdf(req: ReportV2PdfRequest):
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as exc:
        raise HTTPException(status_code=500, detail="PDF 생성을 위해 WeasyPrint와 시스템 라이브러리가 필요합니다.") from exc
    try:
        pages = {page_id: page.model_dump(mode="json") for page_id, page in req.pages.items()}
        for page_id, page in pages.items():
            apply_backend_calculations(page_id, page)
        for page_id, page in pages.items():
            errors = validate_page_result(page_id, page, pages)
            if errors:
                raise HTTPException(
                    status_code=422,
                    detail={"page_id": page_id, "contract_errors": errors},
                )
        layouts = [layout.model_dump(mode="json") for layout in req.page_layouts]
        html_content = (
            build_report_v2_compact_html(pages)
            if len(pages) >= 20
            else build_report_v2_html(pages, layouts)
        )
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        HTML(string=html_content).write_pdf(tmp.name)
        tmp.close()

        def file_iterator(path: str, chunk_size: int = 4096):
            try:
                with open(path, "rb") as file:
                    while chunk := file.read(chunk_size):
                        yield chunk
            finally:
                try:
                    os.remove(path)
                except OSError:
                    pass

        from urllib.parse import quote
        filename = quote(f"nametag_{req.brand_name}_V2_report.pdf")
        return StreamingResponse(
            file_iterator(tmp.name),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename*=utf-8''{filename}"},
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"V2 PDF 생성 실패: {exc}") from exc
