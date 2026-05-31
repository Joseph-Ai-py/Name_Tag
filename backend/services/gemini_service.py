from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts.nametag_prompts import SYSTEM_PROMPT

load_dotenv()

TEXT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview").strip() or "gemini-3-flash-preview"
IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview").strip() or "gemini-3.1-flash-image-preview"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_IMAGE_API_KEY = os.getenv("GEMINI_IMAGE_API_KEY", "").strip()


def parse_ai_response(raw_text: str) -> dict[str, Any]:
    match = re.search(r"\{[\s\S]*\}", raw_text)
    if not match:
        raise ValueError("AI 응답에서 JSON을 찾을 수 없습니다.")
    return json.loads(match.group())


def _is_retryable(error_text: str) -> bool:
    return any(code in error_text for code in ["429", "500", "502", "503"])


def request_gemini_text(prompt: str, max_retries: int = 10) -> dict[str, Any]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    attempt = 0
    while True:
        try:
            response = client.models.generate_content(
                model=TEXT_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return parse_ai_response(response.text or "")
        except Exception as exc:
            error_text = str(exc)
            if _is_retryable(error_text) and attempt < max_retries:
                attempt += 1
                time.sleep(90)
                continue
            raise


def request_gemini_image(prompt: str, max_retries: int = 3) -> bytes | None:
    if not GEMINI_IMAGE_API_KEY:
        raise RuntimeError("GEMINI_IMAGE_API_KEY가 설정되지 않았습니다.")

    client = genai.Client(api_key=GEMINI_IMAGE_API_KEY)
    attempt = 0
    while True:
        try:
            result = client.models.generate_content(
                model=IMAGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
            )
            if hasattr(result, "parts") and result.parts:
                part = result.parts[0]
                if hasattr(part, "inline_data") and part.inline_data:
                    return part.inline_data.data
                if hasattr(part, "image") and part.image:
                    return part.image.image_bytes
            return None
        except Exception as exc:
            error_text = str(exc)
            if _is_retryable(error_text) and attempt < max_retries:
                attempt += 1
                time.sleep(30)
                continue
            raise