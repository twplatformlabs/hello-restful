"""
Header inspection.

Endpoints for retrieving HTTP request headers and the client's IP address.
"""

from typing import Dict, Any
from fastapi import APIRouter, Request, status

route = APIRouter()


@route.get(
    "/headers",
    summary="Return the incoming request's HTTP headers.",
    tags=["request inspection"],
    status_code=status.HTTP_200_OK,
)
async def get_headers(request: Request) -> Dict[str, Any]:
    """
    Returns the incoming HTTP request's headers.

    Args:
        request (Request): The incoming FastAPI request object.

    Returns:
        dict: A dictionary containing the request headers.
    """
    return {"headers": dict(request.headers)}


@route.get(
    "/ip",
    summary="Returns the requester's IP Address.",
    tags=["request inspection"],
    status_code=status.HTTP_200_OK,
)
async def get_ip(request: Request) -> Dict[str, Any]:
    """
    Returns the client's IP address from the request.

    Args:
        request (Request): The incoming FastAPI request object.

    Returns:
        dict: A dictionary containing the client's IP address.

    Note:
        In some environments (e.g., behind proxies), the IP may not be accurate unless forwarded headers are trusted.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return {"ip": forwarded.split(",")[0]}
    return {"ip": request.client.host}
