from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_O_interview_prompt, get_O_mvb_prompt
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse

from services.gemini_service import request_gemini_with_schema
from schemas.schema_interview import InterviewResponseSchema


router = APIRouter()


class BrandData(BaseModel):
    business_type: str
    vibes: list[str]
    target: str
    keywords: str = ""


class OInterviewRequest(BaseModel):
    brand_data: BrandData


class OMvbRequest(BaseModel):
    brand_data: BrandData
    interview_data: str


def build_base_prompt(brand_data: BrandData, core_prompt: str, brand_name: str = "브랜드명 미정") -> str:
    return f"""
[기본 입력 정보]
- 업종/서비스: {brand_data.business_type}
- 브랜드 감성: {', '.join(brand_data.vibes)}
- 타겟 고객: {brand_data.target}
- 확정된 브랜드명: {brand_name}
- 추가 키워드: {brand_data.keywords or '없음'}
""" + core_prompt


@router.post("/interview")
async def get_initial_interview(req: dict):
    try:
        # 기존 request_gemini_text 대신 with_schema를 써서 무결성 보장!
        return request_gemini_with_schema(
            get_O_interview_prompt(), 
            schema=InterviewResponseSchema
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/candidates")
async def get_mvb_candidates(req: OMvbRequest):
    try:
        prompt = build_base_prompt(req.brand_data, get_O_mvb_prompt(req.interview_data))
        return request_gemini_text(prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


class ORegenRequest(BaseModel):
    brand_data: BrandData
    context: dict
    target: str


@router.post("/re-generate")
async def regenerate_o_field(req: ORegenRequest):
    try:
        prompt = f'Produce 3 alternative short values for `{req.target}` based on brand info {req.brand_info} and context {req.context}. Return JSON only: {{"candidates": [..]}}'
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_o.re-generate", "target": req.target})
        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": req.target, "result": validated.dict()}
        except Exception:
            return {"target": req.target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))