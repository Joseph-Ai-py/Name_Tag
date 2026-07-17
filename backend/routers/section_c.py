from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_C0_visual_interview_prompt, get_C1_visual_identity_prompt
# 스키마 강제 함수(request_gemini_with_schema) 임포트
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse

# 섹션 C 도면(Schema) 임포트
from schemas.schema_c import CResponseSchema

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
        print(f"[DEBUG] C 시각적 인터뷰 질문 생성 요청 시작...", flush=True)
        result = request_gemini_text(get_C0_visual_interview_prompt(req.brand_info.model_dump()))
        print(f"[DEBUG] C 인터뷰 생성 결과: {result}", flush=True)
        return result
    except Exception as exc:
        print(f"[FATAL ERROR] /interview 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_c(req: CGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b}"

        print(f"[DEBUG] C1(스키마 강제) 프롬프트 요청 시작...", flush=True)
        
        # 💡 3. AI에게 프롬프트와 함께 스키마 도면(CResponseSchema)을 주입하여 강제함
        result = request_gemini_with_schema(
            get_C1_visual_identity_prompt(brand, previous_context, req.interview_data_c),
            schema=CResponseSchema
        )
        print(f"[DEBUG] C1(스키마 강제) 결과: {result}", flush=True)

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

        print(f"[DEBUG] C 재생성({req.target}) 요청 시작...", flush=True)
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_c.re-generate", "target": req.target})
        print(f"[DEBUG] C 재생성 원본 결과: {result}", flush=True)

        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            print(f"[DEBUG] C 재생성 정규화 성공: {validated.dict()}", flush=True)
            return {"target": req.target, "result": validated.dict()}
        except Exception as parse_exc:
            print(f"[ERROR] C 재생성 결과 파싱 실패. 빈 리스트 반환. 에러: {str(parse_exc)}", flush=True)
            return {"target": req.target, "result": {"candidates": []}}
            
    except Exception as exc:
        print(f"[FATAL ERROR] /re-generate 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))