from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app import MAX_LENGTH


client = TestClient(app)

def test_classify_headline():
    response = client.post(
            "/classify",
            json={"headline": "Ebay stock is soaring after Depop acquisition"},
    )
    assert response.status_code == 200

def test_health_check():
    response_health = client.get("/health")
    assert response_health.status_code == 200
    assert response_health.json() == {
        "status": "ok",
    }

def test_blank_and_long_headline():
    response_blank = client.post(
            "/classify",
            json={"headline": ""},
    )
    print(response_blank.json())
    assert response_blank.status_code == 422

    response_long = client.post(
            "/classify",
            json={"headline": "Headline " * MAX_LENGTH},
    )
    assert response_long.status_code == 422

def test_classify_failure():
    with patch("app.models.pipeline", side_effect=Exception("Model error")):
        response = client.post(
            "/classify",
            json={"headline": "Some headline"},
        )
        assert response.status_code == 500
        assert "Classification failed" in response.json()["detail"]