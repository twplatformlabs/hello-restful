"""
Health check endpoint for the hello-restful API.

This endpoint provides a basic liveness check to ensure the service is up and returning metadata.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, status
from ..config import settings

route = APIRouter()


@route.get(
    "/healthz",
    summary="Simple service health check.",
    tags=["main"],
    status_code=status.HTTP_200_OK,
)
async def get_healthz() -> Dict[str, Any]:
    """
    Performs a simple liveness health check.

    Returns:
        dict: A JSON object containing service metadata.
    """
    return {
        "status": "ok",
        "api": settings.version,
        "version": settings.releaseId,
        "description": "health of hello-restful service",
        "time": datetime.now(timezone.utc).isoformat(),
    }
