from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_B1_persona_prompt, get_B2_journey_prompt, get_B_interview_prompt
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


class BInterviewRequest(BaseModel):
    brand_info: BrandInfo


class BGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str
    interview_data_b: str


@router.post("/interview")
async def get_interview_questions(req: BInterviewRequest):
    try:
        return request_gemini_text(get_B_interview_prompt(req.brand_info.model_dump()))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_b(req: BGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        b1 = request_gemini_text(get_B1_persona_prompt(brand, req.interview_data_a, req.interview_data_b))
        b2 = request_gemini_text(get_B2_journey_prompt(brand, req.interview_data_a, req.interview_data_b))
        merged: dict[str, object] = {}
        for part in [b1, b2]:
            merged.update(part)
        return {"data_b": merged}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))