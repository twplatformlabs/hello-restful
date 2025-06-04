"""
hello-restful API

Return server information queried from Istio Envoy sidecar metadata.
"""

from typing import Dict, Union
import httpx
from fastapi import APIRouter, status, HTTPException

from api.config import settings

route = APIRouter()


@route.get(
    "/istio/envoy",
    summary="Return envoy metadata",
    tags=["istio"],
    status_code=status.HTTP_200_OK,
)
async def get_envoy_metadata() -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Queries the Envoy sidecar for locality metadata using the server_info_url setting.

    Returns:
        dict: A dictionary containing locality metadata on success,
              or an error message on failure.

    Raises:
        HTTPException: If the upstream request fails or returns invalid JSON.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.server_info_url)
            response.raise_for_status()
            json_response = await response.json()
            locality = json_response["node"]["locality"]
            return {"locality": locality}

    except (httpx.RequestError, httpx.HTTPStatusError) as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to query server information",
        ) from err

    except (KeyError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected response format from server",
        ) from err
