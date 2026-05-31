from __future__ import annotations

import os
import tempfile
from pathlib import Path

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


def _convert_web_path_to_file_path(web_path: str | None) -> str | None:
    """웹 경로 (e.g., '/assets/...') 를 파일 시스템 경로로 변환"""
    if not web_path:
        return None
    
    # /assets/... 형식의 경로를 파일 경로로 변환
    if web_path.startswith("/assets/"):
        relative = web_path[1:]  # 앞의 / 제거
        root = Path(__file__).resolve().parents[2]  # 프로젝트 루트
        file_path = root / relative
        return str(file_path)
    
    return None


@router.post("/generate")
async def generate_pdf(req: PdfRequest):
    try:
        print(f"[DEBUG] PDF 생성 시작 - brand_name: {req.brand_info.get('brand_name')}")
        
        # data_de에서 이미지 경로 추출 및 파일 경로로 변환
        logo_path = None
        char_path = None
        
        if req.data_de and isinstance(req.data_de, dict):
            web_logo_path = req.data_de.get("logo_path")
            web_char_path = req.data_de.get("char_path")
            
            logo_path = _convert_web_path_to_file_path(web_logo_path)
            char_path = _convert_web_path_to_file_path(web_char_path)
            
            print(f"[DEBUG] 웹 로고 경로: {web_logo_path} -> 파일 경로: {logo_path}")
            print(f"[DEBUG] 웹 캐릭터 경로: {web_char_path} -> 파일 경로: {char_path}")
            print(f"[DEBUG] 로고 파일 존재: {os.path.exists(logo_path) if logo_path else False}")
            print(f"[DEBUG] 캐릭터 파일 존재: {os.path.exists(char_path) if char_path else False}")
        
        # HTML 어셈블 (이미지 경로는 여전히 웹 경로 형식으로 data_de에 저장됨)
        html_content = assemble_html(req.brand_info, req.data_a, req.data_b, req.data_c, req.data_de)
        
        # PDF 생성 (base_url은 이미지 경로가 file:// 형식이므로 무시됨)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        HTML(string=html_content, base_url="http://localhost:8000").write_pdf(tmp.name)
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