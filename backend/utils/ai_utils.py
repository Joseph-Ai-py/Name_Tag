from __future__ import annotations

import json
from typing import Any, List, Dict


def normalize_candidates(raw: Any) -> List[Dict[str, str]]:
    """Normalize various AI response shapes into a list of {text, rationale?} dicts.

    Accepts:
    - {"candidates": ["a","b"]}
    - {"candidates": [{"text":"a","rationale":"x"}, ...]}
    - raw list ["a","b"]

    Returns list of objects: [{"text": "a", "rationale": "..."}, ...]
    """
    candidates: List[Dict[str, str]] = []

    if raw is None:
        return candidates

    # If raw is a dict with 'candidates'
    if isinstance(raw, dict) and "candidates" in raw:
        items = raw.get("candidates")
    else:
        items = raw

    # If items is a JSON string, attempt to parse
    if isinstance(items, str):
        try:
            parsed = json.loads(items)
            items = parsed
        except Exception:
            # treat as single-item text
            items = [items]

    if isinstance(items, list):
        for it in items:
            if isinstance(it, str):
                candidates.append({"text": it})
            elif isinstance(it, dict):
                text = it.get("text") or it.get("candidate") or it.get("value") or ""
                rationale = it.get("rationale") or it.get("reason") or ""
                candidates.append({"text": text, "rationale": rationale})
            else:
                candidates.append({"text": str(it)})

    return candidates
