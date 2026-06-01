from __future__ import annotations

import os
import tempfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

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
<<<<<<< HEAD
        
        # 1. URL 인코딩을 위한 패키지 불러오기 (파일 최상단에 적어도 되지만 여기에 적어도 작동합니다)
        from urllib.parse import quote
        
        # 2. 파일명 전체를 URL 안전한 형태로 변환 (예: %EC%95%88%EB%85%95.pdf)
        encoded_filename = quote(f"nametag_{brand_name}_guideline.pdf")
        
        # 3. filename*=utf-8'' 포맷을 사용하여 한글 파일명 헤더에 삽입
        headers = {"Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}"}
        
=======
        headers = {"Content-Disposition": f'attachment; filename="nametag_{brand_name}_guideline.pdf"'}
>>>>>>> dba00ee0acc31e840322be9a20539dc3da0d7b01
        return StreamingResponse(file_iterator(tmp.name), media_type="application/pdf", headers=headers)
    except Exception as exc:
        print(f"[DEBUG] PDF 생성 오류: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))