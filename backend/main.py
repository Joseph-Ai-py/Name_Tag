from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
# Ensure backend package directory is importable for modules that use top-level imports like `prompts`
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from backend.routers import section_a, section_b, section_c, section_de, section_o

pdf_router = None
try:
    from backend.routers import pdf as pdf_module

    pdf_router = pdf_module.router
except Exception as exc:
    print(f"[WARN] PDF router disabled: {exc}")

load_dotenv()

app = FastAPI(title="NameTag API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(section_o.router, prefix="/api/section-o")
app.include_router(section_a.router, prefix="/api/section-a")
app.include_router(section_b.router, prefix="/api/section-b")
app.include_router(section_c.router, prefix="/api/section-c")
app.include_router(section_de.router, prefix="/api/section-de")
try:
    from backend.routers import uploads as uploads_module
    app.include_router(uploads_module.router, prefix="/api/uploads")
except Exception as exc:
    print(f"[WARN] uploads router disabled: {exc}")
if pdf_router is not None:
    app.include_router(pdf_router, prefix="/api/pdf")

try:
    from services.upload_store import initialize_upload_db

    initialize_upload_db()
except Exception as exc:
    print(f"[WARN] upload DB init failed: {exc}")

ASSETS_DIR = ROOT_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
