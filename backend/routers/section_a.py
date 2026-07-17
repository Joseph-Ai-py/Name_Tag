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
# 1. request_gemini_with_schema 임포트 및 공용 인터뷰 스키마 임포트
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse
from schemas.schema_interview import InterviewResponseSchema # 💡 추가

# 2. schema_a.py 의 스키마들 임포트
from schemas.schema_a import A1ResponseSchema, A2ResponseSchema, A3ResponseSchema

router = APIRouter()

# =====================================================================
# 프론트엔드 데이터를 받아낼 필수 데이터 모델
# =====================================================================
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
    context: dict | None = None
    target: str

# =====================================================================

@router.post("/interview")
async def get_interview_questions(req: AInterviewRequest):
    try:
        print(f"[DEBUG] A 인터뷰(스키마 강제) 프롬프트 요청 시작...", flush=True)
        # 💡 일반 text 요청을 스키마 강제 요청으로 변경하여 데이터 오염 차단
        result = request_gemini_with_schema(
            get_A_interview_prompt(req.brand_info.model_dump()),
            schema=InterviewResponseSchema
        )
        print(f"[DEBUG] A 인터뷰 생성 결과: {result}", flush=True)
        return result
    except Exception as exc:
        print(f"[FATAL ERROR] /interview(A) 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_a(req: AGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        text = req.interview_data_a

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

        prompt = get_A_field_regen_prompt(brand, target, context)
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_a.re-generate", "target": target})

        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": target, "result": validated.dict()}
        except Exception:
            return {"target": target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))