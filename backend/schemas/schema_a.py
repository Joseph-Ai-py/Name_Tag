# 파일 위치: backend/schemas/schema_a.py

from pydantic import BaseModel, Field

# ==========================================
# [A1] 철학과 코어 아이덴티티 스키마
# ==========================================
class BrandPhilosophy(BaseModel):
    manifesto: str = Field(description="철학 선언문 (1~2문단)")
    raison_detre: str = Field(description="브랜드 존재 이유 (1문장)")
    stand_against: list[str] = Field(description="반대하는 것 3가지")
    stand_for: list[str] = Field(description="지지하고 실천하는 가치 3가지")

class BrandEssence(BaseModel):
    keyword: str = Field(description="에센스 키워드 (1~3단어)")
    keyword_explanation: str = Field(description="해당 키워드의 실제 구현 설명 (3~4줄)")
    brand_definition: str = Field(description="브랜드 한 줄 정의 (50자 이내)")

class CoreValueItem(BaseModel):
    value: str = Field(description="핵심 가치 키워드")
    description: str = Field(description="가치에 대한 설명")
    example: str = Field(description="실제 실무 구현 예시")

class CoreIdentity(BaseModel):
    mission: str = Field(description="브랜드 미션 (동사형)")
    vision: str = Field(description="브랜드 비전 (명사형)")
    core_values: list[CoreValueItem] = Field(description="3대 핵심 가치")

class A1ResponseSchema(BaseModel):
    brand_philosophy: BrandPhilosophy
    brand_essence: BrandEssence
    core_identity: CoreIdentity


# ==========================================
# [A2] 스토리 및 버벌 툴킷 스키마
# ==========================================
class AlternativeName(BaseModel):
    name: str = Field(description="대안명 (국문)")
    name_en: str = Field(description="대안명 (영문)")
    rationale: str = Field(description="추천하는 이유")

class NamingExpansion(BaseModel):
    name_story: str = Field(description="탄생 스토리 (100자 이상)")
    domain_suggestions: list[str] = Field(description="추천 도메인 3가지")
    sns_handles: list[str] = Field(description="추천 SNS 핸들 3가지")
    alternative_names: list[AlternativeName] = Field(description="상표권 대안 네이밍 2가지")

class SubSlogan(BaseModel):
    slogan: str = Field(description="서브 슬로건")
    emphasis: str = Field(description="사용 상황 및 강조점")

class SloganExpansion(BaseModel):
    main_slogan_en: str = Field(description="영문 메인 슬로건")
    sub_slogans: list[SubSlogan] = Field(description="상황별 서브 슬로건 3가지")

class A2ResponseSchema(BaseModel):
    naming_expansion: NamingExpansion
    slogan_expansion: SloganExpansion
    brand_story_full: str = Field(description="브랜드 스토리 전문 (500자 이상)")


# ==========================================
# [A3] 포지셔닝 및 약속 스키마
# ==========================================
class Differentiator(BaseModel):
    point: str = Field(description="차별화 셀링 포인트 제목")
    description: str = Field(description="구체적인 차별점 설명")

class PositioningMap(BaseModel):
    axis_x: str = Field(description="X축의 양 극단 설명")
    axis_y: str = Field(description="Y축의 양 극단 설명")
    quadrants_description: str = Field(description="4개의 사분면 시장 묘사")
    our_exact_position: str = Field(description="우리의 정확한 위치와 분위기 묘사")

class Positioning(BaseModel):
    statement: str = Field(description="가치 제안 선언문 (For 타겟, ~과 달리 ~ 혜택 제공)")
    differentiators: list[Differentiator] = Field(description="3대 차별화 팩트")
    positioning_map_visualized: PositioningMap

class PromiseRule(BaseModel):
    channel: str = Field(description="마케팅, 패키징, CS 등 접점 채널")
    actionable_rule: str = Field(description="구체적인 실무 행동 지침")

class BrandPromise(BaseModel):
    declaration: str = Field(description="타협 불가능한 약속 선언문")
    proof_of_promise: list[PromiseRule] = Field(description="접점별 실천 행동 수칙 3가지")

class A3ResponseSchema(BaseModel):
    positioning: Positioning
    unbreakable_brand_promise: BrandPromise