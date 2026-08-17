from __future__ import annotations

import re
from typing import Any


def coerce_to_dict(value: Any) -> dict[str, Any]:
	if isinstance(value, dict):
		return value
	return {}


def safe_get_nested(data: dict[str, Any], path: list[str], default: Any = None) -> Any:
	current: Any = data
	for key in path:
		if not isinstance(current, dict):
			return default
		current = current.get(key)
		if current is None:
			return default
	return current


def validate_hex_color(value: str) -> bool:
	return bool(re.fullmatch(r"#[0-9a-fA-F]{6}", value or ""))


def normalize_candidates(result: dict[str, Any]) -> list[dict[str, str]]:
	raw = result.get("candidates", []) if isinstance(result, dict) else []
	normalized: list[dict[str, str]] = []
	for item in raw:
		if isinstance(item, dict):
			text = str(item.get("text", "")).strip()
			rationale = item.get("rationale")
			if text:
				normalized.append({"text": text, "rationale": str(rationale) if rationale else ""})
		else:
			text = str(item).strip()
			if text:
				normalized.append({"text": text, "rationale": ""})
	return normalized

