from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_B1_persona_prompt, get_B2_journey_prompt, get_B_interview_prompt
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse

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


class BRegenRequest(BaseModel):
    brand_info: BrandInfo
    context: dict
    target: str


@router.post("/re-generate")
async def regenerate_b_field(req: BRegenRequest):
    try:
        prompt = f'Produce 3 alternative short values for `{req.target}` based on brand info {req.brand_info} and context {req.context}. Return JSON only: {{"candidates": [..]}}'
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_b.re-generate", "target": req.target})
        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": req.target, "result": validated.dict()}
        except Exception:
            return {"target": req.target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))