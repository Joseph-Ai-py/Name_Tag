from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ReportInterviewQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: int = Field(ge=1)
    question_text: str = Field(min_length=1)
    options: list[str] = Field(min_length=4, max_length=4)

    @field_validator("question_text")
    @classmethod
    def question_text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question_text must not be blank")
        return value.strip()

    @field_validator("options")
    @classmethod
    def options_must_be_four_nonempty_strings(cls, value: list[str]) -> list[str]:
        if len(value) != 4 or any(not option.strip() for option in value):
            raise ValueError("each question must have exactly four non-empty options")
        return [option.strip() for option in value]


class ReportInterviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_question_count: int = Field(ge=5, le=10)
    reasoning: str = Field(min_length=1)
    questions: list[ReportInterviewQuestion] = Field(min_length=5, max_length=10)

    @model_validator(mode="after")
    def validate_question_count_and_ids(self) -> "ReportInterviewResponse":
        if self.required_question_count != len(self.questions):
            raise ValueError("required_question_count must match questions length")
        question_ids = [question.question_id for question in self.questions]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("question_id values must be unique")
        return self


class ReportPageSchema(BaseModel):
    """Validated common page envelope; page-specific data is checked by prompt contracts."""

    model_config = ConfigDict(extra="forbid")

    page_id: str = Field(pattern=r"^(?:0[0-9]|1[0-9]|2[0-4])$")
    title: str = Field(min_length=1)
    status: Literal["complete", "insufficient_data", "to_validate"]
    data: dict[str, Any]
    # Mirrors the page contract supplied in the prompt; renderers consume `data` only.
    field_guidance: list[str] = Field(default_factory=list)
    evidence_type: str = Field(min_length=1)
    source_ids: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"]
    validation_notes: list[str] = Field(default_factory=list)


class ReportPageLayoutSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_id: str = Field(pattern=r"^(?:0[0-9]|1[0-9]|2[0-4])$")
    paper_size: Literal["A4", "A3"]
    orientation: Literal["portrait", "landscape"]
    margins_mm: int = Field(default=12, ge=5, le=30)


class ReportV2PdfRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pages: dict[str, ReportPageSchema] = Field(min_length=1)
    page_layouts: list[ReportPageLayoutSchema] = Field(default_factory=list)
    brand_name: str = Field(default="NAME TAG", min_length=1)

    @model_validator(mode="after")
    def validate_page_keys(self) -> "ReportV2PdfRequest":
        for key, page in self.pages.items():
            if key != page.page_id:
                raise ValueError(f"page key {key} does not match page_id {page.page_id}")
        return self
