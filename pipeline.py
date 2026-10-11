from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

V1_DIR = Path(__file__).resolve().parents[1]
V2_DIR = Path(__file__).resolve().parent


def _load_v1_modules(*module_names: str) -> dict[str, ModuleType]:
    """Load legacy pipeline modules with their original absolute imports.

    v2 keeps its models and state isolated; the adapter temporarily gives the
    legacy modules their own import namespace and restores v2 precedence after
    loading.
    """
    previous_path = list(sys.path)
    previous_modules = {
        name: sys.modules.get(name)
        for name in (
            "models",
            "prompts",
            "utils",
            "gemini_client",
            "image_service",
            "brand_dna",
            "pdf_builder",
            "pdf_service",
        )
    }
    sys.path = [str(V1_DIR)] + [path for path in sys.path if path not in {str(V1_DIR), str(V2_DIR)}]
    try:
        for name in previous_modules:
            sys.modules.pop(name, None)
        loaded = {name: importlib.import_module(name) for name in module_names}
    finally:
        sys.path = previous_path
        for name, module in previous_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
    return loaded


def generate_o_candidates(initial_idea: str, conversation_text: str) -> list[dict[str, Any]]:
    modules = _load_v1_modules("logic_o")
    brand_data = modules["logic_o"].BrandData(initial_idea=initial_idea)
    response = modules["logic_o"].generate_o_candidates(brand_data, conversation_text)
    return response.get("candidates", []) if isinstance(response, dict) else []


def confirm_brand_candidate(candidates: list[dict[str, Any]], index: int) -> dict[str, Any]:
    modules = _load_v1_modules("logic_o")
    brand_info = modules["logic_o"].apply_candidate_mix(
        candidates,
        {key: index for key in ("name", "meaning", "slogan", "story", "color")},
    )
    return brand_info.model_dump()


def generate_full_pipeline(
    brand_info_data: dict[str, Any],
    conversation_text: str,
) -> dict[str, Any]:
    modules = _load_v1_modules("models", "logic_a", "logic_b", "logic_c", "logic_de")
    models_module = modules["models"]
    brand_info = models_module.BrandInfo(**brand_info_data)
    data_a = modules["logic_a"].generate_section_a(brand_info, conversation_text).get("data_a", {})
    data_b = modules["logic_b"].generate_section_b(brand_info, conversation_text, conversation_text, data_a).get("data_b", {})
    data_c = modules["logic_c"].generate_section_c(brand_info, conversation_text, conversation_text, conversation_text, data_a, data_b).get("data_c", {})
    data_de = modules["logic_de"].generate_section_de(
        brand_info,
        data_c,
        conversation_text,
        conversation_text,
        conversation_text,
        conversation_text,
        data_a,
        data_b,
    ).get("data_de", {})
    return {"brand_info": brand_info_data, "A": data_a, "B": data_b, "C": data_c, "DE": data_de}


def generate_pdf(results: dict[str, Any], decision_traces: list[dict[str, Any]]) -> bytes:
    modules = _load_v1_modules("models", "brand_dna", "pdf_builder", "pdf_service")
    dna = modules["brand_dna"].build_brand_dna(
        results.get("brand_info", {}),
        results.get("A", {}),
        results.get("B", {}),
        results.get("C", {}),
        results.get("DE", {}),
    )
    integrity = {"status": "PASS", "issues": []}
    return modules["pdf_service"].generate_pdf_bytes(
        results.get("brand_info", {}),
        results.get("A", {}),
        results.get("B", {}),
        results.get("C", {}),
        results.get("DE", {}),
        dna,
        integrity,
        decision_traces,
    )
