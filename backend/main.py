"""
Krishivaani - FastAPI Backend
Main entry point for the AI-powered Farm Decision Intelligence Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import uvicorn
from dotenv import load_dotenv
import os

logger = logging.getLogger("croprakshak")

# Load environment variables
load_dotenv()

# Import routers
from api.routes import (
    diagnosis,
    weather,
    risk_score,
    recommendations,
    schemes,
    chat,
    analytics,
    alerts
)

# Initialize FastAPI app
app = FastAPI(
    title="Krishivaani API",
    description="AI-Powered Farm Decision Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://krisi-sar-ai.vercel.app",
]

# Also allow Vercel preview deployments (e.g. krisi-sar-ai-git-*.vercel.app)
# without having to hardcode each one.
origin_regex = r"https://.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Krishivaani API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "krisisar-ai-backend",
        "version": "1.0.0"
    }

# Include routers
app.include_router(diagnosis.router, prefix="/api/v1/diagnosis", tags=["Diagnosis"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(risk_score.router, prefix="/api/v1/risk", tags=["Risk Score"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(schemes.router, prefix="/api/v1/schemes", tags=["Government Schemes"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])

GENERIC_5XX_MESSAGE = "Something went wrong. Please try again later."


# Sanitize 5xx HTTPExceptions raised by routes (e.g. detail=str(e)) so raw
# error text never reaches the client. 4xx messages (validation, "invalid
# image format", etc.) stay intact because they're safe and useful.
@app.exception_handler(StarletteHTTPException)
async def http_exception_sanitizer(request, exc: StarletteHTTPException):
    if exc.status_code >= 500:
        logger.error(
            "%s error on %s %s: %s",
            exc.status_code, request.method, request.url.path, exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "Server error", "message": GENERIC_5XX_MESSAGE},
        )
    # Non-5xx: use FastAPI's default handler (preserves helpful detail).
    return await http_exception_handler(request, exc)


# Catch-all for any unhandled (non-HTTP) exception: log it, return generic.
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": GENERIC_5XX_MESSAGE},
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        # Only watch our own source folders. We deliberately do NOT watch the
        # project root, because venv/ lives there and (especially inside OneDrive,
        # which constantly re-syncs library files) it triggers an endless reload
        # loop. Trade-off: edits to main.py / config.py need a manual restart.
        reload_dirs=["agents", "api", "models", "services", "utils"],
        log_level="info",
    )
