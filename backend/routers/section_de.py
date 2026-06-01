from __future__ import annotations

from fastapi.staticfiles import StaticFiles
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_DE_identity_prompt, get_DE_interview_prompt
from services.gemini_service import request_gemini_text, request_gemini_text_flash_lite
from utils.ai_utils import normalize_candidates
from schemas.ai_models import CandidatesResponse
from services.image_service import generate_character_image, generate_logo_image

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


@router.post("/interview")
async def get_interview_questions(req: DEInterviewRequest):
    try:
        return request_gemini_text(
            get_DE_interview_prompt(req.brand_info.model_dump(), req.interview_data_c)
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate")
async def generate_section_de(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        previous_context = f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}"
        print(
            f"[DEBUG] section-de generate start - brand={brand['brand_name']}, "
            f"data_c_keys={list(req.data_c.keys())}, context_lengths={{'a': len(req.interview_data_a), 'b': len(req.interview_data_b), 'c': len(req.interview_data_c), 'de': len(req.interview_data_de)}}"
        )
        result = request_gemini_text(
            get_DE_identity_prompt(brand, req.data_c, previous_context, req.interview_data_de)
        )
        print(f"[DEBUG] section-de identity generated - keys={list(result.keys())}")

        logo_path = generate_logo_image(brand["brand_name"], result)
        char_path = generate_character_image(brand["brand_name"], result)

        print(f"[DEBUG] section-de images generated - logo_path={logo_path}, char_path={char_path}")

        def to_url_path(abs_path: str | None) -> str | None:
            if not abs_path:
                return None
            normalized = abs_path.replace("\\", "/")
            index = normalized.find("assets/")
            return "/" + normalized[index:] if index != -1 else None

        result["logo_path"] = to_url_path(logo_path)
        result["char_path"] = to_url_path(char_path)
        print(
            f"[DEBUG] section-de generate done - brand={brand['brand_name']}, "
            f"logo_path={result['logo_path']}, char_path={result['char_path']}"
        )

        print(f"[DEBUG] section-de final result - {result}")

        return {"data_de": result}
    except Exception as exc:
        print(f"[DEBUG] section-de generate error - {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-logo")
async def generate_logo_only(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        result = request_gemini_text(get_DE_identity_prompt(brand, req.data_c, f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}", req.interview_data_de))
        logo_path = generate_logo_image(brand["brand_name"], result)

        def to_url_path(abs_path: str | None) -> str | None:
            if not abs_path:
                return None
            normalized = abs_path.replace("\\", "/")
            index = normalized.find("backend/assets/")
            return "/" + normalized[index:] if index != -1 else None

        result["logo_path"] = to_url_path(logo_path)
        return {"logo_path": result["logo_path"], "data_de": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-character")
async def generate_character_only(req: DEGenerateRequest):
    try:
        brand = req.brand_info.model_dump()
        result = request_gemini_text(get_DE_identity_prompt(brand, req.data_c, f"{req.interview_data_a} + {req.interview_data_b} + {req.interview_data_c}", req.interview_data_de))
        char_path = generate_character_image(brand["brand_name"], result)

        def to_url_path(abs_path: str | None) -> str | None:
            if not abs_path:
                return None
            normalized = abs_path.replace("\\", "/")
            index = normalized.find("backend/   assets/")
            return "/" + normalized[index:] if index != -1 else None

        result["char_path"] = to_url_path(char_path)
        return {"char_path": result["char_path"], "data_de": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


class DERegenRequest(BaseModel):
    brand_info: BrandInfo
    context: dict
    target: str


@router.post("/re-generate")
async def regenerate_de_field(req: DERegenRequest):
    try:
        prompt = f'Produce 3 alternative short values for `{req.target}` based on brand info {req.brand_info} and context {req.context}. Return JSON only: {{"candidates": [..]}}'
        result = request_gemini_text_flash_lite(prompt, metadata={"endpoint": "section_de.re-generate", "target": req.target})
        try:
            candidates = normalize_candidates(result)
            validated = CandidatesResponse(candidates=candidates)
            return {"target": req.target, "result": validated.dict()}
        except Exception:
            return {"target": req.target, "result": {"candidates": []}}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))