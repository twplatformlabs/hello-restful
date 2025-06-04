import pytest
from fastapi.testclient import TestClient

from api.main import api
from api.config import route_prefix

client = TestClient(api)
client.base_url = client.base_url.join(route_prefix.rstrip("/") + "/")


def test_inspection_headers():
    response = client.get("headers")
    assert response.status_code == 200


# @pytest.mark.skip(reason="until fastapi supports starlette>=0.37.2 with fix in https://github.com/encode/starlette/pull/2525")
def test_inspection_ip():
    response = client.get("ip")
    assert response.status_code == 200
    assert "ip" in response.json()
