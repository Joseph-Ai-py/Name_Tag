from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class Candidate(BaseModel):
    text: str
    rationale: Optional[str] = None


class CandidatesResponse(BaseModel):
    candidates: List[Candidate]
