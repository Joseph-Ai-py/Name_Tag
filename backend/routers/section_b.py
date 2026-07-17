# 파일 위치: backend/routers/section_b.py

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_B1_persona_prompt, get_B2_journey_prompt, get_B_interview_prompt
# 1. 스키마 강제 함수 및 공용 인터뷰 스키마 임포트
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from schemas.schema_interview import InterviewResponseSchema
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
        print(f"[DEBUG] B 인터뷰(스키마 강제) 프롬프트 요청 시작...", flush=True)
        # 💡 일반 text 요청 대신 인터뷰 스키마 강제 적용
        result = request_gemini_with_schema(
            get_B_interview_prompt(req.brand_info.model_dump()),
            schema=InterviewResponseSchema
        )
        print(f"[DEBUG] B 인터뷰 생성 결과: {result}", flush=True)
        return result
    except Exception as exc:
        print(f"[FATAL ERROR] /interview(B) 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_b(req: BGenerateRequest):
    try:
        brand = req.brand_info.model_dump()

        print(f"[DEBUG] B1(페르소나) 프롬프트 요청 시작...", flush=True)
        b1 = request_gemini_text(get_B1_persona_prompt(brand, req.interview_data_a, req.interview_data_b))
        print(f"[DEBUG] B1 결과: {b1}", flush=True)

        print(f"[DEBUG] B2(저니) 프롬프트 요청 시작...", flush=True)
        b2 = request_gemini_text(get_B2_journey_prompt(brand, req.interview_data_a, req.interview_data_b))
        print(f"[DEBUG] B2 결과: {b2}", flush=True)

        merged: dict[str, object] = {}
        for idx, part in enumerate([b1, b2], start=1):
            if isinstance(part, dict):
                merged.update(part)
            else:
                print(f"[ERROR] B{idx}의 결과값이 딕셔너리가 아닙니다! 데이터 병합 누락. 내용: {part}", flush=True)

        print(f"[DEBUG] 최종 완성된 data_b: {merged}", flush=True)
        return {"data_b": merged}
    except Exception as exc:
        print(f"[FATAL ERROR] /generate 실행 중 에러 발생: {str(exc)}", flush=True)
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