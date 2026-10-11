from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel

V1_DIR = Path(__file__).resolve().parents[1]
V2_DIR = Path(__file__).resolve().parent
if str(V2_DIR) not in sys.path:
    sys.path.insert(0, str(V2_DIR))
if str(V1_DIR) not in sys.path:
    sys.path.append(str(V1_DIR))

from brand_dna import check_brand_integrity  # noqa: E402

from models import BrandDocument, ConversationState  # noqa: E402


def build_brand_document(state: ConversationState) -> BrandDocument:
    raw = state.raw_results
    identity = raw.get("O", {})
    strategy = raw.get("A", {})
    customer = {
        "target": raw.get("B1", {}),
        "journey": raw.get("B2", {}),
        "swot": raw.get("B4", {}),
    }
    business = raw.get("B5", {})
    visual = {"visual": raw.get("C", {}), "identity": raw.get("DE", {})}
    integrity = state.raw_results.get("integrity", {})
    return BrandDocument(
        identity=identity,
        strategy=strategy,
        customer=customer,
        business=business,
        visual=visual,
        decisions=state.decision_traces,
        integrity=integrity,
    )


def build_pdf_view_model(document: BrandDocument) -> dict[str, Any]:
    return {
        "cover": document.identity,
        "O": document.identity,
        "A": document.strategy,
        "B1": document.customer.get("target", {}),
        "B2": document.customer.get("journey", {}),
        "B4": document.customer.get("swot", {}),
        "B5": document.business,
        "C": document.visual.get("visual", {}),
        "DE": document.visual.get("identity", {}),
        "DECISION_MAP": document.decisions,
        "INTEGRITY": document.integrity,
    }


def refresh_integrity(document: BrandDocument, brand_info: dict[str, Any] | None = None) -> BrandDocument:
    dna_like = {"foundation": document.identity}
    outputs = build_pdf_view_model(document)
    document.integrity = check_brand_integrity(brand_info or document.identity, dna_like, outputs)
    return document
