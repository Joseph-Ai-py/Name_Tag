# 파일 위치: backend/schemas/legacy_interview_schema.py

from pydantic import BaseModel, Field, field_validator, model_validator

class InterviewQuestion(BaseModel):
    question_id: int = Field(ge=1, description="질문 번호")
    question_text: str = Field(min_length=1, description="질문 내용")
    options: list[str] = Field(min_length=4, max_length=4, description="4지선다 객관식 선택지 4개")

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

class InterviewResponseSchema(BaseModel):
    required_question_count: int = Field(ge=5, le=10, description="생성된 질문의 총 개수")
    reasoning: str = Field(description="이 질문들을 생성한 전략적 이유")
    questions: list[InterviewQuestion] = Field(min_length=5, max_length=10, description="실제 질문 리스트")

    @model_validator(mode="after")
    def validate_question_consistency(self) -> "InterviewResponseSchema":
        if self.required_question_count != len(self.questions):
            raise ValueError("required_question_count must match questions length")

        ids = [q.question_id for q in self.questions]
        if len(ids) != len(set(ids)):
            raise ValueError("question_id values must be unique")

        return self
