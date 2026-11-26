from pydantic import BaseModel, Field


class CoreTargetGroup(BaseModel):
    definition: str
    demographics: str
    lifestyle_keywords: list[str] = Field(default_factory=list)
    consumption_behavior: str


class PrimaryPersona(BaseModel):
    name: str
    age_and_job: str
    daily_scene: str
    pain_point_and_desire: str
    emotional_needs: list[str] = Field(default_factory=list)
    deal_breaker: str


class SecondaryPersona(BaseModel):
    id: int
    name_and_demographic: str
    character_type: str
    why_they_buy: str


class EmotionalTrigger(BaseModel):
    trigger: str
    reason: str


class B1ResponseSchema(BaseModel):
    target_strategy_reasoning: str
    core_target_group: CoreTargetGroup
    primary_persona: PrimaryPersona
    secondary_personas: list[SecondaryPersona] = Field(default_factory=list)
    emotional_triggers: list[EmotionalTrigger] = Field(default_factory=list)


class CustomerJourneyItem(BaseModel):
    stage: str
    touchpoint: str
    customer_emotion: str
    brand_action: str


class B2ResponseSchema(BaseModel):
    journey_strategy_reasoning: str
    customer_journey_map: list[CustomerJourneyItem] = Field(default_factory=list)


class BResponseSchema(BaseModel):
    target_strategy_reasoning: str
    core_target_group: CoreTargetGroup
    primary_persona: PrimaryPersona
    secondary_personas: list[SecondaryPersona] = Field(default_factory=list)
    emotional_triggers: list[EmotionalTrigger] = Field(default_factory=list)
    journey_strategy_reasoning: str
    customer_journey_map: list[CustomerJourneyItem] = Field(default_factory=list)


class BGenerateResponseSchema(BaseModel):
    data_b: BResponseSchema
