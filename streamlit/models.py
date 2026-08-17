from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BrandData(BaseModel):
	business_type: str
	vibes: list[str]
	target: str
	keywords: str = ""


class BrandInfo(BaseModel):
	brand_name: str
	brand_name_en: str
	name_meaning: str
	slogan: str
	story_summary: str
	seed_color: str
	seed_color_reason: str


class InterviewQuestion(BaseModel):
	question_id: int = Field(description="Question index")
	question_text: str = Field(description="Question text")
	options: list[str] = Field(description="Four-choice options")


class InterviewResponseSchema(BaseModel):
	required_question_count: int = Field(description="Generated question count")
	reasoning: str = Field(description="Why these questions are asked")
	questions: list[InterviewQuestion] = Field(description="Questions list")


class Candidate(BaseModel):
	text: str
	rationale: str | None = None


class CandidatesResponse(BaseModel):
	candidates: list[Candidate]


class CoreValueItem(BaseModel):
	value: str
	description: str
	example: str


class BrandPhilosophy(BaseModel):
	manifesto: str
	raison_detre: str
	stand_against: list[str]
	stand_for: list[str]


class BrandEssence(BaseModel):
	keyword: str
	keyword_explanation: str
	brand_definition: str


class CoreIdentity(BaseModel):
	mission: str
	vision: str
	core_values: list[CoreValueItem]


class AlternativeName(BaseModel):
	name: str
	name_en: str
	rationale: str


class NamingExpansion(BaseModel):
	name_story: str
	domain_suggestions: list[str]
	sns_handles: list[str]
	alternative_names: list[AlternativeName]


class SubSlogan(BaseModel):
	slogan: str
	emphasis: str


class SloganExpansion(BaseModel):
	main_slogan_en: str
	sub_slogans: list[SubSlogan]


class Differentiator(BaseModel):
	point: str
	description: str


class PositioningMap(BaseModel):
	axis_x: str
	axis_y: str
	quadrants_description: str
	our_exact_position: str


class Positioning(BaseModel):
	statement: str
	differentiators: list[Differentiator]
	positioning_map_visualized: PositioningMap


class PromiseRule(BaseModel):
	channel: str
	actionable_rule: str


class BrandPromise(BaseModel):
	declaration: str
	proof_of_promise: list[PromiseRule]


class A1ResponseSchema(BaseModel):
	brand_philosophy: BrandPhilosophy
	brand_essence: BrandEssence
	core_identity: CoreIdentity


class A2ResponseSchema(BaseModel):
	naming_expansion: NamingExpansion
	slogan_expansion: SloganExpansion
	brand_story_full: str


class A3ResponseSchema(BaseModel):
	positioning: Positioning
	unbreakable_brand_promise: BrandPromise


class AResponseSchemaSet(BaseModel):
	data_a: dict[str, Any]


class ColorPaletteItem(BaseModel):
	color_name: str
	hex_code: str
	role: str
	reason: str


class FontDetail(BaseModel):
	font_name_kr: str
	google_fonts_family: str
	weight_recommendation: int
	usage_and_reason: str


class Typography(BaseModel):
	primary_font: FontDetail
	secondary_font: FontDetail


class VisualMoodGuide(BaseModel):
	photography_do: list[str]
	photography_dont: list[str]
	mood_keywords: list[str]


class DesignPrinciples(BaseModel):
	layout_direction: str
	image_processing: str


class CResponseSchema(BaseModel):
	color_palette: list[ColorPaletteItem]
	typography: Typography
	visual_mood_guide: VisualMoodGuide
	design_principles: DesignPrinciples


class LogoConcept(BaseModel):
	symbol_reason: str
	color_reason: str
	overall_message: str
	direction_text: str


class LogoGuide(BaseModel):
	minimum_size: str
	clear_space: str


class LogoIdentity(BaseModel):
	concept: LogoConcept
	guide: LogoGuide


class CharacterIntro(BaseModel):
	name: str
	appearance: str
	symbolic_value: str


class CharacterReasoning(BaseModel):
	selection_reason: str
	emotional_connection: str


class CharacterStory(BaseModel):
	background: str
	brand_role: str


class CharacterGuide(BaseModel):
	intro: CharacterIntro
	reasoning: CharacterReasoning
	story: CharacterStory


class DEResponseSchema(BaseModel):
	logo_identity: LogoIdentity
	character_guide: CharacterGuide

