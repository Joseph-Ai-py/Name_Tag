# 파일 위치: backend/schemas/schema_de.py

from pydantic import BaseModel, Field

# ==========================================
# [D] 로고 아이덴티티
# ==========================================
class LogoConcept(BaseModel):
    symbol_reason: str = Field(description="심볼 선정 이유")
    color_reason: str = Field(description="컬러 선정 이유")
    overall_message: str = Field(description="로고가 전달해야 할 전체 메시지")
    direction_text: str = Field(description="이미지 생성용 영문 디렉션 텍스트")

class LogoGuide(BaseModel):
    minimum_size: str = Field(description="최소 사용 크기")
    clear_space: str = Field(description="클리어 스페이스 규정")

class LogoIdentity(BaseModel):
    concept: LogoConcept
    guide: LogoGuide

# ==========================================
# [E] 브랜드 캐릭터 가이드 (이 부분이 누락됐었음!)
# ==========================================
class CharacterIntro(BaseModel):
    name: str = Field(description="캐릭터 이름")
    appearance: str = Field(description="캐릭터 외형 묘사")
    symbolic_value: str = Field(description="상징 가치")

class CharacterReasoning(BaseModel):
    selection_reason: str = Field(description="캐릭터 선택 이유")
    emotional_connection: str = Field(description="고객과의 감정적 연결 포인트")

class CharacterStory(BaseModel):
    background: str = Field(description="캐릭터 배경 스토리")
    brand_role: str = Field(description="브랜드 내 역할")

class CharacterGuide(BaseModel):
    intro: CharacterIntro
    reasoning: CharacterReasoning
    story: CharacterStory

# 최종적으로 DE 파트에서 받아야 할 전체 껍질
class DEResponseSchema(BaseModel):
    logo_identity: LogoIdentity
    character_guide: CharacterGuide