from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health", summary="Service Health Check")
def health_check():
    """Returns the operational status, environment profile, and API version."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "api_version": "v1",
        "project": settings.PROJECT_NAME,
    }
