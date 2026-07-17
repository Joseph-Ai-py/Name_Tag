# 파일 위치: backend/routers/section_a.py

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
# 1. request_gemini_with_schema 임포트
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse

# 2. schema_a.py 의 스키마들 임포트
from schemas.schema_a import A1ResponseSchema, A2ResponseSchema, A3ResponseSchema

router = APIRouter()

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
        
        # 3. 일반 text 요청 대신 with_schema 요청으로 변경하고, schema= 도면 주입
        print(f"[DEBUG] A1(스키마 강제) 프롬프트 요청 시작...", flush=True)
        a1 = request_gemini_with_schema(get_A1_philosophy_prompt(brand, text), schema=A1ResponseSchema)
        print(f"[DEBUG] A1 결과: {a1}", flush=True)
        
        print(f"[DEBUG] A2(스키마 강제) 프롬프트 요청 시작...", flush=True)
        a2 = request_gemini_with_schema(get_A2_story_prompt(brand, text), schema=A2ResponseSchema)
        print(f"[DEBUG] A2 결과: {a2}", flush=True)
        
        print(f"[DEBUG] A3(스키마 강제) 프롬프트 요청 시작...", flush=True)
        a3 = request_gemini_with_schema(get_A3_positioning_prompt(brand, text), schema=A3ResponseSchema)
        print(f"[DEBUG] A3 결과: {a3}", flush=True)

        merged: dict[str, object] = {}
        # 스키마 강제를 통과했기 때문에 무조건 dict임이 보장됨
        for part in [a1, a2, a3]:
            merged.update(part)

        print(f"[DEBUG] 최종 완성된 data_a: {merged}", flush=True)
        return {"data_a": merged}
        
    except Exception as exc:
        print(f"[FATAL ERROR] /generate 실행 중 에러 발생: {str(exc)}", flush=True)
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