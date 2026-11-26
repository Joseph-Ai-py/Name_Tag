import pytest
from pydantic import ValidationError

from backend.schemas.legacy_interview_schema import InterviewResponseSchema


def _question(question_id: int) -> dict:
    return {
        "question_id": question_id,
        "question_text": f"질문 {question_id}",
        "options": ["1. A", "2. B", "3. C", "4. D"],
    }


def _payload(count: int) -> dict:
    return {
        "required_question_count": count,
        "reasoning": "검증용 데이터",
        "questions": [_question(i + 1) for i in range(count)],
    }


def test_valid_interview_response_passes() -> None:
    payload = _payload(5)
    parsed = InterviewResponseSchema.model_validate(payload)
    assert parsed.required_question_count == 5
    assert len(parsed.questions) == 5


@pytest.mark.parametrize("question_count", [4, 11])
def test_invalid_question_count_fails(question_count: int) -> None:
    payload = _payload(question_count)
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(payload)


@pytest.mark.parametrize("option_count", [3, 5])
def test_invalid_option_count_fails(option_count: int) -> None:
    payload = _payload(5)
    payload["questions"][0]["options"] = [f"{i}. x" for i in range(1, option_count + 1)]
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(payload)


def test_required_question_count_mismatch_fails() -> None:
    payload = _payload(5)
    payload["required_question_count"] = 6
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(payload)


def test_duplicate_question_id_fails() -> None:
    payload = _payload(5)
    payload["questions"][4]["question_id"] = 1
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(payload)


def test_blank_question_and_empty_choice_are_rejected() -> None:
    blank_question = _payload(5)
    blank_question["questions"][0]["question_text"] = "   "
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(blank_question)

    blank_choice = _payload(5)
    blank_choice["questions"][0]["options"][2] = "  "
    with pytest.raises(ValidationError):
        InterviewResponseSchema.model_validate(blank_choice)
