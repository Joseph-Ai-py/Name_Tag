from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_C0_visual_interview_prompt, get_C1_visual_identity_prompt
from services.gemini_service import request_gemini_text

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class CInterviewRequest(BaseModel):
    brand_info: BrandInfo


class CGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str
    interview_data_b: str
    interview_data_c: str


@router.post("/interview")
async def get_interview_questions(req: CInterviewRequest):
    try:
        return request_gemini_text(get_C0_visual_interview_prompt(req.brand_info.model_dump()))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_c(req: CGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b}"
        result = request_gemini_text(
            get_C1_visual_identity_prompt(brand, previous_context, req.interview_data_c)
        )
        return {"data_c": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))