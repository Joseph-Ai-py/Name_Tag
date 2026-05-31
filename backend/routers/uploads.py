from __future__ import annotations

import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from models.uploads import Upload
from services.upload_store import list_upload_rows, save_upload

router = APIRouter()

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "uploads"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=Upload)
async def upload_file(file: UploadFile = File(...)):
    try:
        dest = ASSETS_DIR / file.filename
        with open(dest, "wb") as f:
            content = await file.read()
            f.write(content)

        upload_id = save_upload(file.filename, str(dest))
        upload = Upload(id=upload_id, filename=file.filename, path=str(dest))
        return upload
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/list", response_model=List[Upload])
async def list_uploads():
    rows = list_upload_rows()
    uploads = [Upload(id=row["id"], filename=row["filename"], path=row["path"], created_at=row["created_at"]) for row in rows]
    return JSONResponse(content=[f.model_dump() for f in uploads])
