from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import (
    get_A1_philosophy_prompt,
    get_A2_story_prompt,
    get_A3_positioning_prompt,
    get_A_interview_prompt,
)
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


class AInterviewRequest(BaseModel):
    brand_info: BrandInfo


class AGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str


@router.post("/interview")
async def get_interview_questions(req: AInterviewRequest):
    try:
        return request_gemini_text(get_A_interview_prompt(req.brand_info.model_dump()))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_a(req: AGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        text = req.interview_data_a
        a1 = request_gemini_text(get_A1_philosophy_prompt(brand, text))
        a2 = request_gemini_text(get_A2_story_prompt(brand, text))
        a3 = request_gemini_text(get_A3_positioning_prompt(brand, text))

        merged: dict[str, object] = {}
        for part in [a1, a2, a3]:
            merged.update(part)

        return {"data_a": merged}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))