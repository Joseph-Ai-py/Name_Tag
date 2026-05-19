"""FastAPI backend for NameTag - Package A"""
import os
import sys
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers import brand
from utils.logger import setup_logger, get_logger

load_dotenv()

# Setup logger
logger = get_logger("NameTag.Backend")
logger.info("🚀 Initializing FastAPI backend...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("✅ FastAPI backend starting...")
    yield
    logger.info("👋 FastAPI backend shutting down...")


app = FastAPI(
    title="NameTag API",
    description="AI-powered brand identity generation API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brand.router, prefix="/api/v1", tags=["brand"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with detailed logging."""
    logger.error(f"🔴 Validation Error on {request.method} {request.url.path}")
    logger.error(f"   Request body: {await request.body()}")
    logger.error(f"   Errors: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": error.get("loc"),
                    "msg": error.get("msg"),
                    "type": error.get("type"),
                }
                for error in exc.errors()
            ]
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.debug("Health check requested")
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting uvicorn on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
