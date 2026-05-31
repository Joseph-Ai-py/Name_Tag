from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prompts.nametag_prompts import get_DE_identity_prompt, get_DE_interview_prompt
from services.gemini_service import request_gemini_text
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
        result = request_gemini_text(
            get_DE_identity_prompt(brand, req.data_c, previous_context, req.interview_data_de)
        )

        logo_path = generate_logo_image(brand["brand_name"], result)
        char_path = generate_character_image(brand["brand_name"], result)

        def to_url_path(abs_path: str | None) -> str | None:
            if not abs_path:
                return None
            normalized = abs_path.replace("\\", "/")
            index = normalized.find("assets/")
            return "/" + normalized[index:] if index != -1 else None

        result["logo_path"] = to_url_path(logo_path)
        result["char_path"] = to_url_path(char_path)

        return {"data_de": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))