"""Brand generation router."""
from typing import Any, Optional
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.brand_generator import (
    generate_brand_identity,
    generate_logo_variables,
)

router = APIRouter()


class BrandGenerateRequest(BaseModel):
    """Request model for brand generation."""

    business_type: str = Field(..., min_length=3, description="Type of business/service")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes (1-4)")
    target: str = Field(..., min_length=3, description="Target customer description")
    keywords: str = Field(default="", description="Additional keywords")
    session_id: Optional[str] = Field(default=None, description="Optional session ID for tracking")


class TypographyInfo(BaseModel):
    """Typography information."""
    korean: str
    english: str
    reason: str

class CharacterInfo(BaseModel):
    """Character information."""
    name: str
    concept: str
    personality: str
    visual: str

class LogoDesignInfo(BaseModel):
    """Logo design information."""
    brand_name: str
    brand_topic: str
    core_value: str
    target_mood: str
    symbol_type: str
    font_style: str
    font_reference: str
    font_weight: str
    brand_color: str
    logo_type: str
    background: str

class BrandInfo(BaseModel):
    """Individual brand information with all design details."""
    name: str
    meaning: str
    story: str
    slogan: str
    typography: TypographyInfo
    character: CharacterInfo
    logo_design: LogoDesignInfo

class BrandGenerateResponse(BaseModel):
    """Response model for brand generation - each brand has full design info."""
    session_id: str
    brands: list[BrandInfo]


class LogoVariablesRequest(BaseModel):
    """Request model for logo variables generation."""

    business_type: str = Field(..., min_length=3, description="Type of business/service")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes (1-4)")
    target: str = Field(..., min_length=3, description="Target customer description")
    keywords: str = Field(default="", description="Additional keywords")
    session_id: Optional[str] = Field(default=None, description="Optional session ID for tracking")


class LogoVariablesResponse(BaseModel):
    """Response model for logo variables generation."""

    session_id: str
    brand_identity: dict[str, Any]
    logo_variables: dict[str, Any]
    recommendations_reason: str
    variables_summary: dict[str, Any]


@router.post("/brand/generate", response_model=BrandGenerateResponse)
async def generate_brand(request: BrandGenerateRequest) -> dict[str, Any]:
    """
    Generate brand identity based on user input.

    Args:
        request: BrandGenerateRequest with business_type, vibes, target, keywords

    Returns:
        BrandGenerateResponse with brands, typography, and character

    Raises:
        HTTPException: If generation fails
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = generate_brand_identity(
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
            session_id=session_id,
        )
        result["session_id"] = session_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/brand/logo-variables", response_model=LogoVariablesResponse)
async def get_logo_variables(request: LogoVariablesRequest) -> dict[str, Any]:
    """
    Generate logo variables and recommendations based on user input.
    
    This endpoint receives user input and returns:
    - Recommended brand name, topic, core values
    - Recommended logo variables (mood, color, font, symbol, etc.)
    - All variables are tracked with detailed logging

    Args:
        request: LogoVariablesRequest with business_type, vibes, target, keywords

    Returns:
        LogoVariablesResponse with all brand and logo variables

    Raises:
        HTTPException: If generation fails
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = generate_logo_variables(
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
            session_id=session_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로고 변수 생성 실패: {str(e)}")


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}



class BrandGenerateRequest(BaseModel):
    """Request model for brand generation."""

    business_type: str = Field(..., min_length=3, description="Type of business/service")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes (1-4)")
    target: str = Field(..., min_length=3, description="Target customer description")
    keywords: str = Field(default="", description="Additional keywords")


class BrandGenerateResponse(BaseModel):
    """Response model for brand generation."""

    brands: list[dict[str, str]]
    typography: dict[str, str]
    character: dict[str, str]


class LogoGenerateRequest(BaseModel):
    """Request model for logo image generation."""

    brand_name: str = Field(..., min_length=1, description="Brand name")
    brand_story: str = Field(..., min_length=1, description="Brand story/description")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes (1-4)")
    symbol_type: Optional[str] = Field(default="기하학적", description="Symbol style: 기하학적, 유기적, 미니멀, 레터마크, 아이콘형")
    brand_color: Optional[str] = Field(default="", description="Brand color (auto-mapped if empty)")
    logo_type: Optional[str] = Field(default="심볼+텍스트 조합", description="Logo composition type")
    background: Optional[str] = Field(default="흰색", description="Background color")


class LogoGenerateResponse(BaseModel):
    """Response model for logo generation."""

    image: str = Field(..., description="Base64 encoded logo image")


class CharacterGenerateRequest(BaseModel):
    """Request model for character image generation."""

    character_name: str = Field(..., min_length=1, description="Character name")
    character_concept: str = Field(..., min_length=1, description="Character concept")
    character_visual: str = Field(..., min_length=1, description="Character visual description")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes (1-4)")
    brand_name: Optional[str] = Field(default="", description="Brand name for context")
    brand_topic: Optional[str] = Field(default="", description="Brand topic for context")
    core_value: Optional[str] = Field(default="", description="Core values for context")
    character_style: Optional[str] = Field(default="플랫 일러스트", description="Illustration style")
    character_age_feel: Optional[str] = Field(default="나이 초월", description="Age feeling")


class CharacterGenerateResponse(BaseModel):
    """Response model for character generation."""

    image: str = Field(..., description="Base64 encoded character image")


class LogoGenerateContextRequest(BaseModel):
    """Request model for logo generation with Name Tag prompt template."""

    brand_name: str = Field(..., min_length=1, description="Brand name")
    brand_topic: str = Field(..., min_length=1, description="Business topic/industry")
    core_value: str = Field(..., min_length=1, description="Core brand values")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes")
    brand_color: str = Field(default="", description="Preferred brand color (auto-mapped if empty)")
    symbol_type: str = Field(
        default="기하학적", description="Symbol style: 기하학적, 유기적, 미니멀, 레터마크, 아이콘형"
    )
    logo_type: str = Field(default="심볼+텍스트 조합", description="Logo composition type")
    background: str = Field(default="흰색", description="Background color")


class CharacterGenerateContextRequest(BaseModel):
    """Request model for character generation with Name Tag prompt template."""

    brand_name: str = Field(..., min_length=1, description="Brand name")
    brand_topic: str = Field(..., min_length=1, description="Business topic/industry")
    core_value: str = Field(..., min_length=1, description="Core brand values")
    character_name: str = Field(..., min_length=1, description="Character name")
    character_concept: str = Field(..., min_length=1, description="Character concept")
    character_personality: str = Field(..., min_length=1, description="Character personality (comma-separated)")
    vibes: list[str] = Field(..., min_items=1, max_items=4, description="Brand vibes")
    character_style: str = Field(
        default="플랫 일러스트", description="Illustration style"
    )
    character_age_feel: str = Field(default="나이 초월", description="Age feeling")


class LogoGenerateCustomRequest(BaseModel):
    """Request model for custom logo generation with optional variables."""

    brand_name: str = Field(default="", description="Brand name (optional, auto-inferred if empty)")
    brand_topic: str = Field(default="", description="Business topic/industry (optional, auto-inferred if empty)")
    core_value: str = Field(default="", description="Core brand values (optional, auto-inferred if empty)")
    target_mood: str = Field(default="", description="Target mood for the logo")
    symbol_type: str = Field(
        default="", description="Symbol style (기하학적, 유기적, 미니멀, 레터마크, 아이콘형)"
    )
    font_style: str = Field(default="", description="Font style for the logo")
    font_reference: str = Field(default="", description="Font reference/example")
    font_weight: str = Field(default="", description="Font weight (Light, Regular, Medium, Bold, ExtraBold)")
    vibes: list[str] = Field(default_factory=list, description="Brand vibes (optional)")
    brand_color: str = Field(default="", description="Preferred brand color")
    logo_type: str = Field(default="", description="Logo composition type (심볼만, 텍스트만, 심볼+텍스트 조합)")
    background: str = Field(default="", description="Background color (흰색, 투명, 그라디언트, 색상)")
    # Context for inference
    business_type: str = Field(default="", description="Business type (for inference)")
    target: str = Field(default="", description="Target customer (for inference)")
    keywords: str = Field(default="", description="Additional keywords (for inference)")


class CharacterGenerateCustomRequest(BaseModel):
    """Request model for custom character generation with optional variables."""

    brand_name: str = Field(default="", description="Brand name (optional)")
    brand_topic: str = Field(default="", description="Business topic (optional)")
    core_value: str = Field(default="", description="Core values (optional)")
    character_name: str = Field(default="", description="Character name (optional)")
    character_concept: str = Field(default="", description="Character concept (optional)")
    character_personality: str = Field(default="", description="Character personality (optional)")
    vibes: list[str] = Field(default_factory=list, description="Brand vibes (optional)")
    character_style: str = Field(default="", description="Illustration style (optional)")
    character_age_feel: str = Field(default="", description="Age feeling (optional)")
    # Context for inference
    business_type: str = Field(default="", description="Business type (for inference)")
    target: str = Field(default="", description="Target customer (for inference)")
    keywords: str = Field(default="", description="Additional keywords (for inference)")


class InferVariablesRequest(BaseModel):
    """Request model for variable inference from existing brand data."""

    brand_name: str = Field(default="", description="Brand name")
    brand_topic: str = Field(default="", description="Business topic")
    core_value: str = Field(default="", description="Core values")
    business_type: str = Field(default="", description="Business type")
    vibes: list[str] = Field(default_factory=list, description="Brand vibes")
    target: str = Field(default="", description="Target customer")
    keywords: str = Field(default="", description="Additional keywords")


class InferVariablesResponse(BaseModel):
    """Response model for variable inference."""

    inferred_variables: dict[str, str]
    reasoning: str




@router.post("/brand/generate", response_model=BrandGenerateResponse)
async def generate_brand(request: BrandGenerateRequest) -> dict[str, Any]:
    """
    Generate brand identity based on user input.

    Args:
        request: BrandGenerateRequest with business_type, vibes, target, keywords

    Returns:
        BrandGenerateResponse with brands, typography, and character

    Raises:
        HTTPException: If generation fails
    """
    try:
        result = generate_brand_identity(
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/brand/logo", response_model=LogoGenerateResponse)
async def generate_logo(request: LogoGenerateRequest) -> dict[str, Any]:
    """
    Generate logo image for a brand.

    Args:
        request: LogoGenerateRequest with brand_name, brand_story, vibes

    Returns:
        LogoGenerateResponse with base64 encoded logo image

    Raises:
        HTTPException: If generation fails
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"🔴 Logo request received: {request.model_dump()}")
    
    try:
        logger.error(f"🟡 Calling generate_logo_image with: brand_name={request.brand_name}, vibes={request.vibes}")
        image = generate_logo_image(
            brand_name=request.brand_name,
            brand_story=request.brand_story,
            vibes=request.vibes,
            symbol_type=request.symbol_type or "기하학적",
            brand_color=request.brand_color or "",
            logo_type=request.logo_type or "심볼+텍스트 조합",
            background=request.background or "흰색",
        )
        logger.error(f"🟢 Logo generated successfully")
        return {"image": image}
    except ValueError as e:
        logger.error(f"❌ ValueError: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        logger.error(f"❌ RuntimeError: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Exception: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"로고 생성 중 오류 발생: {str(e)}")


@router.post("/brand/character", response_model=CharacterGenerateResponse)
async def generate_character(request: CharacterGenerateRequest) -> dict[str, Any]:
    """
    Generate character image for a brand.

    Args:
        request: CharacterGenerateRequest with character info and vibes

    Returns:
        CharacterGenerateResponse with base64 encoded character image

    Raises:
        HTTPException: If generation fails
    """
@router.post("/brand/character", response_model=CharacterGenerateResponse)
async def generate_character(request: CharacterGenerateRequest) -> dict[str, Any]:
    """
    Generate character image for a brand.

    Args:
        request: CharacterGenerateRequest with character info and vibes

    Returns:
        CharacterGenerateResponse with base64 encoded character image

    Raises:
        HTTPException: If generation fails
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"🔴 Character request received: {request.model_dump()}")
    
    try:
        logger.error(f"🟡 Calling generate_character_image")
        image = generate_character_image(
            character_name=request.character_name,
            character_concept=request.character_concept,
            character_visual=request.character_visual,
            vibes=request.vibes,
            character_style=request.character_style or "플랫 일러스트",
            character_age_feel=request.character_age_feel or "나이 초월",
            brand_name=request.brand_name or "",
            brand_topic=request.brand_topic or "",
            core_value=request.core_value or "",
        )
        logger.error(f"🟢 Character generated successfully")
        return {"image": image}
    except ValueError as e:
        logger.error(f"❌ ValueError: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        logger.error(f"❌ RuntimeError: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Exception: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"캐릭터 생성 중 오류 발생: {str(e)}")


@router.post("/brand/logo-advanced", response_model=LogoGenerateResponse)
async def generate_logo_advanced(request: LogoGenerateContextRequest) -> dict[str, Any]:
    """
    Generate professional logo using Name Tag prompt template.

    This endpoint uses the detailed logo generation prompt from the 
    Name Tag system to create professional, specification-based logos.

    Args:
        request: LogoGenerateContextRequest with detailed brand context

    Returns:
        LogoGenerateResponse with base64 encoded professional logo image

    Raises:
        HTTPException: If generation fails
    """
    try:
        image = generate_logo_image_with_context(
            brand_name=request.brand_name,
            brand_topic=request.brand_topic,
            core_value=request.core_value,
            vibes=request.vibes,
            brand_color=request.brand_color,
            symbol_type=request.symbol_type,
            logo_type=request.logo_type,
            background=request.background,
        )
        return {"image": image}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로고 생성 중 오류 발생: {str(e)}")


@router.post("/brand/character-advanced", response_model=CharacterGenerateResponse)
async def generate_character_advanced(request: CharacterGenerateContextRequest) -> dict[str, Any]:
    """
    Generate professional character using Name Tag prompt template.

    This endpoint uses the detailed character generation prompt from the 
    Name Tag system to create professional, specification-based characters.

    Args:
        request: CharacterGenerateContextRequest with detailed brand and character context

    Returns:
        CharacterGenerateResponse with base64 encoded professional character image

    Raises:
        HTTPException: If generation fails
    """
    try:
        image = generate_character_image_with_context(
            brand_name=request.brand_name,
            brand_topic=request.brand_topic,
            core_value=request.core_value,
            character_name=request.character_name,
            character_concept=request.character_concept,
            character_personality=request.character_personality,
            vibes=request.vibes,
            character_style=request.character_style,
            character_age_feel=request.character_age_feel,
        )
        return {"image": image}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐릭터 생성 중 오류 발생: {str(e)}")


@router.post("/brand/infer-variables", response_model=InferVariablesResponse)
async def infer_variables(request: InferVariablesRequest) -> dict[str, Any]:
    """
    Infer missing image generation variables from existing brand data.

    Analyzes provided brand information and recommends optimal values
    for logo/character generation variables.

    Args:
        request: InferVariablesRequest with existing brand information

    Returns:
        InferVariablesResponse with inferred variables and reasoning

    Raises:
        HTTPException: If inference fails
    """
    try:
        inferred = infer_missing_variables(
            brand_name=request.brand_name,
            brand_topic=request.brand_topic,
            core_value=request.core_value,
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
        )
        return {
            "inferred_variables": inferred,
            "reasoning": "변수가 기존 브랜드 정보로부터 자동으로 추론되었습니다.",
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"변수 추론 중 오류 발생: {str(e)}")


@router.post("/brand/logo-custom", response_model=LogoGenerateResponse)
async def generate_logo_custom(request: LogoGenerateCustomRequest) -> dict[str, Any]:
    """
    Generate logo with optional/auto-inferred variables.

    If variables are not provided, they will be inferred from available brand data.
    User can provide partial information, and the system will auto-complete.

    Args:
        request: LogoGenerateCustomRequest with optional variables

    Returns:
        LogoGenerateResponse with base64 encoded logo image

    Raises:
        HTTPException: If generation fails
    """
    try:
        # Infer missing variables if needed
        inferred = infer_missing_variables(
            brand_name=request.brand_name,
            brand_topic=request.brand_topic,
            core_value=request.core_value,
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
        )

        # Use provided values if available, otherwise use inferred values
        brand_name = request.brand_name or inferred.get("brand_name", "Brand")
        brand_topic = request.brand_topic or inferred.get("brand_topic", "서비스")
        core_value = request.core_value or inferred.get("core_value", "우수성")
        symbol_type = request.symbol_type or inferred.get("symbol_type", "기하학적")
        logo_type = request.logo_type or inferred.get("logo_type", "심볼+텍스트 조합")
        vibes_list = request.vibes or [inferred.get("recommended_mood", "모던 & 신뢰")]

        image = generate_logo_image_with_context(
            brand_name=brand_name,
            brand_topic=brand_topic,
            core_value=core_value,
            vibes=vibes_list,
            brand_color=request.brand_color,
            symbol_type=symbol_type,
            logo_type=logo_type,
            background=request.background or "흰색",
        )
        return {"image": image}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로고 생성 중 오류 발생: {str(e)}")


@router.post("/brand/character-custom", response_model=CharacterGenerateResponse)
async def generate_character_custom(request: CharacterGenerateCustomRequest) -> dict[str, Any]:
    """
    Generate character with optional/auto-inferred variables.

    If variables are not provided, they will be inferred from available brand data.
    User can provide partial information, and the system will auto-complete.

    Args:
        request: CharacterGenerateCustomRequest with optional variables

    Returns:
        CharacterGenerateResponse with base64 encoded character image

    Raises:
        HTTPException: If generation fails
    """
    try:
        # Infer missing variables if needed
        inferred = infer_missing_variables(
            brand_name=request.brand_name,
            brand_topic=request.brand_topic,
            core_value=request.core_value,
            business_type=request.business_type,
            vibes=request.vibes,
            target=request.target,
            keywords=request.keywords,
        )

        # Use provided values if available, otherwise use inferred values
        brand_name = request.brand_name or inferred.get("brand_name", "Brand")
        brand_topic = request.brand_topic or inferred.get("brand_topic", "서비스")
        core_value = request.core_value or inferred.get("core_value", "우수성")
        character_name = request.character_name or inferred.get("character_name", "친구")
        character_concept = request.character_concept or inferred.get("character_concept", "귀여운 캐릭터")
        character_personality = (
            request.character_personality or inferred.get("character_personality", "친근함, 긍정적, 도움이 됨")
        )
        character_style = request.character_style or inferred.get("character_style", "플랫 일러스트")
        character_age_feel = request.character_age_feel or inferred.get("character_age_feel", "나이 초월")
        vibes_list = request.vibes or [inferred.get("recommended_mood", "따뜻 & 친근")]

        image = generate_character_image_with_context(
            brand_name=brand_name,
            brand_topic=brand_topic,
            core_value=core_value,
            character_name=character_name,
            character_concept=character_concept,
            character_personality=character_personality,
            vibes=vibes_list,
            character_style=character_style,
            character_age_feel=character_age_feel,
        )
        return {"image": image}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐릭터 생성 중 오류 발생: {str(e)}")


