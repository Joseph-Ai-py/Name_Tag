from __future__ import annotations

from fastapi.staticfiles import StaticFiles
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_DE_identity_prompt, get_DE_interview_prompt
#  스키마 강제 함수(request_gemini_with_schema) 임포트
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite, request_gemini_with_schema
from utils.ai_utils import normalize_candidates
from schemas.schema_interview import InterviewResponseSchema
from schemas.ai_models import CandidatesResponse
from services.image_service import generate_character_image, generate_logo_image

# 섹션 DE 도면(Schema) 임포트
from schemas.schema_de import DEResponseSchema

router = APIRouter()


class BrandInfo(BaseModel):
    brand_name: str
    brand_name_en: str
    name_meaning: str
    slogan: str
    story_summary: str
    seed_color: str
    seed_color_reason: str


class DEInterviewRequest(BaseModel):
    brand_info: BrandInfo
    interview_data_c: str


class DEGenerateRequest(BaseModel):
    brand_info: BrandInfo
    data_c: dict
    interview_data_a: str
    interview_data_b: str
    interview_data_c: str
    interview_data_de: str


# --- 공통 헬퍼 함수 ---
def to_url_path(abs_path: str | None) -> str | None:
    """절대 경로를 프론트엔드에서 접근 가능한 /assets/... 형태의 URL 경로로 변환"""
    if not abs_path:
        return None
    normalized = abs_path.replace("\\", "/")
    # 메인 서버의 마운트 포인트("/assets")와 맞추기 위해 "assets/"를 찾음
    index = normalized.find("assets/")
    return "/" + normalized[index:] if index != -1 else None


@router.post("/interview")
async def get_interview_questions(req: DEInterviewRequest):
    try:
        print(f"[DEBUG] DE 인터뷰(스키마 강제) 질문 생성 요청 시작...", flush=True)
        # 💡 일반 text 요청 대신 인터뷰 스키마 강제 적용
        result = request_gemini_with_schema(
            get_DE_interview_prompt(req.brand_info.model_dump(), req.interview_data_c),
            schema=InterviewResponseSchema
        )
        print(f"[DEBUG] DE 인터뷰 생성 결과: {result}", flush=True)
        return result
    except Exception as exc:
        print(f"[FATAL ERROR] /interview(DE) 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))



@router.post("/generate")
async def generate_section_de(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}"

        print(f"[DEBUG] section-de generate start - brand={brand['brand_name']}, "
              f"data_c_keys={list(req.data_c.keys())}, context_lengths={{'a': len(req.interview_data_a), 'b': len(req.interview_data_b), 'c': len(req.interview_data_c), 'de': len(req.interview_data_de)}}", flush=True)

        result = request_gemini_with_schema(
            get_DE_identity_prompt(brand, req.data_c, previous_context, req.interview_data_de),
            schema=DEResponseSchema
        )
        print(f"[DEBUG] section-de identity generated (스키마 강제) - keys={list(result.keys())}", flush=True)

        print(f"[DEBUG] 로고 및 캐릭터 이미지 생성 시작...", flush=True)

        logo_path = generate_logo_image(
            brand_name=brand["brand_name"],
            result=result,
            data_c=req.data_c,
            brand_info=brand,
            deepdive_answers_text=req.interview_data_de,
        )

        intro = result["character_guide"]["intro"]
        reasoning = result["character_guide"]["reasoning"]
        char_path = generate_character_image(
            brand_name=brand["brand_name"],
            char_name=intro["name"],
            char_appearance=intro["appearance"],
            symbolic_value=intro["symbolic_value"],
            emotional_connection=reasoning["emotional_connection"],
            data_c=req.data_c,
        )

        print(f"[DEBUG] section-de images generated - logo_path={logo_path}, char_path={char_path}", flush=True)

        result["logo_path"] = to_url_path(logo_path)
        result["char_path"] = to_url_path(char_path)

        print(f"[DEBUG] section-de generate done - logo_url={result['logo_path']}, char_url={result['char_path']}", flush=True)
        print(f"[DEBUG] section-de final result - {result}", flush=True)

        return {"data_de": result}
    except Exception as exc:
        print(f"[FATAL ERROR] /generate(DE) 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-logo")
async def generate_logo_only(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}"
        print(f"[DEBUG] DE 단독 로고 생성 요청 시작...", flush=True)

        result = request_gemini_with_schema(
            get_DE_identity_prompt(brand, req.data_c, previous_context, req.interview_data_de),
            schema=DEResponseSchema
        )

        logo_path = generate_logo_image(
            brand_name=brand["brand_name"],
            result=result,
            data_c=req.data_c,
            brand_info=brand,
            deepdive_answers_text=req.interview_data_de,
        )
        result["logo_path"] = to_url_path(logo_path)

        print(f"[DEBUG] 단독 로고 생성 완료: {result['logo_path']}", flush=True)
        return {"logo_path": result["logo_path"], "data_de": result}
    except Exception as exc:
        print(f"[FATAL ERROR] /generate-logo 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-character")
async def generate_character_only(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}"
        print(f"[DEBUG] DE 단독 캐릭터 생성 요청 시작...", flush=True)

        result = request_gemini_with_schema(
            get_DE_identity_prompt(brand, req.data_c, previous_context, req.interview_data_de),
            schema=DEResponseSchema
        )

        intro = result["character_guide"]["intro"]
        reasoning = result["character_guide"]["reasoning"]
        char_path = generate_character_image(
            brand_name=brand["brand_name"],
            char_name=intro["name"],
            char_appearance=intro["appearance"],
            symbolic_value=intro["symbolic_value"],
            emotional_connection=reasoning["emotional_connection"],
            data_c=req.data_c,
        )
        result["char_path"] = to_url_path(char_path)

        print(f"[DEBUG] 단독 캐릭터 생성 완료: {result['char_path']}", flush=True)
        return {"char_path": result["char_path"], "data_de": result}
    except Exception as exc:
        print(f"[FATAL ERROR] /generate-character 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


class DERegenRequest(BaseModel):
    brand_info: BrandInfo
    context: dict
    target: str


@router.post("/re-generate")
async def regenerate_de_field(req: DERegenRequest):
    try:
        prompt = f'Produce 3 alternative short values for `{req.target}` based on brand info {req.brand_info} and context {req.context}. Return JSON only: {{"candidates": [..]}}'

        print(f"[DEBUG] DE 재생성({req.target}) 요청 시작...", flush=True)
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_de.re-generate", "target": req.target})
        print(f"[DEBUG] DE 재생성 원본 결과: {result}", flush=True)

        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            print(f"[DEBUG] DE 재생성 정규화 성공: {validated.dict()}", flush=True)
            return {"target": req.target, "result": validated.dict()}
        except Exception as parse_exc:
            print(f"[ERROR] DE 재생성 결과 파싱 실패. 빈 리스트 반환. 에러: {str(parse_exc)}", flush=True)
            return {"target": req.target, "result": {"candidates": []}}

    except Exception as exc:
        print(f"[FATAL ERROR] /re-generate(DE) 실행 중 에러 발생: {str(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))