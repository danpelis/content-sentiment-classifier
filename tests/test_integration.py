import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:7860"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_classify_headline():
    response = requests.post(
        f"{BASE_URL}/classify",
        json={"headline": "Stock market rises"},
    )

    logger.info(f"Status: {response.status_code}")
    logger.info(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert "sentiment" in response.json()
    assert "confidence" in response.json()