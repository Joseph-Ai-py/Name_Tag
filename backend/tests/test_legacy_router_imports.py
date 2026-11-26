import importlib

import pytest

from backend.prompts.nametag_prompts import get_C_interview_prompt
from backend.routers.legacy_visual_identity_router import router as visual_router
from backend.main import app


@pytest.mark.parametrize(
    "module_name",
    [
        "backend.routers.legacy_brand_identity_router",
        "backend.routers.legacy_customer_strategy_router",
        "backend.routers.legacy_visual_identity_router",
        "backend.routers.legacy_logo_character_router",
        "backend.routers.legacy_naming_router",
    ],
)
def test_legacy_router_modules_import(module_name: str) -> None:
    module = importlib.import_module(module_name)
    assert module.router.routes


def test_legacy_visual_router_imports_defined_interview_prompt() -> None:
    assert callable(get_C_interview_prompt)
    assert any(route.path == "/interview" for route in visual_router.routes)


def test_legacy_routers_and_response_schemas_are_registered_in_app() -> None:
    openapi = app.openapi()
    paths = openapi["paths"]
    expected_paths = {
        "/api/section-o/interview",
        "/api/section-a/generate",
        "/api/section-b/generate",
        "/api/section-c/generate",
        "/api/section-de/generate",
    }
    assert expected_paths.issubset(paths)

    models = openapi["components"]["schemas"]
    expected_models = {
        "InterviewResponseSchema",
        "AGenerateResponseSchema",
        "AResponseSchema",
        "BGenerateResponseSchema",
        "BResponseSchema",
        "CGenerateResponseSchema",
        "CResponseSchema",
        "DEGenerateResponseSchema",
        "DEGeneratedDataSchema",
    }
    assert expected_models.issubset(models)
