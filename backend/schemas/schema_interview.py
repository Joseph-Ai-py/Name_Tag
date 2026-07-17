# 파일 위치: backend/schemas/schema_interview.py

from pydantic import BaseModel, Field

class InterviewQuestion(BaseModel):
    question_id: int = Field(description="질문 번호")
    question_text: str = Field(description="질문 내용")
    options: list[str] = Field(description="4지선다 객관식 선택지 4개")

class InterviewResponseSchema(BaseModel):
    required_question_count: int = Field(description="생성된 질문의 총 개수")
    reasoning: str = Field(description="이 질문들을 생성한 전략적 이유")
    questions: list[InterviewQuestion] = Field(description="실제 질문 리스트")