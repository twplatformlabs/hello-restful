import json

import requests.exceptions
from fastapi.testclient import TestClient
import pytest
import httpx
from mock import patch
from unittest.mock import AsyncMock, patch

from api.config import route_prefix
from api.main import api

client = TestClient(api)
client.base_url = client.base_url.join(route_prefix.rstrip("/") + "/")


@patch("requests.get")
def test_istio_envoy_returns_502_when_endpoint_unreachable(mock_server_response):
    mock_server_response.side_effect = requests.exceptions.ConnectionError
    response = client.get("istio/envoy")
    assert response.status_code == 502
    assert response.json() == {"detail": "Unable to query server information"}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_istio_envoy_returns_200_when_endpoint_reachable(mock_server_response):
    locality_info = {
        "region": "us-region-2",
        "zone": "us-region-2c",
        "sub_zone": "some-zone",
    }

    server_info = {"locality": locality_info}

    # server_info = {
    #     "node": {
    #         "locality": locality_info,
    #     }
    # }

    mock_response = AsyncMock()
    # mock_response.json.return_value = server_info
    mock_response.json = AsyncMock(return_value=server_info)
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_server_response.return_value = mock_response

    transport = httpx.ASGITransport(app=api)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/istio/envoy")

    assert response.status_code == 200
    assert await response.json() == {"locality": locality_info}
