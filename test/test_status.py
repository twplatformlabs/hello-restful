from fastapi.testclient import TestClient

from api.main import api
from api.config import route_prefix

client = TestClient(api)
client.base_url = client.base_url.join(route_prefix.rstrip("/") + "/")


def test_status_code_get_200():
    response = client.get("status/200")
    assert response.status_code == 200
    assert response.json() == {"message": 200}


def test_status_code_get_302():
    response = client.get("status/302")
    assert response.status_code == 302
    assert response.json() == {"message": 302}


def test_status_code_post_201():
    response = client.post("status/201")
    assert response.status_code == 201
    assert response.json() == {"message": 201}


def test_status_code_put_200():
    response = client.put("status/200")
    assert response.status_code == 200
    assert response.json() == {"message": 200}


def test_status_code_patch_200():
    response = client.patch("status/200")
    assert response.status_code == 200
    assert response.json() == {"message": 200}


def test_status_code_delete_204():
    response = client.delete("status/204")
    assert response.status_code == 204
    assert response.content == b""


def test_status_code_delete_404():
    response = client.delete("status/404")
    assert response.status_code == 404
    assert response.json() == {"message": 404}
