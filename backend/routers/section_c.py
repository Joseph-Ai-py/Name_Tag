from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_C0_visual_interview_prompt, get_C1_visual_identity_prompt
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


class CRegenRequest(BaseModel):
    brand_info: BrandInfo
    context: dict
    target: str


@router.post("/re-generate")
async def regenerate_c_field(req: CRegenRequest):
    try:
        prompt = f'Produce 3 alternative short values for `{req.target}` based on brand info {req.brand_info} and context {req.context}. Return JSON only: {{"candidates": [..]}}'
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_c.re-generate", "target": req.target})
        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": req.target, "result": validated.dict()}
        except Exception:
            return {"target": req.target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))