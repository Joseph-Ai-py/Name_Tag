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
        
        print(f"[DEBUG] C1(시각적 정체성) 프롬프트 요청 시작...", flush=True)
        result = request_gemini_text(
            get_C1_visual_identity_prompt(brand, previous_context, req.interview_data_c)
        )
        print(f"[DEBUG] C1 결과: {result}", flush=True)

        # 방어적 코드: Gemini의 결과가 딕셔너리 형태가 아닐 경우 프론트엔드 파싱 에러 방지용 경고
        if not isinstance(result, dict):
            print(f"[WARN] C1 결과값이 딕셔너리가 아닙니다! 프론트엔드 렌더링에 문제가 생길 수 있습니다. 내용: {result}", flush=True)

        return {"data_c": result}
    except Exception as exc:
        print(f"[FATAL ERROR] /generate 실행 중 에러 발생: {str(exc)}", flush=True)
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