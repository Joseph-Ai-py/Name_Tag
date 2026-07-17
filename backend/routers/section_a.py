from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import (
    get_A1_philosophy_prompt,
    get_A2_story_prompt,
    get_A3_positioning_prompt,
    get_A_interview_prompt,
    get_A_field_regen_prompt,
)
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


class AInterviewRequest(BaseModel):
    brand_info: BrandInfo


class AGenerateRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_a: str


class ARegenRequest(BaseModel):
    brand_info: BrandInfo
    context: dict
    target: str


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
        
        print(f"[DEBUG] A1 프롬프트 요청 시작...")
        a1 = request_gemini_text(get_A1_philosophy_prompt(brand, text))
        print(f"[DEBUG] A1 결과: {a1}")
        
        print(f"[DEBUG] A2 프롬프트 요청 시작...")
        a2 = request_gemini_text(get_A2_story_prompt(brand, text))
        print(f"[DEBUG] A2 결과: {a2}")
        
        print(f"[DEBUG] A3 프롬프트 요청 시작...")
        a3 = request_gemini_text(get_A3_positioning_prompt(brand, text))
        print(f"[DEBUG] A3 결과: {a3}")

        merged: dict[str, object] = {}
        for idx, part in enumerate([a1, a2, a3], start=1):
            # 방어적 코드: part가 딕셔너리인지 확인
            if isinstance(part, dict):
                merged.update(part)
            else:
                print(f"[ERROR] A{idx}의 결과값이 딕셔너리가 아닙니다! 내용: {part}")

        print(f"[DEBUG] 최종 완성된 data_a: {merged}")
        return {"data_a": merged}
        
    except Exception as exc:
        print(f"[FATAL ERROR] /generate 실행 중 에러 발생: {str(exc)}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/re-generate")
async def regenerate_field(req: ARegenRequest):
    try:
        brand = req.brand_info.model_dump()
        target = req.target
        context = req.context or {}

        # Build a field-specific prompt using the A-section prompt templates
        prompt = get_A_field_regen_prompt(brand, target, context)

        # call flash-lite wrapper for small regenerations (logs usage)
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_a.re-generate", "target": target})

        # normalize candidates into consistent shape
        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": target, "result": validated.dict()}
        except Exception:
            return {"target": target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))