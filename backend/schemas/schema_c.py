# 파일 위치: backend/schemas/schema_c.py

from pydantic import BaseModel, Field

# ==========================================
# [C] 비주얼 시스템 (컬러, 폰트, 무드, 디자인 원칙)
# ==========================================
class ColorPaletteItem(BaseModel):
    color_name: str = Field(description="주조색, 보조색 등 색상명")
    hex_code: str = Field(description="HEX 컬러 코드 (예: #FFFFFF)")
    role: str = Field(description="Primary, Secondary, Accent, Background, Text Color 중 하나")
    reason: str = Field(description="해당 컬러 선정 이유")

class FontDetail(BaseModel):
    font_name_kr: str = Field(description="한글 서체명 (예: 본고딕)")
    google_fonts_family: str = Field(description="Google Fonts 가족명 (예: Noto Sans KR)")
    weight_recommendation: int = Field(description="권장 굵기 숫자 (예: 400, 800)")
    usage_and_reason: str = Field(description="사용처 및 어울리는 이유")

class Typography(BaseModel):
    primary_font: FontDetail
    secondary_font: FontDetail

class VisualMoodGuide(BaseModel):
    photography_do: list[str] = Field(description="권장하는 사진/비주얼 표현 3가지")
    photography_dont: list[str] = Field(description="피해야 할 사진/비주얼 표현 3가지")
    mood_keywords: list[str] = Field(description="무드 키워드 5가지")

class DesignPrinciples(BaseModel):
    layout_direction: str = Field(description="레이아웃 방향성 설명")
    image_processing: str = Field(description="이미지 보정 및 가공 규칙 설명")

# 최종적으로 C 파트에서 받아야 할 전체 껍질
class CResponseSchema(BaseModel):
    color_palette: list[ColorPaletteItem] # 리스트 형태를 무조건 지키도록 강제!
    typography: Typography
    visual_mood_guide: VisualMoodGuide
    design_principles: DesignPrinciples