from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.prompts import nametag_prompts_v2 as report_prompts
from backend.services.gemini_service import request_gemini_text
from backend.schemas.report_v2 import ReportInterviewResponse, ReportPageSchema

router = APIRouter()
logger = logging.getLogger(__name__)


class ReportContextRequest(BaseModel):
    context: dict[str, Any] = Field(default_factory=dict)


class GeneratePageRequest(ReportContextRequest):
    regenerate: bool = False
    conditional_decisions: dict[str, bool] = Field(default_factory=dict)


class ReportPlanRequest(ReportContextRequest):
    skipped_page_ids: list[str] = Field(default_factory=list)
    conditional_decisions: dict[str, bool] = Field(default_factory=dict)


def _harness(context: dict[str, Any]) -> report_prompts.ReportHarness:
    def generate_v2_json(prompt: str) -> dict[str, Any]:
        return request_gemini_text(
            prompt, system_instruction=report_prompts.V2_SYSTEM_PROMPT
        )

    harness = report_prompts.ReportHarness(generate_v2_json, max_repairs=2)
    harness.completed_pages = dict(context.get("pages", {}))
    harness.interview_answers = dict(context.get("interview_answers", {}))
    return harness


@router.get("/meta")
async def report_metadata() -> dict[str, Any]:
    return {
        "page_order": report_prompts.REPORT_PAGE_ORDER,
        "page_specs": report_prompts.REPORT_PAGE_SPECS,
        "interviews": report_prompts.INTERVIEW_SPECS,
        "required_interviews_by_page": report_prompts.REQUIRED_INTERVIEWS_BY_PAGE,
        "conditional_pages": ["17", "21"],
    }


@router.post("/plan")
async def report_plan(req: ReportPlanRequest) -> dict[str, Any]:
    context = req.context
    completed = set(context.get("pages", {}))
    skipped = set(req.skipped_page_ids)
    ready_pages = report_prompts.next_report_pages(
        completed, skipped, req.conditional_decisions
    )
    answers = context.get("interview_answers", {})
    ready_pages = [
        page_id for page_id in ready_pages
        if set(report_prompts.REQUIRED_INTERVIEWS_BY_PAGE.get(page_id, [])).issubset(answers)
    ]
    ready_interviews = report_prompts.next_report_interviews(
        completed, set(answers)
    )
    return {
        "ready_page_ids": ready_pages,
        "ready_interview_ids": ready_interviews,
        "completed_page_ids": sorted(completed),
        "skipped_page_ids": sorted(skipped),
    }


@router.post("/interviews/{interview_id}")
async def generate_report_interview(
    interview_id: str, req: ReportContextRequest
) -> dict[str, Any]:
    try:
        harness = _harness(req.context)
        result = harness.generate_interview(interview_id, req.context)
        validated = ReportInterviewResponse.model_validate(result)
        return validated.model_dump(mode="json")
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"인터뷰 생성 실패: {exc}") from exc


@router.post("/pages/{page_id}")
async def generate_report_page(
    page_id: str, req: GeneratePageRequest
) -> dict[str, Any]:
    try:
        harness = _harness(req.context)
        for conditional_id, enabled in req.conditional_decisions.items():
            harness.set_conditional_decision(conditional_id, enabled)
        page = harness.generate_page(page_id, req.context, regenerate=req.regenerate)
        validated_page = ReportPageSchema.model_validate(page)
        return {
            "page": validated_page.model_dump(mode="json"),
            "invalidated_page_ids": sorted(harness.get_invalidated_page_ids()),
        }
    except (ValueError, KeyError) as exc:
        logger.warning("Report page request rejected: page_id=%s error=%s", page_id, exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Report page generation failed unexpectedly: page_id=%s", page_id)
        raise HTTPException(status_code=502, detail=f"페이지 생성 실패: {exc}") from exc
