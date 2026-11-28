from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from gemini_client import request_gemini_image
from prompts import get_character_image_prompt, get_logo_image_prompt

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def save_image(image_data: bytes, subdir: str, filename_prefix: str, brand_name: str) -> str:
	target_dir = ASSETS_DIR / subdir
	target_dir.mkdir(parents=True, exist_ok=True)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	safe_brand_name = brand_name.replace(" ", "_")
	file_path = target_dir / f"{filename_prefix}_{safe_brand_name}_{timestamp}.png"
	file_path.write_bytes(image_data)
	return str(file_path.resolve())


def _log_image_request(kind: str, brand_name: str, payload: dict[str, Any]) -> None:
	print(
		f"[DEBUG] {kind} image request - brand={brand_name}, keys={list(payload.keys())}, "
		f"concept_keys={list(payload.get('logo_identity', {}).get('concept', {}).keys()) if kind == 'logo' else list(payload.get('character_guide', {}).keys())}"
	)


def generate_logo_image(
	brand_name: str,
	de_section_data: dict[str, Any],
	brand_info: dict[str, Any],
	data_c: dict[str, Any],
	deepdive_answers_text: str,
) -> str | None:
	_log_image_request("logo", brand_name, de_section_data)
	concept = de_section_data.get("logo_identity", {}).get("concept", {})
	direction_text = concept.get("direction_text", "Modern, clean wordmark or symbol")
	prompt = get_logo_image_prompt(
		brand_name=brand_name,
		direction_text=direction_text,
		brand_info=brand_info,
		deepdive_answers_text=deepdive_answers_text,
		data_c=data_c,
	)
	image_data = request_gemini_image(prompt)
	if not image_data:
		return None
	return save_image(image_data, "logos", "logo", brand_name)


def generate_character_image(
	brand_name: str,
	de_section_data: dict[str, Any],
	brand_info: dict[str, Any],
	data_c: dict[str, Any],
	deepdive_answers_text: str,
) -> str | None:
	_log_image_request("character", brand_name, de_section_data)
	char_guide = de_section_data.get("character_guide", {})
	intro = char_guide.get("intro", {})
	reasoning = char_guide.get("reasoning", {})

	prompt = get_character_image_prompt(
		brand_name=brand_name,
		char_name=intro.get("name", "Mascot"),
		char_appearance=intro.get("appearance", "A compelling brand character"),
		symbolic_value=intro.get("symbolic_value", "Brand symbol"),
		emotional_connection=reasoning.get("emotional_connection", "Emotional connection with customers"),
		brand_info=brand_info,
		deepdive_answers_text=deepdive_answers_text,
		data_c=data_c,
	)

	image_data = request_gemini_image(prompt)
	if not image_data:
		return None
	return save_image(image_data, "characters", "char", brand_name)

