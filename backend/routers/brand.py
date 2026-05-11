"""Brand generation router."""
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.brand_generator import generate_brand_identity

router = APIRouter()


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
