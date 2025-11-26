"""
FastAPI main application.
Air Quality Platform API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import logger
from app.api.v1.router import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    Logs application startup.
    """
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"API available at {settings.API_V1_STR}")
    logger.info(f"Documentation available at {settings.API_V1_STR}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    Logs application shutdown.
    """
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


@app.get("/")
def root():
    """
    Root endpoint.
    Returns basic API information.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "status": "running"
    }


@app.get("/health")
def health():
    """
    Health check endpoint.
    Returns API health status.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

