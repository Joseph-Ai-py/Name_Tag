from __future__ import annotations

import os
import tempfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from weasyprint import HTML

from pdf.nametag_pdf_builder import assemble_html

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

        brand_name = req.brand_info.get("brand_name", "brand")
        return FileResponse(
            path=tmp.name,
            media_type="application/pdf",
            filename=f"nametag_{brand_name}_guideline.pdf",
        )
    except Exception as exc:
        print(f"[DEBUG] PDF 생성 오류: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))