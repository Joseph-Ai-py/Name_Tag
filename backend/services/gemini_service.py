from __future__ import annotations

import json
import os
import re
import base64
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
    # Remove markdown code blocks if present
    cleaned = re.sub(r"```(?:json)?\n?", "", raw_text)
    cleaned = re.sub(r"```\n?", "", cleaned)
    
    # Extract first complete JSON object
    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned)
    if not match:
        raise ValueError(f"AI 응답에서 JSON을 찾을 수 없습니다: {raw_text[:200]}")
    
    json_str = match.group()
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # If basic parsing fails, try to extract from first { to first complete }
        try:
            start = cleaned.find('{')
            if start == -1:
                raise ValueError("JSON 시작 문자를 찾을 수 없습니다")
            # Find matching closing brace
            depth = 0
            end = -1
            for i in range(start, len(cleaned)):
                if cleaned[i] == '{':
                    depth += 1
                elif cleaned[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end == -1:
                raise ValueError("일치하는 closing brace를 찾을 수 없습니다")
            return json.loads(cleaned[start:end])
        except Exception as inner_e:
            raise ValueError(f"JSON 파싱 실패: {str(e)} / {str(inner_e)}")


def _is_retryable(error_text: str) -> bool:
    return any(code in error_text for code in ["429", "500", "502", "503"])


def request_gemini_text(prompt: str, max_retries: int = 10) -> dict[str, Any]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # 새로운 방식의 config 설정 (딕셔너리 형태)
    generation_config = {
        'temperature': 1,
        'max_output_tokens': 65536,
        'top_p': 0.95,
        'thinking_level': 'high', # 필요에 따라 조정 가능
    }

    attempt = 0
    while True:
        try:
            # 새로운 Interactions API 호출
            interaction = client.interactions.create(
                model=TEXT_MODEL,
                input=prompt,
                system_instruction=SYSTEM_PROMPT,
                generation_config=generation_config,
            )
            
            # output_text 속성을 통해 직관적으로 텍스트 추출 후 파싱
            return parse_ai_response(interaction.output_text or "")
            
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

    # 이미지 전용 API 키로 클라이언트 생성
    client = genai.Client(api_key=GEMINI_IMAGE_API_KEY)

    # 이미지 출력을 명시하는 config
    generation_config = {
        'response_modalities': ['IMAGE']
    }

    attempt = 0
    while True:
        try:
            interaction = client.interactions.create(
                model=IMAGE_MODEL,
                input=prompt,
                generation_config=generation_config,
            )

            # AI 스튜디오의 구조를 반영하여 응답 객체에서 이미지 바이트(bytes) 데이터 추출
            for step in interaction.steps:
                if step.type == 'model_output' and step.content:
                    for part in step.content:
                        if part.type == 'image' and hasattr(part, 'data'):
                            # Base64 문자열을 디코딩하여 실제 바이트 데이터로 반환
                            return base64.b64decode(part.data)

            # 이미지가 포함되지 않은 응답이 올 경우
            return None

        except Exception as exc:
            error_text = str(exc)
            if _is_retryable(error_text) and attempt < max_retries:
                attempt += 1
                time.sleep(30)
                continue
            raise

def request_gemini_text_with_model(prompt: str, model: str, max_retries: int = 6) -> dict[str, Any]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    attempt = 0
    while True:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return parse_ai_response(response.text or "")
        except Exception as exc:
            error_text = str(exc)
            if _is_retryable(error_text) and attempt < max_retries:
                attempt += 1
                time.sleep(10 + attempt * 5)
                continue
            raise


def _ensure_logs_dir():
    try:
        import pathlib

        p = pathlib.Path("logs")
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        return None


def _log_usage(model: str, prompt: str, response_text: str | None, metadata: dict | None = None):
    try:
        p = _ensure_logs_dir()
        if not p:
            return
        import json, time

        entry = {
            "ts": int(time.time()),
            "model": model,
            "prompt_len": len(prompt or ""),
            "response_len": len(response_text or ""),
        }
        if metadata:
            entry.update({"meta": metadata})
        with open(p / "gemini_usage.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def request_gemini_text_flash_lite(prompt: str, max_retries: int = 6, metadata: dict | None = None) -> dict[str, Any]:
    model = "gemini-2.0-flash-lite"
    resp = request_gemini_text_with_model(prompt, model=model, max_retries=max_retries)
    # attempt to log usage (prompt and response sizes) with optional metadata
    try:
        _log_usage(model, prompt, str(resp), metadata=metadata)
    except Exception:
        pass
    return resp